#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 将log文件转换为rslt.csv，便于csv_parser.py处理

import re

file_name_to_open = "data_test.log"
file_name_to_write = "rslt.csv"
# 程序工作模式，test代表测试，work代表实际运行
command_mode = "work"

if __name__ == '__main__':
    REF_length = None
    REF_privacy_sum = None
    REF_privacy_sum_known = None
    REF_times_of_turning_off_camera = None
    REF_times_of_intrusion = None
    REF_times_of_intrusion_known = None

    length = None
    privacy_sum = None
    privacy_sum_known = None
    times_of_turning_off_camera = None
    times_of_intrusion = None
    times_of_intrusion_known = None
    times_of_replanning = None
    times_of_no_solution = None
    times_of_flag_1 = 0
    times_of_flag_2 = 0
    times_of_flag_3 = 0
    exploration_rate = None
    execution_time = None

    # x_flag 表示输出的类型
    # 0：输出表头
    # 1：输出Hybrid
    # 2：输出SC
    # 3：输出PP
    x_flag = 0
    with open(file_name_to_open, 'r') as log_file:
        with open(file_name_to_write, "w") as csv_file:
            for line in log_file:
                # 匹配如下内容：
                # [2019-07-17 20:39:44,902] MainFunc-viewradius2.py-><module> line:131
                # [INFO]Iteration: 1; Configuration: grid: 10, safety_threshold: 0.200000,
                # privacy_threshold: 0.050000, the starting point: [0, 0, 0]; the end point: [9, 9, 9];
                # T_budget(alpha): 45.000000 (1.666667); T_optimal(beta): 36.000000 (1.333333);
                # Exploration_rate: 0.100000; Preference: 1.000000; View_radius: 1.000000
                pattern = re.compile(r'.*MainFunc.*Iteration:.*; Configuration: grid: (\d+), '
                                     r'safety_threshold: (\d+.\d+), privacy_threshold: (\d+.\d+), '
                                     r'the starting point: \[(\d+), (\d+), (\d+)\]; '
                                     r'the end point: \[(\d+), (\d+), (\d+)\]; '
                                     r'T_budget\(alpha\): (\d+.\d+) .*; T_optimal\(beta\): (\d+.\d+).*; '
                                     r'Exploration_rate: (\d+.\d+); '
                                     r'Preference: (\d+.\d+); View_radius: (\d+.\d+).*')
                result = pattern.findall(line)
                if result:
                    # 获得结果
                    result = result[0]
                    # 测试代码
                    if command_mode == "test":
                        if x_flag != 0:
                            print(",,,,,,,,,,,,,")
                        x_flag = 0
                        print("gridX,girdY,girdZ,safety_threshold,privacy_threshold,starting_point,end_point,idealtime,"
                              "T_budget,T_optimal,Exploration rate,Preference,View radius,")
                        print("{},{},{},{},{},\"{},{},{}\","
                              "\"{},{},{}\",{},{},{},{},{},{},".format(result[0], result[0], result[0], result[1],
                                                                       result[2],result[3], result[4], result[5],
                                                                       result[6], result[7],result[8],
                                                                       (int(result[0]) - 1) * 3, result[9], result[10],
                                                                       result[11], result[12], result[13]))
                        print(",,,,,,,,,,,,,")
                    # 工作代码
                    else:
                        if x_flag != 0:
                            csv_file.write(",,,,,,,,,,,,,\n")
                        x_flag = 0
                        csv_file.write("gridX,girdY,girdZ,safety_threshold,privacy_threshold,starting_point,end_point,"
                                       "idealtime,T_budget,T_optimal,Exploration rate,Preference,View radius,\n")
                        csv_file.write("{},{},{},{},{},\"{},{},{}\","
                                       "\"{},{},{}\",{},{},{},{},{},{},\n".format(result[0], result[0], result[0],
                                                                                  result[1], result[2], result[3],
                                                                                  result[4], result[5], result[6],
                                                                                  result[7], result[8],
                                                                                  (int(result[0])-1)*3, result[9],
                                                                                  result[10], result[11], result[12],
                                                                                  result[13]))
                        csv_file.write(",,,,,,,,,,,,,\n")

                # 匹配如下内容：
                # [2019-07-17 20:40:07,501] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:453
                # [INFO]Online_Hybrid_Planning: No solution for local planning: from [2, 0, 0] to [4, 2, 0].
                # No solution flag is 1, PR for PP is 1.213061. length of PP is 10, T plan optimal is 13
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'No solution for local planning: .*'
                                     r'No solution flag is (\d+).*')
                result = pattern.findall(line)
                if result:
                    result = result[0]
                    num = int(result)
                    if num == 1:
                        times_of_flag_1 += 1
                    elif num == 2:
                        times_of_flag_2 += 1
                    elif num == 3:
                        times_of_flag_3 += 1
                    else:
                        pass

                # 匹配如下内容:
                # [2019-07-17 20:40:09,929] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:544
                # [INFO]Online_Hybrid_Planning: Length of replanned trajectory: 37
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Length of replanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    length = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:09,929] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:545
                # [INFO]Online_Hybrid_Planning: Sum of privacy threat of replanned trajectory(occ_grid): 28.255528
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Sum of privacy threat of replanned trajectory\(occ_grid\): (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    privacy_sum = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:09,929] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:546
                # [INFO]Online_Hybrid_Planning: Sum of privacy threat of replanned trajectory(occ_grid_known): 18.100493
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Sum of privacy threat of replanned trajectory\(occ_grid_known\): (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    privacy_sum_known = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:09,929] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:547
                # [INFO]Online_Hybrid_Planning: Times of turning off camera of replanned trajectory: 8
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Times of turning off camera of replanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_turning_off_camera = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:09,929] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:549
                # [INFO]Online_Hybrid_Planning: Times of intrusion of replanned trajectory(occ_grid): 14
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Times of intrusion of replanned trajectory\(occ_grid\): (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_intrusion = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:09,929] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:550
                # [INFO]Online_Hybrid_Planning: Times of intrusion of replanned trajectory(occ_grid_known): 11
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Times of intrusion of replanned trajectory\(occ_grid_known\): (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_intrusion_known = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:09,937] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:588
                # [INFO]Online_Hybrid_Planning: Length of preplanned trajectory: 27
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Length of preplanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_length = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:09,937] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:589
                # [INFO]Online_Hybrid_Planning: Sum of privacy threat of preplanned trajectory(occ_grid): 39.713011
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Sum of privacy threat of preplanned trajectory\(occ_grid\): (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_privacy_sum = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:09,937] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:590
                # [INFO]Online_Hybrid_Planning:
                # Sum of privacy threat of preplanned trajectory(occ_grid_known): 29.882827
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Sum of privacy threat of preplanned trajectory\(occ_grid_known\): (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_privacy_sum_known = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:09,937] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:591
                # [INFO]Online_Hybrid_Planning: Times of turning off camera of preplanned trajectory: 0
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Times of turning off camera of preplanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_times_of_turning_off_camera = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:09,937] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:593
                # [INFO]Online_Hybrid_Planning: Times of intrusion of preplanned trajectory(occ_grid): 18
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Times of intrusion of preplanned trajectory\(occ_grid\): (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_times_of_intrusion = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:09,938] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:594
                # [INFO]Online_Hybrid_Planning: Times of intrusion of preplanned trajectory(occ_grid_known): 16
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Times of intrusion of preplanned trajectory\(occ_grid_known\): (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_times_of_intrusion_known = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:09,938] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:612
                # [INFO]Online_Hybrid_Planning: Replanning times: 4
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Replanning times: (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_replanning = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:09,938] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:614
                # [INFO]Online_Hybrid_Planning: No solution times: 4
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'No solution times: (\d+)')
                result = pattern.findall(line)
                if result:
                    times_of_no_solution = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:09,938] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:616
                # [INFO]Online_Hybrid_Planning: Execution time: 3.056799
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Execution time: (\d+\.?\d*)')
                result = pattern.findall(line)
                if result:
                    execution_time = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:09,946] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:646
                # [INFO]Online_Hybrid_Planning: Exploration rate: 0.200000
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Exploration rate: (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    exploration_rate = result[0]
                    if command_mode == "test":
                        if x_flag != 1:
                            if x_flag != 0:
                                print(",,,,,,,,,,,,,")
                            print(",Length,PR,PR_known,turn off camera,Intrusion,Intrusion_known,replan times,"
                                  "No solution times,flag 1 times,flag 2 times,flag 3 times,exploration rate,"
                                  "execution time")

                        x_flag = 1
                        # print("REF,{},{},,{},,,,,,,,".format(REF_length, REF_privacy_sum, REF_times_of_turning_off_camera,
                        #                                      REF_times_of_intrusion))
                        # csv_file.write("REF,{},{},,{},,,,,,,,\n".format(REF_length, REF_privacy_sum,
                        #                                                 REF_times_of_turning_off_camera,
                        #                                                 REF_times_of_intrusion))
                        print("Hybrid,{},{},{},{},{},"
                              "{},{},{},{},{},{},{},{}".format(length, privacy_sum, privacy_sum_known,
                                                               times_of_turning_off_camera, times_of_intrusion,
                                                               times_of_intrusion_known, times_of_replanning,
                                                               times_of_no_solution, times_of_flag_1, times_of_flag_2,
                                                               times_of_flag_3, exploration_rate, execution_time))
                    else:
                        if x_flag != 1:
                            if x_flag != 0:
                                csv_file.write(",,,,,,,,,,,,,\n")
                            csv_file.write(",Length,PR,PR_known,turn off camera,Intrusion,Intrusion_known,replan times,"
                                           "No solution times,flag 1 times,flag 2 times,flag 3 times,"
                                           "exploration rate,execution time\n")
                            x_flag = 1
                        csv_file.write("Hybrid,{},{},{},{},{},"
                                       "{},{},{},{},{},{},{},{}\n".format(length, privacy_sum, privacy_sum_known,
                                                                          times_of_turning_off_camera,
                                                                          times_of_intrusion, times_of_intrusion_known,
                                                                          times_of_replanning, times_of_no_solution,
                                                                          times_of_flag_1, times_of_flag_2,
                                                                          times_of_flag_3, exploration_rate,
                                                                          execution_time))
                    times_of_flag_1 = 0
                    times_of_flag_2 = 0
                    times_of_flag_3 = 0

                # 匹配如下内容：
                # [2019-07-17 20:40:10,109] SensorConfigOnline.py->Astar_Sensor_Config_online line:221
                # [INFO]Online_Sensor_Config: Length of replanned trajectory: 27
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Length of replanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    length = result[0]

                # 匹配如下内容
                # [2019-07-17 20:40:10,109] SensorConfigOnline.py->Astar_Sensor_Config_online line:222
                # [INFO]Online_Sensor_Config: Sum of privacy threat of replanned trajectory(occ_grid): 33.800477
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Sum of privacy threat of replanned trajectory\(occ_grid\): (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    privacy_sum = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:10,109] SensorConfigOnline.py->Astar_Sensor_Config_online line:223
                # [INFO]Online_Sensor_Config: Sum of privacy threat of replanned trajectory(occ_grid_known): 24.314833
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Sum of privacy threat of replanned trajectory\(occ_grid_known\): (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    privacy_sum_known = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:10,109] SensorConfigOnline.py->Astar_Sensor_Config_online line:224
                # [INFO]Online_Sensor_Config: Times of turning off camera of replanned trajectory: 8
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Times of turning off camera of replanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_turning_off_camera = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:10,109] SensorConfigOnline.py->Astar_Sensor_Config_online line:226
                # [INFO]Online_Sensor_Config: Times of intrusion of replanned trajectory(occ_grid): 18
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Times of intrusion of replanned trajectory\(occ_grid\): (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_intrusion = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:10,110] SensorConfigOnline.py->Astar_Sensor_Config_online line:227
                # [INFO]Online_Sensor_Config: Times of intrusion of replanned trajectory(occ_grid_known): 16
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Times of intrusion of replanned trajectory\(occ_grid_known\): (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_intrusion_known = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:10,117] SensorConfigOnline.py->Astar_Sensor_Config_online line:268
                # [INFO]Online_Sensor_Config: Length of preplanned trajectory: 27
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Length of preplanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_length = result[0]

                # 匹配如下内容
                # [2019-07-17 20:40:10,117] SensorConfigOnline.py->Astar_Sensor_Config_online line:269
                # [INFO]Online_Sensor_Config: Sum of privacy threat of preplanned trajectory(occ_grid): 39.713011
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Sum of privacy threat of preplanned trajectory\(occ_grid\): (\d+\.\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_privacy_sum = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:10,118] SensorConfigOnline.py->Astar_Sensor_Config_online line:270
                # [INFO]Online_Sensor_Config: Sum of privacy threat of preplanned trajectory(occ_grid_known): 29.882827
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Sum of privacy threat of preplanned trajectory(occ_grid_known): (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_privacy_sum_known = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:10,118] SensorConfigOnline.py->Astar_Sensor_Config_online line:271
                # [INFO]Online_Sensor_Config: Times of turning off camera of preplanned trajectory: 0
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Times of turning off camera of preplanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_times_of_turning_off_camera = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:10,118] SensorConfigOnline.py->Astar_Sensor_Config_online line:274
                # [INFO]Online_Sensor_Config: Times of intrusion of preplanned trajectory(occ_grid): 18
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Times of intrusion of preplanned trajectory\(occ_grid\): (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_times_of_intrusion = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:10,118] SensorConfigOnline.py->Astar_Sensor_Config_online line:275
                # [INFO]Online_Sensor_Config: Times of intrusion of preplanned trajectory(occ_grid_known): 16
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Times of intrusion of preplanned trajectory\(occ_grid_known\): (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_times_of_intrusion_known = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:10,118] SensorConfigOnline.py->Astar_Sensor_Config_online line:292
                # [INFO]Online_Sensor_Config: Replanning times: 4
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Replanning times: (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_replanning = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:10,118] SensorConfigOnline.py->Astar_Sensor_Config_online line:294
                # [INFO]Online_Sensor_Config: Execution time: 0
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Execution time: (\d+\.?\d*)')
                result = pattern.findall(line)
                if result:
                    execution_time = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:10,123] SensorConfigOnline.py->Astar_Sensor_Config_online line:324
                # [INFO]Online_Sensor_Config: Exploration rate: 0.200000
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Exploration rate: (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    exploration_rate = result[0]
                    if command_mode == "test":
                        if x_flag != 2:
                            if x_flag != 0:
                                print(",,,,,,,,,,,,,")
                            print(",Length,PR,PR_known,turn off camera,Intrusion,Intrusion_known,"
                                  "replan times,exploration rate,execution time,,,,")
                        x_flag = 2
                        # print("REF,{},{},,{},,,,,,,,".format(REF_length, REF_privacy_sum, REF_times_of_turning_off_camera,
                        #                                      REF_times_of_intrusion))
                        # csv_file.write("REF,{},{},,{},,,,,,,,\n".format(REF_length, REF_privacy_sum,
                        #                                                 REF_times_of_turning_off_camera,
                        #                                                 REF_times_of_intrusion))
                        print("SC,{},{},{},{},"
                              "{},{},{},{},{},,,,".format(length, privacy_sum, privacy_sum_known,
                                                          times_of_turning_off_camera, times_of_intrusion,
                                                          times_of_intrusion_known, times_of_replanning,
                                                          exploration_rate, execution_time))
                    else:
                        if x_flag != 2:
                            if x_flag != 0:
                                csv_file.write(",,,,,,,,,,,,,\n")
                            csv_file.write(",Length,PR,PR_known,turn off camera,Intrusion,Intrusion_known,"
                                           "replan times,exploration rate,execution time,,,,\n")
                        x_flag = 2
                        csv_file.write("SC,{},{},{},{},"
                                       "{},{},{},{},{},,,,\n".format(length, privacy_sum, privacy_sum_known,
                                                                     times_of_turning_off_camera, times_of_intrusion,
                                                                     times_of_intrusion_known, times_of_replanning,
                                                                     exploration_rate, execution_time))

                # 匹配如下内容：
                # [2019-07-17 20:40:10,809] PathPlanningOnline.py->Astar_Path_Planning_online line:248
                # [INFO]Online_Path_Planning: No solution for local planning: from [2, 0, 0] to [4, 2, 0].
                # No solution flag is 1, PR for PP is 1.213061. length of PP is 10, T plan optimal is 13
                pattern = re.compile(r'.*PathPlanningOnline.*Online_Path_Planning: '
                                     r'No solution for local planning: .*'
                                     r'No solution flag is (\d+).*')
                result = pattern.findall(line)
                if result:
                    result = result[0]
                    num = int(result)
                    if num == 1:
                        times_of_flag_1 += 1
                    elif num == 2:
                        times_of_flag_2 += 1
                    elif num == 3:
                        times_of_flag_3 += 1
                    else:
                        pass

                # 匹配如下内容：
                # [2019-07-17 20:40:11,205] PathPlanningOnline.py->Astar_Path_Planning_online line:339
                # [INFO]Online_Path_Planning: Length of replanned trajectory: 35
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Length of replanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    length = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:11,205] PathPlanningOnline.py->Astar_Path_Planning_online line:340
                # [INFO]Online_Path_Planning: Sum of privacy threat of replanned trajectory(occ_grid): 33.111192
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Sum of privacy threat of replanned trajectory\(occ_grid\): (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    privacy_sum = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:11,205] PathPlanningOnline.py->Astar_Path_Planning_online line:341
                # [INFO]Online_Path_Planning: Sum of privacy threat of replanned trajectory(occ_grid_known): 27.264731
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Sum of privacy threat of replanned trajectory\(occ_grid_known\): (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    privacy_sum_known = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:11,205] PathPlanningOnline.py->Astar_Path_Planning_online line:342
                # [INFO]Online_Path_Planning: Times of turning off camera of replanned trajectory: 0
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Times of turning off camera of replanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_turning_off_camera = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:11,205] PathPlanningOnline.py->Astar_Path_Planning_online line:344
                # [INFO]Online_Path_Planning: Times of intrusion of replanned trajectory(occ_grid): 15
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Times of intrusion of replanned trajectory\(occ_grid\): (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_intrusion = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:21,584] PathPlanningOnline.py->Astar_Path_Planning_online line:774
                # [INFO]Online_Path_Planning: Times of intrusion of replanned trajectory(occ_grid_known): 10
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Times of intrusion of replanned trajectory\(occ_grid_known\): (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_intrusion_known = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:11,205] PathPlanningOnline.py->Astar_Path_Planning_online line:345
                # [INFO]Online_Path_Planning: Times of intrusion of replanned trajectory(occ_grid_known): 13
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Length of preplanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_length = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:11,213] PathPlanningOnline.py->Astar_Path_Planning_online line:387
                # [INFO]Online_Path_Planning: Sum of privacy threat of preplanned trajectory(occ_grid): 39.713011
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Sum of privacy threat of preplanned trajectory\(occ_grid\): (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_privacy_sum = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:11,213] PathPlanningOnline.py->Astar_Path_Planning_online line:388
                # [INFO]Online_Path_Planning: Sum of privacy threat of preplanned trajectory(occ_grid_known): 33.866551
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Sum of privacy threat of preplanned trajectory\(occ_grid_known\): (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_privacy_sum_known = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:11,213] PathPlanningOnline.py->Astar_Path_Planning_online line:389
                # [INFO]Online_Path_Planning: Times of turning off camera of preplanned trajectory: 0
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Times of turning off camera of preplanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_times_of_turning_off_camera = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:11,213] PathPlanningOnline.py->Astar_Path_Planning_online line:392
                # [INFO]Online_Path_Planning: Times of intrusion of preplanned trajectory(occ_grid): 18
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Times of intrusion of preplanned trajectory\(occ_grid\): (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_times_of_intrusion = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:11,213] PathPlanningOnline.py->Astar_Path_Planning_online line:393
                # [INFO]Online_Path_Planning: Times of intrusion of preplanned trajectory(occ_grid_known): 16
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Times of intrusion of preplanned trajectory\(occ_grid_known\): (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_times_of_intrusion = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:11,213] PathPlanningOnline.py->Astar_Path_Planning_online line:409
                # [INFO]Online_Path_Planning: Replanning times: 5
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Replanning times: (\d+).*')
                result = pattern.findall(line)
                if result:
                    times_of_replanning = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:11,213] PathPlanningOnline.py->Astar_Path_Planning_online line:411
                # [INFO]Online_Path_Planning: No solution times: 5
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'No solution times: (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_no_solution = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:11,213] PathPlanningOnline.py->Astar_Path_Planning_online line:413
                # [INFO]Online_Path_Planning: Execution time: 1
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Execution time: (\d+\.?\d*)')
                result = pattern.findall(line)
                if result:
                    execution_time = result[0]

                # 匹配如下内容：
                # [2019-07-17 20:40:11,221] PathPlanningOnline.py->Astar_Path_Planning_online line:443
                # [INFO]Online_Path_Planning: Exploration rate: 0.220000
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Exploration rate: (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    exploration_rate = result[0]
                    if command_mode == "test":
                        if x_flag != 3:
                            if x_flag != 0:
                                print(",,,,,,,,,,,,")
                            print(",Length,PR,PR_known,turn off camera,Intrusion,Intrusion_known,replan times,"
                                  "No solution times,flag 1 times,flag 2 times,flag 3 times,exploration rate,"
                                  "execution time")

                        x_flag = 3
                        # print("REF,{},{},,{},,,,,,,,".format(REF_length, REF_privacy_sum, REF_times_of_turning_off_camera,
                        #                                      REF_times_of_intrusion))
                        # csv_file.write("REF,{},{},,{},,,,,,,,\n".format(REF_length, REF_privacy_sum,
                        #                                                 REF_times_of_turning_off_camera,
                        #                                                 REF_times_of_intrusion))
                        print("PP,{},{},{},{},{},"
                              "{},{},{},{},{},{},{},{}".format(length, privacy_sum, privacy_sum_known,
                                                               times_of_turning_off_camera, times_of_intrusion,
                                                               times_of_intrusion_known, times_of_replanning,
                                                               times_of_no_solution, times_of_flag_1,
                                                               times_of_flag_2, times_of_flag_3,
                                                               exploration_rate, execution_time))
                    else:
                        if x_flag != 3:
                            if x_flag != 0:
                                csv_file.write(",,,,,,,,,,,,,\n")
                            csv_file.write(",Length,PR,PR_known,turn off camera,Intrusion,Intrusion_known,replan times,"
                                           "No solution times,flag 1 times,flag 2 times,flag 3 times,"
                                           "exploration rate,execution time\n")
                        x_flag = 3
                        csv_file.write("PP,{},{},{},{},{},"
                                       "{},{},{},{},{},{},{},{}\n".format(length, privacy_sum, privacy_sum_known,
                                                                          times_of_turning_off_camera,
                                                                          times_of_intrusion, times_of_intrusion_known,
                                                                          times_of_replanning, times_of_no_solution,
                                                                          times_of_flag_1, times_of_flag_2,
                                                                          times_of_flag_3, exploration_rate,
                                                                          execution_time))
                    times_of_flag_1 = 0
                    times_of_flag_2 = 0
                    times_of_flag_3 = 0
    print("The log to csv finished.")
