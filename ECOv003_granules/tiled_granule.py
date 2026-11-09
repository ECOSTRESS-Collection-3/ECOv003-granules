from __future__ import annotations

import json
import logging
import os
import posixpath
import zipfile
from datetime import datetime, timedelta
from glob import glob
from os import makedirs
from os.path import join, splitext, basename, abspath, expanduser, exists
from time import perf_counter
from typing import Union, List, Optional

import colored_logging as cl
import numpy as np
import rasters
from dateutil import parser
from matplotlib.cm import get_cmap
from matplotlib.colors import Colormap
from rasters import Raster, RasterGeometry, RasterGrid
from shapely import Polygon

from .granule import ECOSTRESSGranule
from .write_XML_metadata import write_XML_metadata

DEFAULT_JSON_INDENT = 2

logger = logging.getLogger(__name__)


class ECOSTRESSTiledGranule(ECOSTRESSGranule):
    _PRODUCT_NAME = None

    _COMPRESSION = "zstd"
    _GRANULE_PREVIEW_CMAP = "jet"

    _STANDARD_METADATA_GROUP = "StandardMetadata"
    _PRODUCT_METADATA_GROUP = "ProductMetadata"

    VARIABLE_CMAPS = {}

    def __init__(
            self,
            product_location: str = None,
            orbit: int = None,
            scene: int = None,
            tile: str = None,
            time_UTC: Union[datetime, str] = None,
            build: str = None,
            process_count: int = None,
            *args,
            containing_directory: str = None,
            compression: str = None,
            layer_preview_quality: int = None,
            granule_preview_cmap: Union[Colormap, str] = None,
            granule_preview_shape: (int, int) = None,
            granule_preview_quality: int = None,
            **kwargs):
        ECOSTRESSGranule.__init__(
            self,
            *args,
            product_filename=product_location,
            granule_preview_cmap=granule_preview_cmap,
            granule_preview_shape=granule_preview_shape,
            granule_preview_quality=granule_preview_quality,
            **kwargs
        )

        if product_location is None:
            if isinstance(time_UTC, str):
                time_UTC = parser.parse(time_UTC)

            granule_name = self.generate_granule_name(
                orbit=orbit,
                scene=scene,
                tile=tile,
                time_UTC=time_UTC,
                process_count=process_count
            )

            if containing_directory is None:
                containing_directory = "."

            product_location = join(containing_directory, granule_name)
        else:
            granule_name = splitext(basename(product_location))[0]

        product_location = abspath(expanduser(product_location))

        if not exists(product_location) and not product_location.endswith(".zip"):
            makedirs(product_location, exist_ok=True)

        if layer_preview_quality is None:
            layer_preview_quality = self._LAYER_PREVIEW_QUALITY

        if compression is None:
            compression = self._COMPRESSION

        self._metadata_dict = None

        self._product_location = product_location
        self._orbit = orbit
        self._scene = scene
        self._tile = tile
        self._time_UTC = time_UTC
        self._time_solar = None
        self._build = build
        self._process_count = process_count
        self._granule_name = granule_name
        self.layer_preview_quality = layer_preview_quality
        self.compression = compression

    @property
    def product_location(self) -> str:
        return self._product_location

    @property
    def filename(self) -> str:
        return self.product_location

    @property
    def product_directory(self) -> str:
        product_location = self.product_location

        if self.is_zip:
            product_directory = splitext(product_location)[0]
        else:
            product_directory = product_location

        return product_directory

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.product_location}")'

    @property
    def metadata_filename_base(self) -> str:
        return f"{self.granule_name}.json"

    @property
    def metadata_filename(self) -> str:
        return join(self.product_directory, self.metadata_filename_base)

    @property
    def metadata_dict(self) -> dict:
        if self._metadata_dict is not None:
            return self._metadata_dict

        if self.is_zip:
            zip_filename = self.product_location
            filename = posixpath.join(self.granule_name, self.metadata_filename_base)

            logger.info(f"reading metadata file {cl.file(filename)} from product zip {cl.file(zip_filename)}")

            with zipfile.ZipFile(zip_filename) as file:
                JSON_text = file.read(filename)
        else:
            filename = self.metadata_filename

            with open(filename, "r") as file:
                JSON_text = file.read()

        metadata_dict = json.loads(JSON_text)
        self._metadata_dict = metadata_dict

        return metadata_dict

    @property
    def standard_metadata(self) -> dict:
        return self.metadata_dict[self.standard_metadata_group_name]

    @property
    def product_metadata(self) -> dict:
        return self.metadata_dict[self.product_metadata_group_name]

    @property
    def water(self) -> Raster:
        return self.variable("water")

    @classmethod
    def generate_granule_name(
            cls,
            orbit: int,
            scene: int,
            tile: str,
            time_UTC: Union[datetime, str],
            process_count: int,
            collection: str = "003"):
        product_name = cls._PRODUCT_NAME
        if product_name is None:
            raise ValueError("invalid product name")

        if orbit is None:
            raise ValueError("invalid orbit")

        if scene is None:
            raise ValueError("invalid scene")

        if tile is None:
            raise ValueError("invalid tile")

        if time_UTC is None:
            raise ValueError("invalid time")

        if process_count is None:
            raise ValueError("invalid process count")

        if isinstance(time_UTC, str):
            time_UTC = parser.parse(time_UTC)

        granule_name = f"ECOv{collection}_{product_name}_{orbit:05d}_{scene:03d}_{tile}_{time_UTC:%Y%m%dT%H%M%S}_{process_count:02d}"

        return granule_name

    def add_layer(
            self,
            variable_name: str,
            image: Raster,
            cmap: Union[Colormap, str] = None,
            include_COG: bool = True,
            include_geojpeg: bool = True) -> str:
        if cmap is None:
            cmap = "jet"

        if isinstance(cmap, str):
            cmap = get_cmap(cmap)

        # print("add_layer")
        filename_base = self.layer_filename(variable_name)
        filename = join(self.product_location, filename_base)
        # print(f"filename: {filename}")
        logger.info(f"adding {cl.name(self.product)} layer {cl.name(variable_name)} min: {cl.val(np.nanmin(image))} mean: {cl.val(np.nanmean(image))} max: {cl.val(np.nanmax(image))} cmap: {cl.name(cmap.name)} file: {cl.file(filename)}")

        preview_filename = filename.replace(".tif", ".jpeg")

        if include_COG:
            image.to_COG(
                filename=filename,
                compress=self.compression,
                preview_filename=preview_filename,
                preview_quality=self.layer_preview_quality,
                cmap=cmap
            )

        if include_COG:
            return filename

        if include_geojpeg:
            return preview_filename

    def write_metadata(self, metadata_dict: dict, indent=DEFAULT_JSON_INDENT):
        filename = self.metadata_filename
        JSON_text = json.dumps(metadata_dict, indent=indent)

        with open(filename, "w") as file:
            file.write(JSON_text)

    @property
    def storage(self):
        return os.stat(self.product_filename).st_size

    def write_zip(self, zip_filename: str):
        product_directory = self.product_directory
        logger.info(f"writing product zip file: {cl.file(product_directory)} -> {cl.file(zip_filename)}")

        directory_name = splitext(basename(zip_filename))[0]

        with zipfile.ZipFile(zip_filename, "w") as zip_file:
            for filename in glob(join(product_directory, "*")):
                arcname = join(directory_name, basename(filename))
                zip_file.write(
                    filename=filename,
                    arcname=arcname
                )

        XML_metadata_filename = zip_filename.replace(".zip", ".zip.xml")
        logger.info(f"writing XML metadata file: {cl.file(XML_metadata_filename)}")
        write_XML_metadata(self.standard_metadata, XML_metadata_filename)

        # TODO should be zip-file validator

        if not exists(zip_filename):
            raise IOError(f"unable to create tiled product zip: {zip_filename}")

    # @classmethod
    # def from_scene(
    #         cls,
    #         gridded_granule: ECOSTRESSGriddedGranule,
    #         tile: str,
    #         tile_granule_directory: str = None,
    #         tile_granule_name: str = None,
    #         geometry: RasterGeometry = None,
    #         variables: List[str] = None,
    #         compression: str = None,
    #         overwrite: bool = False,
    #         skip_blank: bool = True) -> ECOSTRESSTiledGranule or None:
    #     if compression is None:
    #         compression = cls._COMPRESSION
    #
    #     if tile_granule_name is None:
    #         tile_granule_name = gridded_granule.tile_granule_name(tile)
    #
    #     if tile_granule_directory is None:
    #         tile_granule_directory = tile_granule_name
    #
    #     logger.info(
    #         f"target granule directory: {cl.dir(tile_granule_directory)}"
    #     )
    #
    #     metadata = gridded_granule.metadata_dict
    #     metadata["StandardMetadata"]["LocalGranuleID"] = f"{tile_granule_name}.zip"
    #
    #     orbit = gridded_granule.orbit
    #     scene = gridded_granule.scene
    #     time_UTC = gridded_granule.time_UTC
    #     build = gridded_granule.build
    #     process_count = gridded_granule.process_count
    #
    #     granule = cls(
    #         product_location=tile_granule_directory,
    #         orbit=orbit,
    #         scene=scene,
    #         tile=tile,
    #         time_UTC=time_UTC,
    #         build=build,
    #         process_count=process_count,
    #         compression=compression
    #     )
    #
    #     granule.write_metadata(metadata)
    #
    #     if variables is None:
    #         output_variables = gridded_granule.tiled_output_variables
    #     else:
    #         output_variables = variables
    #
    #     for j, variable in enumerate(output_variables):
    #         logger.info(f"processing variable: {variable}")
    #         output_filename = join(tile_granule_directory, f"{tile_granule_name}_{variable}.tif")
    #
    #         if exists(output_filename) and not overwrite:
    #             logger.warning(f"file already exists: {cl.file(output_filename)}")
    #             continue
    #
    #         logger.info(
    #             f"started processing variable {variable} ({j + 1} / {len(output_variables)}) "
    #             f"for granule: {tile_granule_name}"
    #         )
    #
    #
    #         image = gridded_granule.variable(
    #             variable,
    #             apply_scale=True,
    #             apply_cloud=True,
    #             geometry=geometry
    #         )
    #
    #         if skip_blank and np.all(np.isnan(image)):
    #             raise BlankOutput(f"blank output for layer {variable} at tile {tile} at time {time_UTC}")
    #
    #         granule.add_layer(variable, image)
    #
    #         logger.info(
    #             f"finished processing variable {variable} ({j + 1} / {len(output_variables)}) "
    #             f"for granule: {tile_granule_name} "
    #             f"({cl.time(timer)})"
    #         )
    #
    #     return granule

    @classmethod
    def scan_directory(cls, directory: str) -> List[ECOSTRESSTiledGranule]:
        filenames = glob(join(directory, "*"))
        filenames = filter(lambda filename: splitext(basename(filename))[0].split("_")[1].endswith("T"), filenames)

        granules = []

        for filename in filenames:
            try:
                granule = cls(filename)
                granules.append(granule)
            except:
                continue

        return granules

    @property
    def geometry(self) -> RasterGrid:
        if self._geometry is not None:
            return self._geometry

        URI = self.layer_URI(self.primary_variable)
        grid = RasterGrid.open(URI)

        return grid

    @property
    def boundary(self) -> Polygon:
        return self.geometry.boundary

    @property
    def orbit(self) -> int:
        if self._orbit is not None:
            return self._orbit
        else:
            return int(self.granule_name.split('_')[-5])

    @property
    def scene(self) -> int:
        if self._scene is not None:
            return self._scene
        else:
            return int(self.granule_name.split('_')[-4])

    @property
    def tile(self) -> str:
        if self._tile is not None:
            return self._tile
        else:
            return self.granule_name.split('_')[-3]

    @property
    def time_UTC(self) -> datetime:
        if self._time_UTC is not None:
            return self._time_UTC
        else:
            return parser.parse(self.granule_name.split('_')[-2])

    def UTC_to_solar(self, time_UTC: datetime, lon: float) -> datetime:
        return time_UTC + timedelta(hours=(np.radians(lon) / np.pi * 12))

    @property
    def time_solar(self) -> datetime:
        if self._time_solar is not None:
            return self._time_solar
        else:
            return self.UTC_to_solar(self.time_UTC, self.geometry.centroid_latlon.x)

    @property
    def hour_of_day(self) -> float:
        return self.time_solar.hour + self.time_solar.minute / 60

    @property
    def build(self) -> str:
        if self._build is not None:
            return self._build
        else:
            return self.standard_metadata["BuildID"]

    @property
    def process_count(self) -> int:
        if self._process_count is not None:
            return self._process_count
        else:
            return int(self.granule_name.split('_')[-1])

    @property
    def product(self) -> str:
        return "_".join(self.granule_name.split("_")[1:-5])

    @property
    def granule_name(self) -> str:
        if self._granule_name is not None:
            return self._granule_name
        else:
            return self.generate_granule_name(
                product_name=self.product,
                orbit=self.orbit,
                scene=self.scene,
                tile=self.tile,
                time_UTC=self.time_UTC,
                process_count=self.process_count
            )

    @property
    def filenames(self) -> List[str]:
        if self.is_zip:
            try:
                with zipfile.ZipFile(self.product_filename) as zip_file:
                    return sorted(
                        posixpath.basename(filename.rstrip("/"))
                        for filename in zip_file.namelist()
                        if not filename.endswith("/")
                    )
            except zipfile.BadZipFile as error:
                raise ValueError(f"invalid granule ZIP archive: {self.product_filename}") from error

        return [
            filename
            for filename in sorted(os.listdir(self.product_location))
            if os.path.isfile(join(self.product_location, filename))
        ]

    @property
    def layer_filenames(self) -> List[str]:
        return [
            filename
            for filename
            in self.filenames
            if filename.endswith(".tif")
        ]

    def URI_for_filename(self, filename: str) -> str:
        filename = posixpath.basename(filename)
        return f"zip://{abspath(expanduser(self.product_filename))}!/{self.granule_name}/{filename}"

    @property
    def layer_URIs(self) -> List[str]:
        return [
            join(self.product_location, filename)
            if not self.is_zip
            else self.URI_for_filename(filename)
            for filename
            in self.layer_filenames
        ]

    @property
    def variables(self) -> List[str]:
        return [
            str(splitext(basename(filename))[0].split("_")[-1])
            for filename
            in self.filenames
            if filename.endswith(".tif")
        ]

    def layer_filename(self, variable: str) -> Optional[str]:
        if not isinstance(variable, str):
            raise ValueError("invalid variable")

        return f"{self.granule_name}_{variable}.tif"

    @property
    def is_zip(self) -> bool:
        return self.product_location.lower().endswith(".zip")

    def layer_URI(self, variable: str) -> Optional[str]:
        # return join(self.product_directory, f"{self.granule_name}_{variable}.tif")

        layer_filename = self.layer_filename(variable)

        if layer_filename is None:
            return None

        if self.is_zip:
            URI = self.URI_for_filename(layer_filename)
        else:
            URI = join(self.product_location, layer_filename)

        return URI

    def variable(self, variable: str, geometry: RasterGeometry = None, cmap=None, **kwargs) -> Raster:
        URI = self.layer_URI(variable)
        logger.info(f"started reading {self.product} {variable}: {cl.URL(URI)}")
        start_time = perf_counter()
        image = Raster.open(URI)

        if geometry is not None:
            logger.info(f"projecting {self.product} {variable}")
            image = image.to_geometry(geometry, **kwargs)

        end_time = perf_counter()
        duration = end_time - start_time
        logger.info(f"finished reading {self.product} {variable} ({duration:0.2f}s)")

        if cmap is None and cmap in self.VARIABLE_CMAPS:
            cmap = self.VARIABLE_CMAPS[variable]

        if cmap is not None:
            print(f"assigning cmap: {cmap}")
            image.cmap = cmap

        if "float" in str(image.dtype):
            image.nodata = np.nan

        return image

    @classmethod
    def mosaic(cls, variable: str, granules: List[ECOSTRESSTiledGranule], geometry: RasterGeometry):
        return rasters.mosaic((granule.variable(variable) for granule in granules), geometry)
