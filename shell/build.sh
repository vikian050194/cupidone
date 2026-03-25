#!/bin/env bash

source venv/bin/activate

PACKAGE_VERSION=$(python setup.py --version)

GREP_CHANGELOG=$(grep --fixed-strings -o "$PACKAGE_VERSION" CHANGELOG.md | wc -l)

if [ "$GREP_CHANGELOG" != 4 ]; then
    echo "update CHANGELOG: $PACKAGE_VERSION was found $GREP_CHANGELOG times instead of 4";
    exit -1;
fi

set -e

source shell/test.sh

rm -rf "dist"

python -m build -v