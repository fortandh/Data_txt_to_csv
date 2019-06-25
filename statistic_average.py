#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 这个文件的主要目标是将csv_parser.py 分开的三个文件hybrid.csv, pp.csv, sc.csv 分别进行平均数统计
# 结果分别存入hybrid_average,csv pp_average.csv, sc_average.csv中

import re

from Support.record import Record

input_hybrid_file_name = "hybrid.csv"
output_hybrid_file_name = "hybrid_average.csv"

input_pp_file_name = "pp.csv"
output_pp_file_name = "pp_average.csv"

input_sc_file_name = "sc.csv"
output_sc_file_name = "sc_average.csv"

group_size = 10


def average(input_file_name, output_file_name):
    with open(input_file_name, "r") as input_file, \
            open(output_file_name, "w") as output_file:
        record_list = []
        # print(",Length,PR,turn off camera,Intrudsion,replan times,exploration rate")
        output_file.write(",Length,PR,turn off camera,Intrudsion,replan times,exploration rate\n")
        for line in input_file:
            # 匹配如下内容：
            # Hybrid,37,0.025378,21,26,5,0.190000,,,,,
            pattern = re.compile(r'.*,(\d+),(\d+.\d+),(\d+),(\d+),(\d+),(\d+.\d+).*')
            result = pattern.findall(line)
            if result:
                result = result[0]
                tmp_record = Record(int(result[0]), float(result[1]), int(result[2]), int(result[3]),
                                    int(result[4]), float(result[5]))
                record_list.append(tmp_record)

                if len(record_list) == group_size:
                    length_average = 0
                    PR_average = 0
                    times_of_turning_off_camera_average = 0
                    times_of_intrusion_average = 0
                    times_of_replanning_average = 0
                    exploration_rate_average = 0

                    for i in range(len(record_list)):
                        length_average += record_list[i].length
                        PR_average += record_list[i].PR
                        times_of_turning_off_camera_average += record_list[i].times_of_turning_off_camera
                        times_of_intrusion_average += record_list[i].times_of_intrusion
                        times_of_replanning_average += record_list[i].times_of_replanning
                        exploration_rate_average += record_list[i].exploration_rate

                    length_average /= group_size
                    PR_average /= group_size
                    times_of_turning_off_camera_average /= group_size
                    times_of_intrusion_average /= group_size
                    times_of_replanning_average /= group_size
                    exploration_rate_average /= group_size

                    # print("Average,{},{},{},{},{}.{}".format(length_average, PR_average,
                    #                                          times_of_turning_off_camera_average,
                    #                                          times_of_intrusion_average,
                    #                                          times_of_replanning_average,
                    #                                          exploration_rate_average))
                    output_file.write("Average,{},{},"
                                      "{},{},{},{}\n".format(length_average, PR_average,
                                                             times_of_turning_off_camera_average,
                                                             times_of_intrusion_average,
                                                             times_of_replanning_average,
                                                             exploration_rate_average))
                    record_list = []


if __name__ == '__main__':
    print("Hybrid processing...")
    average(input_hybrid_file_name, output_hybrid_file_name)
    print("Hybrid finished.")

    print("PP processing...")
    average(input_pp_file_name, output_pp_file_name)
    print("PP finished.")

    print("SC processing...")
    average(input_sc_file_name, output_sc_file_name)
    print("SC finished.")
