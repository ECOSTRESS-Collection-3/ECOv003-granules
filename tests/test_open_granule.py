from importlib import import_module

import pytest


open_granule_module = import_module("ECOv003_granules.open_granule")


@pytest.mark.parametrize(
    ("product", "class_name"),
    [
        ("L1CT_RAD", "L1CTRAD"),
        ("L2T_LSTE", "L2TLSTE"),
        ("L2T_STARS", "L2TSTARS"),
        ("L3T_ETAUX", "L3TETAUX"),
        ("L3T_JET", "L3TJET"),
        ("L3T_MET", "L3TMET"),
        ("L3T_SM", "L3TSM"),
        ("L3T_SEB", "L3TSEB"),
        ("L4T_ESI", "L4TESI"),
        ("L4T_WUE", "L4TWUE"),
    ],
)
def test_open_granule_dispatches_collection_3_products(tmp_path, monkeypatch, product, class_name):
    granule_path = tmp_path / f"ECOv003_{product}_fixture"
    granule_path.mkdir()
    constructor_call = (product, str(granule_path))

    def constructor(filename, **kwargs):
        return constructor_call, kwargs

    monkeypatch.setattr(open_granule_module, class_name, constructor)

    result = open_granule_module.open_granule(str(granule_path), option="value")

    assert result == (constructor_call, {"option": "value"})


def test_open_granule_rejects_unsupported_product(tmp_path):
    with pytest.raises(ValueError, match="unsupported granule product"):
        open_granule_module.open_granule(str(tmp_path / "unknown_product"))


def test_open_granule_rejects_missing_product_path(tmp_path):
    with pytest.raises(FileNotFoundError, match="granule does not exist"):
        open_granule_module.open_granule(str(tmp_path / "ECOv003_L3T_ETAUX_missing"))


def test_open_granule_rejects_non_granule_file(tmp_path):
    granule_path = tmp_path / "ECOv003_L3T_ETAUX_layer.tif"
    granule_path.touch()

    with pytest.raises(ValueError, match="directory or ZIP archive"):
        open_granule_module.open_granule(str(granule_path))


def test_open_granule_rejects_malformed_zip(tmp_path):
    granule_path = tmp_path / "ECOv003_L3T_ETAUX_invalid.zip"
    granule_path.write_text("not a ZIP archive")

    with pytest.raises(ValueError, match="invalid granule ZIP archive"):
        open_granule_module.open_granule(str(granule_path))
