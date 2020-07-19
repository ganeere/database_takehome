#!/bin/bash

echo "remove tildas..."



perl -pi -e s,~,,g text/*.txt