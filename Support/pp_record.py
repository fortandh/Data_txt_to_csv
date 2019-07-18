from Support.record import Record


class PP_Record(Record):
    """记录csv表格中的PP的一行

    Attributes:
        length: 规划的长度
        PR: 侵犯隐私影响的总和
        PR_known: 侵犯已知隐私影响的总和
        times_of_turning_off_camera: 关闭camera的次数
        times_of_intrusion: 侵犯隐私的数量
        times_of_intrusion_known: 侵犯已知隐私的数量
        times_of_replanning: 重规划的数量
        times_of_no_solution: 规划失败的次数
        times_of_flag_1: 规划失败时，错误标志为1的次数
        times_of_flag_2: 规划失败时，错误标志为2的次数
        times_of_flag_3: 规划失败时，错误标志为3的次数
        exploration_rate: 探索率
        execution_time: 执行时间
    """
    def __init__(self, length, PR, PR_known, times_of_turning_off_camera, times_of_intrusion, times_of_intrusion_known,
                 times_of_replanning, times_of_no_solution, times_of_flag_1, times_of_flag_2, times_of_flag_3,
                 exploration_rate, execution_time):
        super().__init__(length, PR, PR_known, times_of_turning_off_camera, times_of_intrusion,
                         times_of_intrusion_known, times_of_replanning, exploration_rate, execution_time)
        self.times_of_no_solution = times_of_no_solution
        self.times_of_flag_1 = times_of_flag_1
        self.times_of_flag_2 = times_of_flag_2
        self.times_of_flag_3 = times_of_flag_3

    def __str__(self):
        return (str(self.length) + ', ' + str(self.PR) + ', ' + str(self.PR_known) + ', ' +
                str(self.times_of_turning_off_camera) + ', ' + str(self.times_of_intrusion) + ', ' +
                str(self.times_of_intrusion_known) + ', ' + str(self.times_of_replanning) + ', ' +
                str(self.times_of_no_solution) + ', ' + str(self.times_of_flag_1) + ', ' +
                str(self.times_of_flag_2) + ', ' + str(self.times_of_flag_3) + ', ' +
                str(self.exploration_rate) + ', ' + str(self.execution_time))
