#!/usr/bin/env python

import earthaccess

from query_functions import download_results, query_files

results, folder_name = query_files()
# print(results[0], len(results))

download_results(results, folder_name)
