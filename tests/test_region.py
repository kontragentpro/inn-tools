import pytest

from inn_tools import region_code, region_name
from inn_tools.region import REGIONS


@pytest.mark.parametrize("inn,code,name", [
    ("7707083893", 77, "город Москва"),
    ("7841438000", 78, "город Санкт-Петербург"),
    ("0264063018", 2, "Республика Башкортостан"),
])
def test_region_lookup(inn, code, name):
    assert region_code(inn) == code
    assert region_name(inn) == name


def test_region_unknown_code():
    # code 00 is not a real federal subject
    assert region_name("0012345678") is None


def test_region_bad_length():
    assert region_code("123") is None
    assert region_name("123") is None


def test_regions_table_sane():
    assert REGIONS[77] == "город Москва"
    assert all(1 <= code <= 99 for code in REGIONS)

