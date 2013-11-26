#!/bin/bash
#
# Copyright 2012 Google Inc. All Rights Reserved.
# Author: kwinter@google.com (Kevin Winter)
#
# Runs both bug "unit" tests as well integration tests.
# Expects pickles to work.

BASE_DIR=$1
LIB=$2
MAX_VER=$3
BUGS_DIR="tests/adspygoogle/$LIB/bugs"
INTEGRATION_TEST_DIR="tests/adspygoogle/$LIB/$MAX_VER/"

# Move into base release directory.
pushd $BASE_DIR

# Move into and test all integration tests.
pushd $INTEGRATION_TEST_DIR
python alltests.py
popd

# If we have a bugs dir, run those to.
if [ -d $BUGS_DIR ]; then
  pushd $BUGS_DIR
  python alltests.py
  popd
fi

# Final pop.
popd
