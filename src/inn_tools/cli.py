"""Command-line interface: ``python -m inn_tools <identifier> [...]``."""

from __future__ import annotations

import sys

from .region import region_code, region_name
from .validators import clean, validate


def _describe(value: str) -> str:
    digits = clean(value)
    n = len(digits)
    kinds = {10: "ИНН (ЮЛ)", 12: "ИНН (ФЛ/ИП)", 13: "ОГРН",
             15: "ОГРНИП", 11: "СНИЛС"}
    kind = kinds.get(n, f"неизвестный формат ({n} симв.)")
    ok = validate(value)
    mark = "OK " if ok else "FAIL"
    line = f"[{mark}] {value}  →  {kind}"
    if ok and n in (10, 12):
        line += f"  ·  регион {region_code(value)}: {region_name(value)}"
    return line


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print("usage: python -m inn_tools <ИНН|ОГРН|ОГРНИП|СНИЛС> [...]",
              file=sys.stderr)
        return 2
    all_ok = True
    for value in args:
        result = _describe(value)
        all_ok &= result.startswith("[OK ")
        print(result)
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
