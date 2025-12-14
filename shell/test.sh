#!/bin/env bash

python -m unittest discover -t=${workspaceFolder} -s=tests -p=test_*.py -v