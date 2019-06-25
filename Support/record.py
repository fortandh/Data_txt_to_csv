#!/usr/bin/python


class Record(object):
    """记录csv表格中的一行

    Attributes:
        length: 规划的长度
        PR: 侵犯隐私数量的总和
        times_of_turning_off_camera: 关闭camera的次数
        times_of_intrusion: 侵犯隐私的数量
        times_of_replanning: 重规划的数量
        exploration_rate: 探索率
    """
    def __init__(self, length, PR, times_of_turning_off_camera, times_of_intrusion,
                 times_of_replanning, exploration_rate):
        self.length = length
        self.PR = PR
        self.times_of_turning_off_camera = times_of_turning_off_camera
        self.times_of_intrusion = times_of_intrusion
        self.times_of_replanning = times_of_replanning
        self.exploration_rate = exploration_rate

    def __str__(self):
        return (str(self.length)+', ' + str(self.PR) + ', ' + str(self.times_of_replanning) + ', ' +
                str(self.times_of_intrusion) + ', ' + str(self.times_of_replanning) + ', ' +
                str(self.exploration_rate))
