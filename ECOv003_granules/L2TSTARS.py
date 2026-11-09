from datetime import datetime
from typing import Union

from dateutil import parser

from .colors import *
from .granule import ECOSTRESSGranule
from .tiled_granule import ECOSTRESSTiledGranule

PRIMARY_VARIABLE = "NDVI"
PREVIEW_CMAP = NDVI_COLORMAP

VARIABLE_CMAPS = {
    "NDVI": NDVI_COLORMAP,
    "NDVI-UQ": "jet",
    "NDVI-bias": "viridis",
    "NDVI-bias-UQ": "viridis",
    "albedo": ALBEDO_COLORMAP,
    "albedo-UQ": "jet",
    "albedo-bias": "viridis",
    "albedo-bias-UQ": "viridis",
}

class L2STARSGranule(ECOSTRESSGranule):
    _PRODUCT_NAME = "L2T_STARS"
    _PRIMARY_VARIABLE = "NDVI"
    _GRANULE_PREVIEW_CMAP = PREVIEW_CMAP

    VARIABLE_CMAPS = VARIABLE_CMAPS

    def __init__(self, product_filename: str):
        super(L2STARSGranule, self).__init__(product_filename=product_filename)

        self._NDVI = None
        self._NDVI_UQ = None
        self._NDVI_bias = None
        self._NDVI_bias_UQ = None
        self._albedo = None
        self._albedo_UQ = None
        self._albedo_bias = None
        self._albedo_bias_UQ = None

    @property
    def NDVI(self):
        if self._NDVI is None:
            self._NDVI = self.variable("NDVI")
            self._NDVI.cmap = NDVI_COLORMAP

        return self._NDVI

    @property
    def NDVI_UQ(self):
        if self._NDVI_UQ is None:
            self._NDVI_UQ = self.variable("NDVI-UQ")

        return self._NDVI_UQ

    @property
    def NDVI_bias(self):
        if self._NDVI_bias is None:
            self._NDVI_bias = self.variable("NDVI-bias")

        return self._NDVI_bias

    @property
    def NDVI_bias_UQ(self):
        if self._NDVI_bias_UQ is None:
            self._NDVI_bias_UQ = self.variable("NDVI-bias-UQ")

        return self._NDVI_bias_UQ

    @property
    def albedo(self):
        if self._albedo is None:
            self._albedo = self.variable("albedo")
            self._albedo.cmap = ALBEDO_COLORMAP

        return self._albedo

    @property
    def albedo_UQ(self):
        if self._albedo_UQ is None:
            self._albedo_UQ = self.variable("albedo-UQ")

        return self._albedo_UQ

    @property
    def albedo_bias(self):
        if self._albedo_bias is None:
            self._albedo_bias = self.variable("albedo-bias")

        return self._albedo_bias

    @property
    def albedo_bias_UQ(self):
        if self._albedo_bias_UQ is None:
            self._albedo_bias_UQ = self.variable("albedo-bias-UQ")

        return self._albedo_bias_UQ

    @property
    def orbit(self):
        return None

    @property
    def scene(self):
        return None


class L2TSTARS(ECOSTRESSTiledGranule, L2STARSGranule):
    _PRODUCT_NAME = "L2T_STARS"
    _PRIMARY_VARIABLE = PRIMARY_VARIABLE
    _GRANULE_PREVIEW_CMAP = PREVIEW_CMAP

    VARIABLE_CMAPS = VARIABLE_CMAPS

    @property
    def product(self) -> str:
        return self._PRODUCT_NAME

    def __init__(
            self,
            product_location: str = None,
            orbit: int = None,
            scene: int = None,
            tile: str = None,
            time_UTC: Union[datetime, str] = None,
            build: str = None,
            process_count: int = None,
            containing_directory: str = None):
        L2STARSGranule.__init__(self, product_filename=product_location)

        ECOSTRESSTiledGranule.__init__(
            self,
            orbit=orbit,
            scene=scene,
            tile=tile,
            time_UTC=time_UTC,
            build=build,
            process_count=process_count,
            product_location=product_location,
            containing_directory=containing_directory
        )

    @property
    def orbit(self):
        return None

    @property
    def scene(self):
        return None

    @classmethod
    def generate_granule_name(
            cls,
            orbit: int,
            scene: int,
            tile: str,
            time_UTC: Union[datetime, str],
            process_count: int,
            collection = "003"):
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

        granule_name = f"ECOv{collection}_{product_name}_{tile}_{time_UTC:%Y%m%d}_{process_count:02d}"

        return granule_name
