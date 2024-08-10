#! /bin/bash

cd $(dirname $0)
cd ../..

python -m pytest --cov=src tests/ --cov-report=html