#!/usr/bin/env bash

rm -rf .venv/
python -m venv .venv
source .venv/bin/activate
pip install setuptools wheel build twine
rm -rf dist/
python -m build

