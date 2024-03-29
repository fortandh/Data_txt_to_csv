#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 这个文件的主要目标是将log_to_csv.py生成的rslt.csv文件内的hybrid行，pp行，以及sc行提取出来
# 然后分到三个文件里面，便于static_average.py处理

import re

input_csv_file_name = "rslt.csv"
hybrid_csv_file_name = "hybrid.csv"
pp_csv_file_name = "pp.csv"
sc_csv_file_name = "sc.csv"

if __name__ == '__main__':
    with open(input_csv_file_name, "r") as input_csv_file, \
            open(hybrid_csv_file_name, "w") as output_hybrid_file, \
            open(pp_csv_file_name, "w") as output_pp_file, \
            open(sc_csv_file_name, "w") as output_sc_file:
        output_hybrid_file.write(",Length,PR,PR_known,turn off camera,Intrusion,Intrusion_known,replan times,"
                                 "No solution times,flag 1 times,flag 2 times,flag 3 times,exploration rate,"
                                 "execution time\n")
        output_sc_file.write(",Length,PR,PR_known,turn off camera,Intrusion,Intrusion_known,"
                             "replan times,exploration rate,execution time,,,,\n")
        output_pp_file.write(",Length,PR,PR_known,turn off camera,Intrusion,Intrusion_known,replan times,"
                             "No solution times,flag 1 times,flag 2 times,flag 3 times,exploration rate,"
                             "execution time\n")
        for line in input_csv_file:
            # 处理Hybrid行
            pattern = re.compile(r'Hybrid.*')
            result = pattern.findall(line)
            if result:
                result = result[0]
                # print(result)
                output_hybrid_file.write(result+'\n')

            # 处理pp行
            pattern = re.compile(r'PP.*')
            result = pattern.findall(line)
            if result:
                result = result[0]
                # print(result)
                output_pp_file.write(result+'\n')

            # 处理sc行
            pattern = re.compile(r'SC.*')
            result = pattern.findall(line)
            if result:
                result = result[0]
                # print(result)
                output_sc_file.write(result+'\n')

        print("csv parser process finished.")
