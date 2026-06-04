# Changelog

## 0.1.0 — 2026-06-01

Первый релиз.

- Валидация ИНН (10/12), ОГРН (13), ОГРНИП (15), КПП (9), СНИЛС (11).
- Определение региона по ИНН (`region_code`, `region_name`).
- Универсальный диспетчер `validate(value, kind=None)`.
- CLI: `inn-tools <id> [...]` и `python -m inn_tools`.

