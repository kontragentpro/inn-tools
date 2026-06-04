"""inn-tools — validation and lookup utilities for Russian business IDs.

Quick start::

    from inn_tools import validate_inn, region_name

    validate_inn("7707083893")   # -> True  (Сбербанк)
    region_name("7707083893")    # -> "город Москва"
"""

from __future__ import annotations

from .region import REGIONS, region_code, region_name
from .validators import (
    clean,
    validate,
    validate_inn,
    validate_inn_fl,
    validate_inn_ul,
    validate_kpp,
    validate_ogrn,
    validate_ogrnip,
    validate_snils,
)

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "clean",
    "validate",
    "validate_inn",
    "validate_inn_ul",
    "validate_inn_fl",
    "validate_ogrn",
    "validate_ogrnip",
    "validate_kpp",
    "validate_snils",
    "REGIONS",
    "region_code",
    "region_name",
]

