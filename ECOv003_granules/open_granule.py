from os.path import basename, exists, isdir, isfile, splitext
import logging
import zipfile

import colored_logging as cl

from .granule import ECOSTRESSGranule
from .L1CTRAD import L1CTRAD
from .L2TLSTE import L2TLSTE
from .L2TSTARS import L2TSTARS
from .L3TETAUX import L3TETAUX
from .L3TJET import L3TJET
from .L3TMET import L3TMET
from .L3TSM import L3TSM
from .L3TSEB import L3TSEB
from .L4TESI import L4TESI
from .L4TWUE import L4TWUE

logger = logging.getLogger(__name__)

def open_granule(
        filename: str,
        L2_CLOUD_filename: str = None,
        L1B_GEO_filename: str = None,
        **kwargs) -> ECOSTRESSGranule:
    filename_base = splitext(basename(filename))[0]

    products = (
        ("ECOv003_L1CT_RAD", L1CTRAD, "L1CT RAD"),
        ("ECOv003_L1CT_RED", L1CTRAD, "L1CT RAD"),
        ("ECOv003_L2T_LSTE", L2TLSTE, "L2T LSTE"),
        ("ECOv003_L2T_STARS", L2TSTARS, "L2T STARS"),
        ("ECOv003_L3T_ETAUX", L3TETAUX, "L3T ETAUX"),
        ("ECOv003_L3T_JET", L3TJET, "L3T JET"),
        ("ECOv003_L3T_MET", L3TMET, "L3T MET"),
        ("ECOv003_L3T_SM", L3TSM, "L3T SM"),
        ("ECOv003_L3T_SEB", L3TSEB, "L3T SEB"),
        ("ECOv003_L4T_ESI", L4TESI, "L4T ESI"),
        ("ECOv003_L4T_WUE", L4TWUE, "L4T WUE"),
    )

    for product_prefix, granule_class, product_name in products:
        if filename_base.startswith(product_prefix):
            if not exists(filename):
                raise FileNotFoundError(f"granule does not exist: {filename}")

            if not isdir(filename):
                if not isfile(filename) or splitext(filename)[1].lower() != ".zip":
                    raise ValueError(f"granule path must be a directory or ZIP archive: {filename}")
                if not zipfile.is_zipfile(filename):
                    raise ValueError(f"invalid granule ZIP archive: {filename}")

            logger.info(f"loading Collection 3 {product_name}: {cl.file(filename)}")
            return granule_class(filename, **kwargs)

    raise ValueError(f"unsupported granule product: {filename_base}")