import os
import zipfile

import pytest

from ECOv003_granules.L2TSTARS import L2TSTARS
from ECOv003_granules.L3TETAUX import L3TETAUX


def make_etaux_directory(tmp_path):
    granule_name = "ECOv003_L3T_ETAUX_00001_001_10TET_20260101T000000_01"
    granule_path = tmp_path / granule_name
    granule_path.mkdir()
    (granule_path / f"{granule_name}_Ta.tif").touch()
    (granule_path / f"{granule_name}_RH.tif").touch()
    return granule_name, granule_path


def test_directory_granule_discovers_tiff_layers(tmp_path):
    granule_name, granule_path = make_etaux_directory(tmp_path)
    granule = L3TETAUX(str(granule_path))

    assert granule.filenames == [f"{granule_name}_RH.tif", f"{granule_name}_Ta.tif"]
    assert granule.layer_filenames == granule.filenames
    assert granule.variables == ["RH", "Ta"]
    assert granule.layer_URIs == [
        os.path.join(str(granule_path), f"{granule_name}_RH.tif"),
        os.path.join(str(granule_path), f"{granule_name}_Ta.tif"),
    ]


def test_zip_granule_discovers_same_tiff_layers_as_directory(tmp_path):
    granule_name, granule_path = make_etaux_directory(tmp_path)
    zip_path = tmp_path / f"{granule_name}.zip"

    with zipfile.ZipFile(zip_path, "w") as archive:
        for filename in granule_path.iterdir():
            archive.write(filename, f"{granule_name}/{filename.name}")

    granule = L3TETAUX(str(zip_path))

    assert granule.filenames == [f"{granule_name}_RH.tif", f"{granule_name}_Ta.tif"]
    assert granule.layer_filenames == granule.filenames
    assert granule.variables == ["RH", "Ta"]
    assert granule.layer_URIs == [
        granule.URI_for_filename(f"{granule_name}_RH.tif"),
        granule.URI_for_filename(f"{granule_name}_Ta.tif"),
    ]


def test_empty_directory_has_no_layers(tmp_path):
    granule_path = tmp_path / "ECOv003_L3T_ETAUX_empty"
    granule_path.mkdir()

    granule = L3TETAUX(str(granule_path))

    assert granule.layer_filenames == []
    assert granule.variables == []


def test_malformed_zip_raises_clear_error(tmp_path):
    zip_path = tmp_path / "ECOv003_L3T_ETAUX_invalid.zip"
    zip_path.write_text("not a ZIP archive")
    granule = L3TETAUX(str(zip_path))

    with pytest.raises(ValueError, match="invalid granule ZIP archive"):
        _ = granule.filenames


def test_stars_product_is_canonical(tmp_path):
    granule_path = tmp_path / "ECOv003_L2T_STARS_10TET_20260101_01"
    granule_path.mkdir()

    assert L2TSTARS(str(granule_path)).product == "L2T_STARS"


def test_etaUX_relative_humidity_uses_its_own_layer(tmp_path, monkeypatch):
    granule_path = tmp_path / "ECOv003_L3T_ETAUX_test"
    granule_path.mkdir()
    granule = L3TETAUX(str(granule_path))
    monkeypatch.setattr(granule, "variable", lambda variable: variable)

    assert granule.RH == "RH"
    assert granule.Rg == "Rg"
