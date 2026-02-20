# compound-demo

## Project Overview
Simple Python validation library. Demo project for Compound Engineering workflow.

## Stack
- Python 3, stdlib only (no external dependencies)
- Tests with `unittest` (built-in)

## Commands
- Run tests: `python -m pytest tests.py` or `python tests.py`

## Conventions
- Each validator is a function that returns `(bool, str)` — valid/invalid + reason
- Tests live in `tests.py`
