#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 这个文件的主要目标是将 csv_parser.py 分开的三个文件中 sc.csv 进行平均数统计
# 结果存入 sc_average.csv 中

import re

from Support.record import Record

input_sc_file_name = "sc.csv"
output_sc_file_name = "sc_average.csv"

group_size = 10
# 程序工作模式，test代表测试，work代表实际运行
command_mode = "work"


if __name__ == '__main__':
    with open(input_sc_file_name, "r") as input_file, \
            open(output_sc_file_name, "w") as output_file:
        record_list = []
        if command_mode == "test":
            print(",Length,PR,PR_known,turn off camera,Intrusion,Intrusion_known,replan times,exploration rate,"
                  "execution time,,,,")
        else:
            output_file.write(",Length,PR,PR_known,turn off camera,Intrusion,Intrusion_known,"
                              "replan times,exploration rate,execution time,,,,\n")
        for line in input_file:
            # 匹配如下内容：
            # SC,27,33.800477,24.314833,8,18,16,4,0.200000,0,,,,
            pattern = re.compile(r'.*,(\d+),(\d+\.\d+),(\d+\.\d+),(\d+),(\d+),(\d+),(\d+),(\d+\.\d+),(\d+\.?\d*).*')
            result = pattern.findall(line)
            if result:
                result = result[0]
                tmp_record = Record(int(result[0]), float(result[1]), float(result[2]), int(result[3]), int(result[4]),
                                    int(result[5]), int(result[6]), float(result[7]), float(result[8]))
                record_list.append(tmp_record)

                if len(record_list) == group_size:
                    length_average = 0
                    PR_average = 0
                    PR_known_average = 0
                    times_of_turning_off_camera_average = 0
                    times_of_intrusion_average = 0
                    times_of_intrusion_known_average = 0
                    times_of_replanning_average = 0
                    exploration_rate_average = 0
                    execution_time_average = 0

                    for i in range(len(record_list)):
                        length_average += record_list[i].length
                        PR_average += record_list[i].PR
                        PR_known_average += record_list[i].PR_known
                        times_of_turning_off_camera_average += record_list[i].times_of_turning_off_camera
                        times_of_intrusion_average += record_list[i].times_of_intrusion
                        times_of_intrusion_known_average += record_list[i].times_of_intrusion_known
                        times_of_replanning_average += record_list[i].times_of_replanning
                        exploration_rate_average += record_list[i].exploration_rate
                        execution_time_average += record_list[i].execution_time

                    length_average /= group_size
                    PR_average /= group_size
                    PR_known_average /= group_size
                    times_of_turning_off_camera_average /= group_size
                    times_of_intrusion_average /= group_size
                    times_of_intrusion_known_average /= group_size
                    times_of_replanning_average /= group_size
                    exploration_rate_average /= group_size
                    execution_time_average /= group_size

                    if command_mode == "test":
                        print("Average,{},{},{},{},{},{},"
                              "{},{},{},,,,".format(length_average, PR_average, PR_known_average,
                                                    times_of_turning_off_camera_average,
                                                    times_of_intrusion_average, times_of_intrusion_known_average,
                                                    times_of_replanning_average, exploration_rate_average,
                                                    execution_time_average))
                    else:
                        output_file.write("Average,{},{},{},{},{},{},"
                                          "{},{},{},,,,\n".format(length_average, PR_average, PR_known_average,
                                                                  times_of_turning_off_camera_average,
                                                                  times_of_intrusion_average,
                                                                  times_of_intrusion_known_average,
                                                                  times_of_replanning_average,
                                                                  exploration_rate_average, execution_time_average))
                    record_list = []
        print("SC average process finished.")
