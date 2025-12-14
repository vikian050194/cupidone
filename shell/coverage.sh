#!/bin/env bash

coverage run -m unittest discover -t=${workspaceFolder} -s=tests -p=test_*.py -v
coverage html