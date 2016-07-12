#!/bin/bash

### Rename all filles maching the pattern all.* by including a prefix

prefix = "my"

for FILENAME in all.*; do mv -v $FILENAME ${prefix}_${FILENAME}; done