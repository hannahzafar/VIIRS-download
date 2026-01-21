#!/bin/bash
# Script to wrapper VIIRS download with command line inputs

# ./viirs_download.py -p VNP64A1 -v 002 -s 2025-01-01 -e 2025-01-01
./viirs_download.py -p VNP43IA4 -v 002 -s 2020-01-01 -e 2020-01-01

# Test a failure query
# ./viirs_download.py -p VNP64A1 -v 002 -s 2026-01-01 -e 2026-01-01
