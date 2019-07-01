#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

if __name__ == '__main__':
    file_name_list = ["rslt.csv",
                      "hybrid.csv", "pp.csv", "sc.csv",
                      "hybrid_average.csv", "pp_average.csv", "sc_average.csv"]
    for file_name in file_name_list:
        if os.path.exists(file_name):
            os.remove(file_name)
            print("{} has been removed.".format(file_name))
    print("All work has been finished.")

