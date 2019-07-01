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
                # [2019-06-30 17:20:10,689] MainFunc-exploration.py-><module> line:111
                # [INFO]Iteration: 1; Configuration: grid: 10, safety_threshold: 0.150000, privacy_threshold: 0.050000,
                # the starting point: [0, 0, 0]; the end point: [9, 9, 9]; T_budget(alpha): 36.000000 (1.333333);
                # T_optimal(beta): 31.500000 (1.166667); Exploration_rate: 0.000000; Preference: 1.000000;
                # View_radius: 2.500000
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
                            print(",,,,,,,,,,,,")
                        x_flag = 0
                        print("gridX,girdY,girdZ,safety_threshold,privacy_threshold,starting_point,end_point,idealtime,"
                              "T_budget,T_optimal,Exploration rate,Preference,View radius")
                        print("{},{},{},{},{},\"{},{},{}\","
                              "\"{},{},{}\",{},{},{},{},{},{}".format(result[0], result[0], result[0], result[1],
                                                                      result[2],result[3], result[4], result[5],
                                                                      result[6], result[7],result[8],
                                                                      (int(result[0]) - 1) * 3, result[9], result[10],
                                                                      result[11], result[12], result[13]))
                        print(",,,,,,,,,,,,")
                    # 工作代码
                    else:
                        if x_flag != 0:
                            csv_file.write(",,,,,,,,,,,,\n")
                        x_flag = 0
                        csv_file.write("gridX,girdY,girdZ,safety_threshold,privacy_threshold,starting_point,end_point,"
                                       "idealtime,T_budget,T_optimal,Exploration rate,Preference,View radius\n")
                        csv_file.write("{},{},{},{},{},\"{},{},{}\","
                                       "\"{},{},{}\",{},{},{},{},{},{}\n".format(result[0], result[0], result[0],
                                                                                 result[1], result[2], result[3],
                                                                                 result[4], result[5], result[6],
                                                                                 result[7], result[8],
                                                                                 (int(result[0])-1)*3, result[9],
                                                                                 result[10], result[11], result[12],
                                                                                 result[13]))
                        csv_file.write(",,,,,,,,,,,,\n")

                # 匹配如下内容：
                # [2019-06-30 17:22:42,293] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:693
                # [INFO]Online_Hybrid_Planning: No solution for local planning: from [3, 9, 2] to [6, 9, 2].
                # No soultion flag is 1, PR for PP is 81.413976. length of PP is 3, T plan optimal is 7
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'No solution for local planning: .*'
                                     r'No soultion flag is (\d+).*')
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
                # [2019-06-30 17:23:19,897] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:835
                # [INFO]Online_Hybrid_Planning: Length of replanned trajectory: 27
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Length of replanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    length = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:19,898] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:836
                # [INFO]Online_Hybrid_Planning: Sum of privacy threat of replanned trajectory(occ_grid): 145.777165
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Sum of privacy threat of replanned trajectory\(occ_grid\): (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    privacy_sum = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:19,898] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:837
                # [INFO]Online_Hybrid_Planning:
                # Sum of privacy threat of replanned trajectory(occ_grid_known): 145.777165
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Sum of privacy threat of replanned trajectory\(occ_grid_known\): (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    privacy_sum_known = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:19,898] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:838
                # [INFO]Online_Hybrid_Planning: Times of turning off camera of replanned trajectory: 5
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Times of turning off camera of replanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_turning_off_camera = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:19,898] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:840
                # [INFO]Online_Hybrid_Planning: Times of intrusion of replanned trajectory(occ_grid): 12
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Times of intrusion of replanned trajectory\(occ_grid\): (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_intrusion = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:19,898] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:841
                # [INFO]Online_Hybrid_Planning: Times of intrusion of replanned trajectory(occ_grid_known): 12
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Times of intrusion of replanned trajectory\(occ_grid_known\): (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_intrusion_known = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:19,905] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:879
                # [INFO]Online_Hybrid_Planning: Length of preplanned trajectory: 27
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Length of preplanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_length = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:19,905] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:880
                # [INFO]Online_Hybrid_Planning: Sum of privacy threat of preplanned trajectory(occ_grid): 422.778035
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Sum of privacy threat of preplanned trajectory\(occ_grid\): (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_privacy_sum = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:19,905] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:881
                # [INFO]Online_Hybrid_Planning:
                # Sum of privacy threat of preplanned trajectory(occ_grid_known): 422.778035
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Sum of privacy threat of preplanned trajectory\(occ_grid_known\): (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_privacy_sum_known = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:19,905] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:882
                # [INFO]Online_Hybrid_Planning: Times of turning off camera of preplanned trajectory: 0
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Times of turning off camera of preplanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_times_of_turning_off_camera = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:19,905] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:884
                # [INFO]Online_Hybrid_Planning: Times of intrusion of preplanned trajectory(occ_grid): 12
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Times of intrusion of preplanned trajectory\(occ_grid\): (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_times_of_intrusion = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:19,905] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:885
                # [INFO]Online_Hybrid_Planning: Times of intrusion of preplanned trajectory(occ_grid_known): 12
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Times of intrusion of preplanned trajectory\(occ_grid_known\): (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_times_of_intrusion_known = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:19,905] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:903
                # [INFO]Online_Hybrid_Planning: Replanning times: 3
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Replanning times: (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_replanning = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:19,905] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:905
                # [INFO]Online_Path_Planning: No solution times: 0
                pattern = re.compile(r'.*HybridPlanning.*Online_Path_Planning: '
                                     r'No solution times: (\d+)')
                result = pattern.findall(line)
                if result:
                    times_of_no_solution = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:19,907] HybridPlanning_SA.py->Astar_Hybrid_Planning_online line:935
                # [INFO]Online_Hybrid_Planning: Exploration rate: 0.220000
                pattern = re.compile(r'.*HybridPlanning.*Online_Hybrid_Planning: '
                                     r'Exploration rate: (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    exploration_rate = result[0]
                    if command_mode == "test":
                        if x_flag != 1:
                            if x_flag != 0:
                                print(",,,,,,,,,,,,")
                            print(",Length,PR,PR_known,turn off camera,Intrusion,Intrusion_known,replan times,"
                                  "No solution times,flag 1 times,flag 2 times,flag 3 times,exploration rate")

                        x_flag = 1
                        # print("REF,{},{},,{},,,,,,,,".format(REF_length, REF_privacy_sum, REF_times_of_turning_off_camera,
                        #                                      REF_times_of_intrusion))
                        # csv_file.write("REF,{},{},,{},,,,,,,,\n".format(REF_length, REF_privacy_sum,
                        #                                                 REF_times_of_turning_off_camera,
                        #                                                 REF_times_of_intrusion))
                        print("Hybrid,{},{},{},{},{},"
                              "{},{},{},{},{},{},{}".format(length, privacy_sum, privacy_sum_known,
                                                            times_of_turning_off_camera, times_of_intrusion,
                                                            times_of_intrusion_known, times_of_replanning,
                                                            times_of_no_solution, times_of_flag_1, times_of_flag_2,
                                                            times_of_flag_3, exploration_rate))
                    else:
                        if x_flag != 1:
                            if x_flag != 0:
                                csv_file.write(",,,,,,,,,,,,\n")
                            csv_file.write(",Length,PR,PR_known,turn off camera,Intrusion,Intrusion_known,replan times,"
                                           "No solution times,flag 1 times,flag 2 times,flag 3 times,"
                                           "exploration rate\n")
                            x_flag = 1
                        csv_file.write("Hybrid,{},{},{},{},{},"
                                       "{},{},{},{},{},{},{}\n".format(length, privacy_sum, privacy_sum_known,
                                                                       times_of_turning_off_camera, times_of_intrusion,
                                                                       times_of_intrusion_known, times_of_replanning,
                                                                       times_of_no_solution, times_of_flag_1,
                                                                       times_of_flag_2, times_of_flag_3,
                                                                       exploration_rate))
                    times_of_flag_1 = 0
                    times_of_flag_2 = 0
                    times_of_flag_3 = 0

                # 匹配如下内容：
                # [2019-06-30 17:23:20,010] SensorConfigOnline.py->Astar_Sensor_Config_online line:556
                # [INFO]Online_Sensor_Config: Length of replanned trajectory: 27
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Length of replanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    length = result[0]

                # 匹配如下内容
                # [2019-06-30 17:23:20,010] SensorConfigOnline.py->Astar_Sensor_Config_online line:557
                # [INFO]Online_Sensor_Config: Sum of privacy threat of replanned trajectory(occ_grid): 182.891553
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Sum of privacy threat of replanned trajectory\(occ_grid\): (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    privacy_sum = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:20,010] SensorConfigOnline.py->Astar_Sensor_Config_online line:558
                # [INFO]Online_Sensor_Config: Sum of privacy threat of replanned trajectory(occ_grid_known): 182.891553
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Sum of privacy threat of replanned trajectory\(occ_grid_known\): (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    privacy_sum_known = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:20,010] SensorConfigOnline.py->Astar_Sensor_Config_online line:559
                # [INFO]Online_Sensor_Config: Times of turning off camera of replanned trajectory: 11
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Times of turning off camera of replanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_turning_off_camera = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:20,010] SensorConfigOnline.py->Astar_Sensor_Config_online line:561
                # [INFO]Online_Sensor_Config: Times of intrusion of replanned trajectory(occ_grid): 12
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Times of intrusion of replanned trajectory\(occ_grid\): (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_intrusion = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:20,010] SensorConfigOnline.py->Astar_Sensor_Config_online line:562
                # [INFO]Online_Sensor_Config: Times of intrusion of replanned trajectory(occ_grid_known): 12
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Times of intrusion of replanned trajectory\(occ_grid_known\): (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_intrusion_known = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:20,017] SensorConfigOnline.py->Astar_Sensor_Config_online line:603
                # [INFO]Online_Sensor_Config: Length of preplanned trajectory: 27
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Length of preplanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_length = result[0]

                # 匹配如下内容
                # [2019-06-30 17:23:20,017] SensorConfigOnline.py->Astar_Sensor_Config_online line:604
                # [INFO]Online_Sensor_Config: Sum of privacy threat of preplanned trajectory(occ_grid): 422.778035
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Sum of privacy threat of preplanned trajectory\(occ_grid\): (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_privacy_sum = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:20,017] SensorConfigOnline.py->Astar_Sensor_Config_online line:605
                # [INFO]Online_Sensor_Config: Sum of privacy threat of preplanned trajectory(occ_grid_known): 422.778035
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Sum of privacy threat of preplanned trajectory(occ_grid_known): (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_privacy_sum_known = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:20,017] SensorConfigOnline.py->Astar_Sensor_Config_online line:606
                # [INFO]Online_Sensor_Config: Times of turning off camera of preplanned trajectory: 0
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Times of turning off camera of preplanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_times_of_turning_off_camera = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:20,017] SensorConfigOnline.py->Astar_Sensor_Config_online line:609
                # [INFO]Online_Sensor_Config: Times of intrusion of preplanned trajectory(occ_grid): 12
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Times of intrusion of preplanned trajectory\(occ_grid\): (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_times_of_intrusion = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:20,017] SensorConfigOnline.py->Astar_Sensor_Config_online line:610
                # [INFO]Online_Sensor_Config: Times of intrusion of preplanned trajectory(occ_grid_known): 12
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Times of intrusion of preplanned trajectory\(occ_grid_known\): (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_times_of_intrusion_known = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:20,017] SensorConfigOnline.py->Astar_Sensor_Config_online line:627
                # [INFO]Online_Sensor_Config: Replanning times: 5
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Replanning times: (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_replanning = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:20,019] SensorConfigOnline.py->Astar_Sensor_Config_online line:657
                # [INFO]Online_Sensor_Config: Exploration rate: 0.180000
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Exploration rate: (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    exploration_rate = result[0]
                    if command_mode == "test":
                        if x_flag != 2:
                            if x_flag != 0:
                                print(",,,,,,,,,,,,")
                            print(",Length,PR,PR_known,turn off camera,Intrusion,Intrusion_known,"
                                  "replan times,exploration rate,,,,")
                        x_flag = 2
                        # print("REF,{},{},,{},,,,,,,,".format(REF_length, REF_privacy_sum, REF_times_of_turning_off_camera,
                        #                                      REF_times_of_intrusion))
                        # csv_file.write("REF,{},{},,{},,,,,,,,\n".format(REF_length, REF_privacy_sum,
                        #                                                 REF_times_of_turning_off_camera,
                        #                                                 REF_times_of_intrusion))
                        print("SC,{},{},{},{},"
                              "{},{},{},{},,,,".format(length, privacy_sum, privacy_sum_known,
                                                       times_of_turning_off_camera, times_of_intrusion,
                                                       times_of_intrusion_known, times_of_replanning,
                                                       exploration_rate))
                    else:
                        if x_flag != 2:
                            if x_flag != 0:
                                csv_file.write(",,,,,,,,,,,,\n")
                            csv_file.write(",Length,PR,PR_known,turn off camera,Intrusion,Intrusion_known,"
                                           "replan times,exploration rate,,,,\n")
                        x_flag = 2
                        csv_file.write("SC,{},{},{},{},"
                                       "{},{},{},{},,,,\n".format(length, privacy_sum, privacy_sum_known,
                                                                  times_of_turning_off_camera, times_of_intrusion,
                                                                  times_of_intrusion_known, times_of_replanning,
                                                                  exploration_rate))
                # 匹配如下内容：
                # [2019-06-30 17:23:21,583] PathPlanningOnline.py->Astar_Path_Planning_online line:767
                # [INFO]Online_Path_Planning: Length of replanned trajectory: 35
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Length of replanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    length = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:21,583] PathPlanningOnline.py->Astar_Path_Planning_online line:768
                # [INFO]Online_Path_Planning: Sum of privacy threat of replanned trajectory(occ_grid): 159.074167
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Sum of privacy threat of replanned trajectory\(occ_grid\): (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    privacy_sum = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:21,583] PathPlanningOnline.py->Astar_Path_Planning_online line:769
                # [INFO]Online_Path_Planning: Sum of privacy threat of replanned trajectory(occ_grid_known): 159.074167
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Sum of privacy threat of replanned trajectory\(occ_grid_known\): (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    privacy_sum_known = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:21,584] PathPlanningOnline.py->Astar_Path_Planning_online line:770
                # [INFO]Online_Path_Planning: Times of turning off camera of replanned trajectory: 0
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Times of turning off camera of replanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_turning_off_camera = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:21,584] PathPlanningOnline.py->Astar_Path_Planning_online line:773
                # [INFO]Online_Path_Planning: Times of intrusion of replanned trajectory(occ_grid): 10
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
                # [2019-06-30 17:23:21,591] PathPlanningOnline.py->Astar_Path_Planning_online line:815
                # [INFO]Online_Path_Planning: Length of preplanned trajectory: 27
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Length of preplanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_length = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:21,591] PathPlanningOnline.py->Astar_Path_Planning_online line:816
                # [INFO]Online_Path_Planning: Sum of privacy threat of preplanned trajectory(occ_grid): 422.778035
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Sum of privacy threat of preplanned trajectory\(occ_grid\): (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_privacy_sum = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:21,591] PathPlanningOnline.py->Astar_Path_Planning_online line:817
                # [INFO]Online_Path_Planning: Sum of privacy threat of preplanned trajectory(occ_grid_known): 422.778035
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Sum of privacy threat of preplanned trajectory\(occ_grid_known\): (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_privacy_sum_known = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:21,591] PathPlanningOnline.py->Astar_Path_Planning_online line:818
                # [INFO]Online_Path_Planning: Times of turning off camera of preplanned trajectory: 0
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Times of turning off camera of preplanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_times_of_turning_off_camera = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:21,591] PathPlanningOnline.py->Astar_Path_Planning_online line:821
                # [INFO]Online_Path_Planning: Times of intrusion of preplanned trajectory(occ_grid): 12
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Times of intrusion of preplanned trajectory\(occ_grid\): (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_times_of_intrusion = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:21,591] PathPlanningOnline.py->Astar_Path_Planning_online line:822
                # [INFO]Online_Path_Planning: Times of intrusion of preplanned trajectory(occ_grid_known): 12
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Times of intrusion of preplanned trajectory\(occ_grid_known\): (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_times_of_intrusion = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:21,591] PathPlanningOnline.py->Astar_Path_Planning_online line:838
                # [INFO]Online_Path_Planning: Replanning times: 2
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Replanning times: (\d+).*')
                result = pattern.findall(line)
                if result:
                    times_of_replanning = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:21,591] PathPlanningOnline.py->Astar_Path_Planning_online line:840
                # [INFO]Online_Path_Planning: No solution times: 0
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'No solution times: (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_no_solution = result[0]

                # 匹配如下内容：
                # [2019-06-30 17:23:21,594] PathPlanningOnline.py->Astar_Path_Planning_online line:870
                # [INFO]Online_Path_Planning: Exploration rate: 0.260000
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
                                  "No solution times,flag 1 times,flag 2 times,flag 3 times,exploration rate")

                        x_flag = 3
                        # print("REF,{},{},,{},,,,,,,,".format(REF_length, REF_privacy_sum, REF_times_of_turning_off_camera,
                        #                                      REF_times_of_intrusion))
                        # csv_file.write("REF,{},{},,{},,,,,,,,\n".format(REF_length, REF_privacy_sum,
                        #                                                 REF_times_of_turning_off_camera,
                        #                                                 REF_times_of_intrusion))
                        print("PP,{},{},{},{},{},"
                              "{},{},{},{},{},{},{}".format(length, privacy_sum, privacy_sum_known,
                                                            times_of_turning_off_camera, times_of_intrusion,
                                                            times_of_intrusion_known, times_of_replanning,
                                                            times_of_no_solution, times_of_flag_1,
                                                            times_of_flag_2, times_of_flag_3,
                                                            exploration_rate))
                    else:
                        if x_flag != 3:
                            if x_flag != 0:
                                csv_file.write(",,,,,,,,,,,,\n")
                            csv_file.write(",Length,PR,PR_known,turn off camera,Intrusion,Intrusion_known,replan times,"
                                           "No solution times,flag 1 times,flag 2 times,flag 3 times,"
                                           "exploration rate\n")
                        x_flag = 3
                        csv_file.write("PP,{},{},{},{},{},"
                                       "{},{},{},{},{},{},{}\n".format(length, privacy_sum, privacy_sum_known,
                                                                       times_of_turning_off_camera, times_of_intrusion,
                                                                       times_of_intrusion_known, times_of_replanning,
                                                                       times_of_no_solution, times_of_flag_1,
                                                                       times_of_flag_2, times_of_flag_3,
                                                                       exploration_rate))
                    times_of_flag_1 = 0
                    times_of_flag_2 = 0
                    times_of_flag_3 = 0
    print("The log to csv finished.")
