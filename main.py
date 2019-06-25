#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re

file_name_to_open = "data1.log"
file_name_to_write = "rslt.csv"

if __name__ == '__main__':
    REF_length = None
    REF_privacy_sum = None
    REF_times_of_turning_off_camera = None
    REF_times_of_intrusion = None

    length = None
    privacy_sum = None
    times_of_turning_off_camera = None
    times_of_intrusion = None
    times_of_replanning = None
    exploration_rate = None

    # x_flag 表示输出的类型
    # 0：输出表头
    # 1：输出Hybrid
    # 2：输出SC
    # 3：输出PP
    x_flag = 0

    with open(file_name_to_open, 'r') as log_file:
        with open(file_name_to_write, "w+") as csv_file:
            for line in log_file:
                # 匹配如下内容：
                # [2019-06-23 12:14:59,381] MainFunc.py-><module> line:64 [INFO]Iteration: 0;
                # Configuration: grid: 10, safety_threshold: 0.200000, privacy_threshold: 0.050000,
                # the starting point: [0, 0, 0]; the end point: [9, 9, 9]; T_budget(alpha): 54.000000 (2.000000);
                # T_optimal(beta): 40.500000 (1.500000)
                pattern = re.compile(r'.*MainFunc.py.*Iteration:.*; Configuration: grid: (\d+), '
                                     r'safety_threshold: (\d+.\d+), privacy_threshold: (\d+.\d+), '
                                     r'the starting point: \[(\d+), (\d+), (\d+)\]; '
                                     r'the end point: \[(\d+), (\d+), (\d+)\]; '
                                     r'T_budget\(alpha\): (\d+.\d+) .*; T_optimal\(beta\): (\d+.\d+).*; '
                                     r'Exploration_rate: (\d+.\d+).*')
                result = pattern.findall(line)
                if result:
                    if x_flag != 0:
                        # print(",,,,,,,,,")
                        csv_file.write(",,,,,,,,,,\n")
                    x_flag = 0
                    # print("gridX,girdY,girdZ,safety_threshold,privacy_threshold,"
                    #       "starting_point,end_point,idealtime,T_budget,T_optimal,Exploration rate")
                    csv_file.write("gridX,girdY,girdZ,safety_threshold,privacy_threshold,"
                                   "starting_point,end_point,idealtime,T_budget,T_optimal,Exploration rate\n")
                    result = result[0]
                    # print("{},{},{},{},{},\"{},{},{}\",\"{},{},{}\",{},{},{},{}".format(result[0], result[0], result[0],
                    #                                                                     result[1], result[2],
                    #                                                                     result[3], result[4], result[5],
                    #                                                                     result[6], result[7], result[8],
                    #                                                                     (int(result[0]) - 1) * 3,
                    #                                                                     result[9], result[10],
                    #                                                                     result[11]))
                    csv_file.write("{},{},{},{},{},\"{},{},{}\",\"{},{},{}\",{},{},{},{}\n".format(result[0], result[0],
                                                                                                   result[0], result[1],
                                                                                                   result[2], result[3],
                                                                                                   result[4], result[5],
                                                                                                   result[6], result[7],
                                                                                                   result[8],
                                                                                                   (int(result[0])-1)*3,
                                                                                                   result[9],result[10],
                                                                                                   result[11]))
                    # print(",,,,,,,,,,")
                    csv_file.write(",,,,,,,,,,\n")

                # 匹配如下内容：
                # [2019-06-23 12:18:30,760] HybridPlanningOnline.py->Astar_Hybrid_Planning_online line:665
                # [INFO]Online_Hybrid_Planning: Length of replanned trajectory: 41
                pattern = re.compile(r'.*HybridPlanningOnline.py.*Online_Hybrid_Planning: '
                                     r'Length of replanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    length = result[0]

                # 匹配如下内容：
                # [2019-06-23 12:18:30,760] HybridPlanningOnline.py->Astar_Hybrid_Planning_online line:666
                # [INFO]Online_Hybrid_Planning: Sum of privacy threat of replanned trajectory: 1008.809349
                pattern = re.compile(r'.*HybridPlanningOnline.py.*Online_Hybrid_Planning: '
                                     r'Sum of privacy threat of replanned trajectory: (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    privacy_sum = result[0]

                # 匹配如下内容：
                # [2019-06-23 12:18:30,760] HybridPlanningOnline.py->Astar_Hybrid_Planning_online line:667
                # [INFO]Online_Hybrid_Planning: Times of turning off camera of replanned trajectory: 14
                pattern = re.compile(r'.*HybridPlanningOnline.py.*Online_Hybrid_Planning: '
                                     r'Times of turning off camera of replanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_turning_off_camera = result[0]

                # 匹配如下内容：
                # [2019-06-23 12:18:30,760] HybridPlanningOnline.py->Astar_Hybrid_Planning_online line:668
                # [INFO]Online_Hybrid_Planning: Times of intrusion of replanned trajectory: 24
                pattern = re.compile(r'.*HybridPlanningOnline.py.*Online_Hybrid_Planning: '
                                     r'Times of intrusion of replanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_intrusion = result[0]

                # 匹配如下内容：
                # [2019-06-23 12:18:30,760] HybridPlanningOnline.py->Astar_Hybrid_Planning_online line:682
                # [INFO]Online_Hybrid_Planning: Length of preplanned trajectory: 27
                pattern = re.compile(r'.*HybridPlanningOnline.py.*Online_Hybrid_Planning: '
                                     r'Length of preplanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_length = result[0]

                # 匹配如下内容：
                # [2019-06-23 12:18:30,761] HybridPlanningOnline.py->Astar_Hybrid_Planning_online line:683
                # [INFO]Online_Hybrid_Planning: Sum of privacy threat of preplanned trajectory: 1493.081372
                pattern = re.compile(r'.*HybridPlanningOnline.py.*Online_Hybrid_Planning: '
                                     r'Sum of privacy threat of preplanned trajectory: (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_privacy_sum = result[0]

                # 匹配如下内容：
                # [2019-06-23 12:18:30,761] HybridPlanningOnline.py->Astar_Hybrid_Planning_online line:684
                # [INFO]Online_Hybrid_Planning: Times of turning off camera of preplanned trajectory: 0
                pattern = re.compile(r'.*HybridPlanningOnline.py.*Online_Hybrid_Planning: '
                                     r'Times of turning off camera of preplanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_times_of_turning_off_camera = result[0]

                # 匹配如下内容：
                # [2019-06-23 12:18:30,761] HybridPlanningOnline.py->Astar_Hybrid_Planning_online line:685
                # [INFO]Online_Hybrid_Planning: Times of intrusion of preplanned trajectory: 20
                pattern = re.compile(r'.*HybridPlanningOnline.py.*Online_Hybrid_Planning: '
                                     r'Times of intrusion of preplanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_times_of_intrusion = result[0]

                # 匹配如下内容：
                # [2019-06-23 12:18:30,761] HybridPlanningOnline.py->Astar_Hybrid_Planning_online line:701
                # [INFO]Online_Hybrid_Planning: Replanning times: 7
                pattern = re.compile(r'.*HybridPlanningOnline.py.*Online_Hybrid_Planning: '
                                     r'Replanning times: (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_replanning = result[0]

                # 匹配如下内容：
                # [2019-06-23 12:18:30,770] HybridPlanningOnline.py->Astar_Hybrid_Planning_online line:731
                # [INFO]Online_Hybrid_Planning: Exploration rate: 0.320000
                pattern = re.compile(r'.*HybridPlanningOnline.py.*Online_Hybrid_Planning: '
                                     r'Exploration rate: (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    exploration_rate = result[0]
                    if x_flag != 1:
                        if x_flag != 0:
                            # print(",,,,,,,,,")
                            csv_file.write(",,,,,,,,,\n")
                        # print(",Length,PR,turn off camera,Intrudsion,replan times,exploration rate,,,")
                        csv_file.write(",Length,PR,turn off camera,Intrudsion,replan times,exploration rate,,,\n")
                    x_flag = 1
                    # print("REF,{},{},,{},,,,,,".format(REF_length, REF_privacy_sum, REF_times_of_turning_off_camera,
                    #                                    REF_times_of_intrusion))
                    # csv_file.write("REF,{},{},,{},,,,,,\n".format(REF_length, REF_privacy_sum,
                    #                                               REF_times_of_turning_off_camera,
                    #                                               REF_times_of_intrusion))
                    # print("Hybrid,{},{},{},{},{},{},,,,".format(length, privacy_sum, times_of_turning_off_camera,
                    #                                             times_of_intrusion, times_of_replanning,
                    #                                             exploration_rate))
                    csv_file.write("Hybrid,{},{},{},{},{},{},,,,\n".format(length, privacy_sum,
                                                                           times_of_turning_off_camera,
                                                                           times_of_intrusion, times_of_replanning,
                                                                           exploration_rate))
                # 匹配如下内容：
                # [2019-06-23 12:21:37,778] SensorConfigOnline.py->Astar_Sensor_Config_online line:523
                # [INFO]Online_Sensor_Config: Length of replanned trajectory: 27
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Length of replanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    length = result[0]

                # 匹配如下内容
                # [2019-06-23 12:21:37,778] SensorConfigOnline.py->Astar_Sensor_Config_online line:524
                # [INFO]Online_Sensor_Config: Sum of privacy threat of replanned trajectory: 835.713663
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Sum of privacy threat of replanned trajectory: (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    privacy_sum = result[0]

                # 匹配如下内容：
                # [2019-06-23 12:21:37,779] SensorConfigOnline.py->Astar_Sensor_Config_online line:525
                # [INFO]Online_Sensor_Config: Times of turning off camera of replanned trajectory: 14
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Times of turning off camera of replanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_turning_off_camera = result[0]

                # 匹配如下内容：
                # [2019-06-23 12:21:37,779] SensorConfigOnline.py->Astar_Sensor_Config_online line:526
                # [INFO]Online_Sensor_Config: Times of intrusion of replanned trajectory: 20
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Times of intrusion of replanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_intrusion = result[0]

                # 匹配如下内容：
                # [2019-06-23 12:21:37,779] SensorConfigOnline.py->Astar_Sensor_Config_online line:540
                # [INFO]Online_Sensor_Config: Length of preplanned trajectory: 27
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Length of preplanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_length = result[0]
                # 匹配如下内容
                # [2019-06-23 12:21:37,779] SensorConfigOnline.py->Astar_Sensor_Config_online line:541
                # [INFO]Online_Sensor_Config: Sum of privacy threat of preplanned trajectory: 1493.081372
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Sum of privacy threat of preplanned trajectory: (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_privacy_sum = result[0]

                # 匹配如下内容：
                # [2019-06-23 12:21:37,779] SensorConfigOnline.py->Astar_Sensor_Config_online line:542
                # [INFO]Online_Sensor_Config: Times of turning off camera of preplanned trajectory: 0
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Times of turning off camera of preplanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_times_of_turning_off_camera = result[0]

                # 匹配如下内容：
                # [2019-06-23 12:21:37,779] SensorConfigOnline.py->Astar_Sensor_Config_online line:543
                # [INFO]Online_Sensor_Config: Times of intrusion of preplanned trajectory: 20
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Times of intrusion of preplanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_times_of_intrusion = result[0]

                # 匹配如下内容：
                # [2019-06-23 12:21:37,779] SensorConfigOnline.py->Astar_Sensor_Config_online line:555
                # [INFO]Online_Sensor_Config: Replanning times: 8
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Replanning times: (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_replanning = result[0]

                # 匹配如下内容：
                # [2019-06-23 12:21:37,788] SensorConfigOnline.py->Astar_Sensor_Config_online line:585
                # [INFO]Online_Sensor_Config: Exploration rate: 0.240000
                pattern = re.compile(r'.*SensorConfigOnline.py.*Online_Sensor_Config: '
                                     r'Exploration rate: (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    exploration_rate = result[0]
                    if x_flag != 2:
                        if x_flag != 0:
                            # print(",,,,,,,,,")
                            csv_file.write(",,,,,,,,,\n")
                        # print(",Length,PR,turn off camera,Intrudsion,replan times,exploration rate,,,")
                        csv_file.write(",Length,PR,turn off camera,Intrudsion,replan times,exploration rate,,,\n")
                    x_flag = 2
                    # print("REF,{},{},,{},,,,,,".format(REF_length, REF_privacy_sum, REF_times_of_turning_off_camera,
                    #                                    REF_times_of_intrusion))
                    # csv_file.write("REF,{},{},,{},,,,,,\n".format(REF_length, REF_privacy_sum,
                    #                                               REF_times_of_turning_off_camera,
                    #                                               REF_times_of_intrusion))
                    # print("SC,{},{},{},{},{},{},,,,".format(length, privacy_sum, times_of_turning_off_camera,
                    #                                         times_of_intrusion, times_of_replanning,
                    #                                         exploration_rate))
                    csv_file.write("SC,{},{},{},{},{},{},,,,\n".format(length, privacy_sum, times_of_turning_off_camera,
                                                                       times_of_intrusion, times_of_replanning,
                                                                       exploration_rate))

                # 匹配如下内容：
                # [2019-06-23 12:25:57,585] PathPlanningOnline.py->Astar_Path_Planning_online line:633
                # [INFO]Online_Path_Planning: Length of replanned trajectory: 43
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Length of replanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    length = result[0]

                # 匹配如下内容：
                # [2019-06-23 12:25:57,585] PathPlanningOnline.py->Astar_Path_Planning_online line:634
                # [INFO]Online_Path_Planning: Sum of privacy threat of replanned trajectory: 1528.279368
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Sum of privacy threat of replanned trajectory: (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    privacy_sum = result[0]

                # 匹配如下内容：
                # [2019-06-23 12:25:57,585] PathPlanningOnline.py->Astar_Path_Planning_online line:635
                # [INFO]Online_Path_Planning: Times of turning off camera of replanned trajectory: 0
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Times of turning off camera of replanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_turning_off_camera = result[0]

                # 匹配如下内容：
                # [2019-06-23 12:25:57,585] PathPlanningOnline.py->Astar_Path_Planning_online line:636
                # [INFO]Online_Path_Planning: Times of intrusion of replanned trajectory: 25
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Times of intrusion of replanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_intrusion = result[0]

                # 匹配如下内容：
                # [2019-06-23 12:25:57,585] PathPlanningOnline.py->Astar_Path_Planning_online line:649
                # [INFO]Online_Path_Planning: Length of preplanned trajectory: 27
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Length of preplanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_length = result[0]

                # 匹配如下内容：
                # [2019-06-23 12:25:57,585] PathPlanningOnline.py->Astar_Path_Planning_online line:650
                # [INFO]Online_Path_Planning: Sum of privacy threat of preplanned trajectory: 1493.081372
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Sum of privacy threat of preplanned trajectory: (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_privacy_sum = result[0]

                # 匹配如下内容：
                # [2019-06-23 12:25:57,585] PathPlanningOnline.py->Astar_Path_Planning_online line:651
                # [INFO]Online_Path_Planning: Times of turning off camera of preplanned trajectory: 0
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Times of turning off camera of preplanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_times_of_turning_off_camera = result[0]

                # 匹配如下内容：
                # [2019-06-23 12:25:57,586] PathPlanningOnline.py->Astar_Path_Planning_online line:652
                # [INFO]Online_Path_Planning: Times of intrusion of preplanned trajectory: 20
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Times of intrusion of preplanned trajectory: (\d+),*')
                result = pattern.findall(line)
                if result:
                    REF_times_of_intrusion = result[0]

                # 匹配如下内容：
                # [2019-06-23 12:25:57,586] PathPlanningOnline.py->Astar_Path_Planning_online line:664
                # [INFO]Online_Path_Planning: Replanning times: 17
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Replanning times: (\d+),*')
                result = pattern.findall(line)
                if result:
                    times_of_replanning = result[0]

                # 匹配如下内容：
                # [2019-06-23 12:25:57,593] PathPlanningOnline.py->Astar_Path_Planning_online line:694
                # [INFO]Online_Path_Planning: Exploration rate: 0.370000
                pattern = re.compile(r'.*PathPlanningOnline.py.*Online_Path_Planning: '
                                     r'Exploration rate: (\d+.\d+),*')
                result = pattern.findall(line)
                if result:
                    exploration_rate = result[0]
                    if x_flag != 3:
                        if x_flag != 0:
                            # print(",,,,,,,,,")
                            csv_file.write(",,,,,,,,,\n")
                        # print(",Length,PR,turn off camera,Intrudsion,replan times,exploration rate,,,")
                        csv_file.write(",Length,PR,turn off camera,Intrudsion,replan times,exploration rate,,,\n")
                    x_flag = 3
                    # print("REF,{},{},,{},,,,,,".format(REF_length, REF_privacy_sum, REF_times_of_turning_off_camera,
                    #                                    REF_times_of_intrusion))
                    # csv_file.write("REF,{},{},,{},,,,,,\n".format(REF_length, REF_privacy_sum,
                    #                                               REF_times_of_turning_off_camera,
                    #                                               REF_times_of_intrusion))
                    # print("PP,{},{},{},{},{},{},,,,".format(length, privacy_sum, times_of_turning_off_camera,
                    #                                         times_of_intrusion, times_of_replanning,
                    #                                         exploration_rate))
                    csv_file.write("PP,{},{},{},{},{},{},,,,\n".format(length, privacy_sum, times_of_turning_off_camera,
                                                                       times_of_intrusion, times_of_replanning,
                                                                       exploration_rate))
