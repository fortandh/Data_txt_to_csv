#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 这个文件的主要目标是将 csv_parser.py 分开的三个文件中 pp.csv 进行平均数统计
# 结果存入 pp_average.csv 中

import re

from Support.pp_record import PP_Record

input_pp_file_name = "pp.csv"
output_pp_file_name = "pp_average.csv"

group_size = 10
# 程序工作模式，test代表测试，work代表实际运行
command_mode = "work"


if __name__ == '__main__':
    with open(input_pp_file_name, "r") as input_file, \
            open(output_pp_file_name, "w") as output_file:
        record_list = []
        if command_mode == "test":
            print(",Length,PR,PR_known,turn off camera,Intrusion,Intrusion_known,replan times,"
                  "No solution times,flag 1 times,flag 2 times,flag 3 times,exploration rate,execution time")
        else:
            output_file.write(",Length,PR,PR_known,turn off camera,Intrusion,Intrusion_known,replan times,"
                              "No solution times,flag 1 times,flag 2 times,flag 3 times,exploration rate,"
                              "execution time\n")
        for line in input_file:
            # 匹配如下内容：
            # PP,35,33.111192,27.264731,0,15,13,5,5,0,0,0,0.220000,1
            pattern = re.compile(r'.*,(\d+),(\d+\.\d+),(\d+\.\d+),(\d+),(\d+),'
                                 r'(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+\.\d+),(\d+\.?\d*).*')
            result = pattern.findall(line)
            if result:
                result = result[0]
                tmp_record = PP_Record(int(result[0]), float(result[1]), float(result[2]), int(result[3]),
                                       int(result[4]), int(result[5]), int(result[6]), int(result[7]),
                                       int(result[8]), int(result[9]), int(result[10]), float(result[11]),
                                       float(result[12]))
                record_list.append(tmp_record)

                if len(record_list) == group_size:
                    length_average = 0
                    PR_average = 0
                    PR_known_average = 0
                    times_of_turning_off_camera_average = 0
                    times_of_intrusion_average = 0
                    times_of_intrusion_known_average = 0
                    times_of_replanning_average = 0
                    times_of_no_solution_average = 0
                    times_of_flag_1_average = 0
                    times_of_flag_2_average = 0
                    times_of_flag_3_average = 0
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
                        times_of_no_solution_average += record_list[i].times_of_no_solution
                        times_of_flag_1_average += record_list[i].times_of_flag_1
                        times_of_flag_2_average += record_list[i].times_of_flag_2
                        times_of_flag_3_average += record_list[i].times_of_flag_3
                        exploration_rate_average += record_list[i].exploration_rate
                        execution_time_average += record_list[i].execution_time

                    length_average /= group_size
                    PR_average /= group_size
                    PR_known_average /= group_size
                    times_of_turning_off_camera_average /= group_size
                    times_of_intrusion_average /= group_size
                    times_of_intrusion_known_average /= group_size
                    times_of_replanning_average /= group_size
                    times_of_no_solution_average /= group_size
                    times_of_flag_1_average /= group_size
                    times_of_flag_2_average /= group_size
                    times_of_flag_3_average /= group_size
                    exploration_rate_average /= group_size
                    execution_time_average /= group_size

                    if command_mode == "test":
                        print("Average,{},{},{},{},{},"
                              "{},{},{},{},{},{},{},{}".format(length_average, PR_average, PR_known_average,
                                                               times_of_turning_off_camera_average,
                                                               times_of_intrusion_average,
                                                               times_of_intrusion_known_average,
                                                               times_of_replanning_average,
                                                               times_of_no_solution_average, times_of_flag_1_average,
                                                               times_of_flag_2_average, times_of_flag_3_average,
                                                               exploration_rate_average, execution_time_average))
                    else:
                        output_file.write("Average,{},{},{},{},{},{},{},{},{},"
                                          "{},{},{},{}\n".format(length_average, PR_average, PR_known_average,
                                                                 times_of_turning_off_camera_average,
                                                                 times_of_intrusion_average,
                                                                 times_of_intrusion_known_average,
                                                                 times_of_replanning_average,
                                                                 times_of_no_solution_average,
                                                                 times_of_flag_1_average,
                                                                 times_of_flag_2_average,
                                                                 times_of_flag_3_average,
                                                                 exploration_rate_average, execution_time_average))
                    record_list = []
        print("PP average process finished.")
