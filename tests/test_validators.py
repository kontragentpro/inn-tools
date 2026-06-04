import pytest

from inn_tools import (
    validate,
    validate_inn,
    validate_inn_fl,
    validate_inn_ul,
    validate_kpp,
    validate_ogrn,
    validate_ogrnip,
    validate_snils,
)


@pytest.mark.parametrize("inn", ["7707083893", "7 707 083 893", "7736207543"])
def test_inn_ul_valid(inn):
    assert validate_inn_ul(inn)
    assert validate_inn(inn)


@pytest.mark.parametrize("inn", ["7707083894", "770708389", "abcdefghij", ""])
def test_inn_ul_invalid(inn):
    assert not validate_inn_ul(inn)


@pytest.mark.parametrize("inn", ["772852855194", "500100732259"])
def test_inn_fl_valid(inn):
    assert validate_inn_fl(inn)
    assert validate_inn(inn)


@pytest.mark.parametrize("inn", ["772852855195", "500100732250"])
def test_inn_fl_invalid(inn):
    assert not validate_inn_fl(inn)


@pytest.mark.parametrize("ogrn", ["1027700132195", "1 027 700 132 195"])
def test_ogrn_valid(ogrn):
    assert validate_ogrn(ogrn)


@pytest.mark.parametrize("ogrn", ["1027700132194", "102770013219"])
def test_ogrn_invalid(ogrn):
    assert not validate_ogrn(ogrn)


def test_ogrnip_valid():
    assert validate_ogrnip("304500116000157")


def test_ogrnip_invalid():
    assert not validate_ogrnip("304500116000158")


@pytest.mark.parametrize("kpp", ["770701001", "7707AB001"])
def test_kpp_valid(kpp):
    assert validate_kpp(kpp)


@pytest.mark.parametrize("kpp", ["77070100", "770701ABC", "12345678"])
def test_kpp_invalid(kpp):
    assert not validate_kpp(kpp)


def test_kpp_lowercase_letters_normalized():
    # latin letters in positions 5-6 are valid and get upper-cased
    assert validate_kpp("7707ab001")


@pytest.mark.parametrize("snils", ["11223344595", "112-233-445 95"])
def test_snils_valid(snils):
    assert validate_snils(snils)


def test_snils_invalid():
    assert not validate_snils("11223344596")


def test_dispatch_guess_by_length():
    assert validate("7707083893")            # INN UL
    assert validate("1027700132195")         # OGRN
    assert not validate("123")               # unknown length


def test_dispatch_explicit_kind():
    assert validate("770701001", kind="kpp")
    with pytest.raises(ValueError):
        validate("770701001", kind="bogus")
