"""Checksum validators for Russian business and personal identifiers.

Supported identifiers:

* ``INN``    — Taxpayer Identification Number (10 digits for legal entities,
               12 digits for individuals / sole proprietors).
* ``OGRN``   — Primary State Registration Number of a legal entity (13 digits).
* ``OGRNIP`` — Primary State Registration Number of a sole proprietor (15 digits).
* ``KPP``    — Tax Registration Reason Code (9 chars, no checksum, format only).
* ``SNILS``  — Individual Insurance Account Number (11 digits).

All control-digit algorithms follow the official specifications published by
the Federal Tax Service of Russia (ФНС) and the Pension Fund (СФР/ПФР).
"""

from __future__ import annotations

import re

__all__ = [
    "clean",
    "validate_inn",
    "validate_inn_ul",
    "validate_inn_fl",
    "validate_ogrn",
    "validate_ogrnip",
    "validate_kpp",
    "validate_snils",
    "validate",
]

# Control-digit weight vectors, taken verbatim from the ФНС specification.
_INN_WEIGHTS_11 = (7, 2, 4, 10, 3, 5, 9, 4, 6, 8)
_INN_WEIGHTS_12 = (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8)

_KPP_RE = re.compile(r"^[0-9]{4}[0-9A-Z]{2}[0-9]{3}$")


def clean(value: str | int) -> str:
    """Strip spaces and non-digit separators, returning a bare digit string.

    Letters are kept (KPP may legally contain ``A``–``Z`` in positions 5–6),
    everything else (spaces, dashes, dots) is removed.
    """
    return re.sub(r"[^0-9A-Za-z]", "", str(value)).upper()


def _control(digits: str, weights: tuple[int, ...]) -> int:
    """Return ``(sum(d_i * w_i) mod 11) mod 10`` for the given weights."""
    total = sum(int(d) * w for d, w in zip(digits, weights))
    return total % 11 % 10


def validate_inn_ul(inn: str | int) -> bool:
    """Validate a 10-digit INN of a legal entity (юридическое лицо)."""
    inn = clean(inn)
    if len(inn) != 10 or not inn.isdigit():
        return False
    return _control(inn, _INN_WEIGHTS_11[1:]) == int(inn[9])


def validate_inn_fl(inn: str | int) -> bool:
    """Validate a 12-digit INN of an individual or sole proprietor."""
    inn = clean(inn)
    if len(inn) != 12 or not inn.isdigit():
        return False
    n11 = _control(inn[:10], _INN_WEIGHTS_11)
    n12 = _control(inn[:11], _INN_WEIGHTS_12)
    return n11 == int(inn[10]) and n12 == int(inn[11])


def validate_inn(inn: str | int) -> bool:
    """Validate an INN of either length (10 or 12 digits)."""
    inn = clean(inn)
    if len(inn) == 10:
        return validate_inn_ul(inn)
    if len(inn) == 12:
        return validate_inn_fl(inn)
    return False


def validate_ogrn(ogrn: str | int) -> bool:
    """Validate a 13-digit OGRN of a legal entity.

    Control digit = ``(first 12 digits as int) mod 11``, then ``mod 10``.
    """
    ogrn = clean(ogrn)
    if len(ogrn) != 13 or not ogrn.isdigit():
        return False
    control = int(ogrn[:12]) % 11 % 10
    return control == int(ogrn[12])


def validate_ogrnip(ogrnip: str | int) -> bool:
    """Validate a 15-digit OGRNIP of a sole proprietor.

    Control digit = ``(first 14 digits as int) mod 13``, then ``mod 10``.
    """
    ogrnip = clean(ogrnip)
    if len(ogrnip) != 15 or not ogrnip.isdigit():
        return False
    control = int(ogrnip[:14]) % 13 % 10
    return control == int(ogrnip[14])


def validate_kpp(kpp: str | int) -> bool:
    """Validate KPP format (9 chars; positions 5–6 may be ``A``–``Z``).

    KPP carries no checksum, so only the structural format is checked.
    """
    return bool(_KPP_RE.match(clean(kpp)))


def validate_snils(snils: str | int) -> bool:
    """Validate an 11-digit SNILS, including its 2-digit control code."""
    snils = clean(snils)
    if len(snils) != 11 or not snils.isdigit():
        return False
    body, control = snils[:9], int(snils[9:])
    total = sum(int(d) * (9 - i) for i, d in enumerate(body))
    if total < 100:
        expected = total
    elif total in (100, 101):
        expected = 0
    else:
        expected = total % 101
        if expected == 100:
            expected = 0
    return expected == control


# Dispatcher --------------------------------------------------------------

_VALIDATORS = {
    "inn": validate_inn,
    "inn_ul": validate_inn_ul,
    "inn_fl": validate_inn_fl,
    "ogrn": validate_ogrn,
    "ogrnip": validate_ogrnip,
    "kpp": validate_kpp,
    "snils": validate_snils,
}


def validate(value: str | int, kind: str | None = None) -> bool:
    """Validate ``value`` as the given ``kind``.

    If ``kind`` is omitted, the identifier type is guessed from its length
    (10/12 → INN, 13 → OGRN, 15 → OGRNIP, 11 → SNILS). KPP cannot be guessed
    because it overlaps with the 9-char space and must be requested explicitly.
    """
    if kind is not None:
        try:
            return _VALIDATORS[kind](value)
        except KeyError as exc:
            raise ValueError(f"unknown identifier kind: {kind!r}") from exc

    digits = clean(value)
    guess = {10: validate_inn, 12: validate_inn, 13: validate_ogrn,
             15: validate_ogrnip, 11: validate_snils}.get(len(digits))
    return guess(value) if guess else False

