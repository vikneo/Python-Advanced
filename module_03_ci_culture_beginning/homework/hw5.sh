#!/usr/bin/bash

path="tests/test_hw2.py"
find "../" -iname $path -exec cp {} . \;

pylint $path --reports=y --output-format=json --output=out.json
pylint_res=$?

if [ $pylint_res -eq 0 ]; then
  echo 'Pylint OK'
else
  echo 'Pylint not OK'

python3 -m unittest

fi
