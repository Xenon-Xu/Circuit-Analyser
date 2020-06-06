"""
    核心分析算法
"""

import numpy as np
from numba import jit
import copy
from models import *

M = 10  # 默认元件数
N = M // 2  # 默认节点数
ground = 1  # 默认地参考点
nodes_num = 0  # 节点编号自增
port_to_node = list()  # 端口对应节点列表
conM = np.zeros((2*M-N, 2*M))  # 连接矩阵
kclM = np.zeros((N, 2*M))  # KCL矩阵
cctM = np.zeros((2*M, 2*M))  # 系数矩阵
powM = np.zeros((1, 2*M))  # 电源矩阵
voltageM = np.zeros((2*M, 1))  # 电压解矩阵
voltage_list = list()  # 电压解存储列表
currentM = np.zeros((M, 1))  # 电流解矩阵
current_list = list()  # 电流解储存列表
nodes_current_update_priority = list()  # 节点KCL更新电流的优先级
ele_current_update_flag = list()  # 每个元件在每个时间步更新电流的标记
step = 0  # 分析步
temp_step = step  # 分析步的缓冲
analyzing_stop = False  # 停止分析标志
timing = 0  # 时间记录
lzy = 1000000  # 防止爆内存
lzy_times = 0  # 膜lzy的次数

def extract_voltage_answer(part, length_x = 100, interval=1000):
    """利用分析步，将某端口的电压，导出为一定长度的列表"""
    temp_voltage = list()
    global temp_step
    temp_step = step  # 防止step不断变化
    if temp_step < interval:
            temp_voltage.append(0.0)
    elif interval <= temp_step < length_x:  # 分析数据画不完一张图
        for i in range(0, temp_step, interval):
            temp_voltage.append(voltage_list[i][part, 0])
    else:  # 动态波形
        for i in range(temp_step-length_x, temp_step, interval):
            temp_voltage.append(voltage_list[i][part, 0])

    return temp_voltage

def layout_initializing(M_set):
    """电路全局初始化"""
    global  port_to_node, M
    M = M_set
    port_to_node = [-1 for i in range(2*M)]

def layout_remove():
    """清空电路布局"""
    global nodes_num
    nodes.clear()
    elements.clear()
    nodes_num = 0

def restart():
    """使电路恢复仿真前状态"""
    global lzy_times
    lzy_times = 0
    for ele in elements:
        ele.clear()

def reattach():
    """使电路恢复连线前状态"""
    global nodes_num, port_to_node
    for ele in elements:
        ele.reattach()
    nodes.clear()
    nodes_num = 0
    port_to_node = [-1 for i in range(2 * M)]
    nodes_current_update_priority.clear()
    ele_current_update_flag.clear()


def ele_current_update_flag_clear():
    """电流更新标记清除"""
    ele_current_update_flag.clear()
    for i in range(len(elements)):
        ele_current_update_flag.append(False)

def connect_matrix_initializing():
    """连接矩阵初始化"""
    global conM, N
    N = len(nodes)  # 注意，N在这里已经改变
    conM = np.zeros((2*M-N, 2*M))

def KCL_matrix_initializing():
    """KCL矩阵初始化"""
    global kclM
    kclM = np.zeros((N, 2*M))

def power_matrix_initializing():
    """电源矩阵初始化"""
    global powM
    powM = np.zeros((2*M, 1))

def voltage_matrix_initializing():
    """电压解矩阵初始化，加入零状态响应"""
    voltage_list.clear()
    global voltageM
    voltageM = np.zeros((2*M, 1))
    voltage_list.append(copy.copy(voltageM))

def current_matrix_initializing():
    """电流解矩阵初始化，加入零状态响应"""
    current_list.clear()
    global currentM
    currentM = np.zeros((M, 1))
    current_list.append(copy.copy(currentM))

def construct_coefficient_matrix():
    """构建系数矩阵"""
    global  cctM
    cctM = np.row_stack((kclM, conM))

def place_elements(**cnf):
    """放置元件"""
    if "R" in cnf:
        elements.append(R(cnf["R"]))
    elif "DC_VS" in cnf:
        elements.append(DC_VS(cnf["DC_VS"]))
    elif "DC_IS" in cnf:
        elements.append(DC_IS(cnf["DC_IS"]))
    elif "AC_VS" in cnf:
        elements.append(AC_VS(cnf["AC_VS"], cnf["A"], cnf["f"]))
    elif "AC_IS" in cnf:
        elements.append(AC_IS(cnf["AC_IS"], cnf["A"], cnf["f"]))
    elif "C" in cnf:
        elements.append(C(cnf["C"]))
    elif "L" in cnf:
        elements.append(L(cnf["L"]))

def modify_element(ele_num, val, frq=0):
    """修改元件值"""
    ele =  elements[ele_num]
    if ele.label in AC_label:
        ele.__init__(0, val, frq)
    else:
        ele.__init__(val)

def connecting(port_num1, port_num2):
    """连接元件，包括更新元件标记，创建节点对象"""
    global nodes_num
    elements_num1 = NODES.port2element(port_num1)  # 元件1
    elements_num2 = NODES.port2element(port_num2)  # 元件2
    if port_to_node[port_num1] == -1 and port_to_node[port_num2] == -1:  # 若两个端口都未连接
        port_to_node[port_num1] = port_to_node[port_num2] = nodes_num  # 加入一个集合中
        nodes.append(NODES(port_num1, port_num2))  # 创建一个节点对象
        if NODES.is_positive(port_num1):
            elements[elements_num1].num_p = nodes_num
        else:
            elements[elements_num1].num_n = nodes_num
        if NODES.is_positive(port_num2):
            elements[elements_num2].num_p = nodes_num
        else:
            elements[elements_num2].num_n = nodes_num
        nodes_num += 1
    else:
        if port_to_node[port_num1] == -1:  # 若端口1悬空
            nodes[port_to_node[port_num2]].insert(port_num1)  # 在端口2连接的节点中添加端口1
            port_to_node[port_num1] = port_to_node[port_num2]  # 端口1并入端口2的节点的集合中
            if NODES.is_positive(port_num1):
                elements[elements_num1].num_p = port_to_node[port_num2]
            else:
                elements[elements_num1].num_n = port_to_node[port_num2]
        elif port_to_node[port_num2] == -1:  # 若端口2悬空
            nodes[port_to_node[port_num1]].insert(port_num2)  # 在端口1连接的节点中添加端口2
            port_to_node[port_num2] = port_to_node[port_num1]  # 端口2并入端口1的节点的集合中
            if NODES.is_positive(port_num2):
                elements[elements_num2].num_p = port_to_node[port_num1]
            else:
                elements[elements_num2].num_n = port_to_node[port_num1]
        else:  # 端口属于不同的节点
            nodes[port_to_node[port_num1]].update(nodes[port_to_node[port_num2]].port)  # 在端口1连接的节点中添加端口2的节点连接的所有端口
            temp_list = nodes[port_to_node[port_num2]].ports()
            del nodes[port_to_node[port_num2]]  # 删除端口2之前的节点
            for i in temp_list:
                port_to_node[i] = port_to_node[port_num1]  # 端口2节点的所有端口并入端口1的节点的集合中
                if NODES.is_positive(i):
                    elements[NODES.port2element(i)].num_p = port_to_node[port_num1]
                else:
                    elements[NODES.port2element(i)].num_n = port_to_node[port_num1]
            nodes_num -= 1

def KCL_priority():  # 根据电压元件的多少决定KCL更新电流顺序的优先级
    num_vs = list()  # 记录各个节点中电压元件的数量的列表
    for i in range(len(nodes)):
        cnt = 0  # 记录每个节点的电压元件数量
        for j in nodes[i].ports():
            ele = elements[NODES.port2element(j)]
            if ele.label in VS_label:
                cnt += 1
        num_vs.append(AwithB(i, cnt))
    num_vs.sort(key=lambda x: x.b)
    for i in num_vs:
        nodes_current_update_priority.append(i.a)


def construct_connect_matrix():
    """构建连接矩阵"""
    colunm = 0  # 自增行变量
    global conM
    for i in range(len(nodes)):
        temp_list = nodes[i].ports()
        for j in range(1, len(temp_list)):
            conM[i + colunm, temp_list[0]] = 1
            conM[i + colunm, temp_list[j]] = -1
            colunm += 1
        colunm -= 1

def construct_kcl_matrix():
    """构建KCL矩阵"""
    global kclM
    for i in range(len(nodes)):
        for j in nodes[i].ports():
            ele = elements[NODES.port2element(j)]  #  元件读取
            if ele.label == 'R':
                if NODES.is_positive(j):
                    kclM[i, j] = ele.k
                    kclM[i, j + 1] = -ele.k
                else:
                    kclM[i, j - 1] = -ele.k
                    kclM[i, j] = ele.k

def construct_power_matrix(timing):
    """在每一个时间步上构建电源矩阵，并更新电感的记忆值，更新交流电流源的电流值"""
    global powM
    for i in range(len(nodes)):
        sum_pow = 0  # 电流源的总和
        for j in nodes[i].ports():
            ele = elements[NODES.port2element(j)]  # 元件读取
            if ele.label == 'DC_IS' or ele.label == 'AC_IS':
                if ele.label == 'AC_IS':
                    ele.crt_update_AC(timing)
                if NODES.is_positive(j):
                    sum_pow += ele.val
                else:
                    sum_pow += -ele.val
            elif ele.label == 'L':
                ele.sum_vtg_pos += ele.vtg_p
                ele.sum_vtg_neg += ele.vtg_n
                ele.crt_update(0)
                if NODES.is_positive(j):
                    sum_pow += ele.cs
                else:
                    sum_pow += -ele.cs
        powM[i, 0] = sum_pow

def matrix_reconstruct_add_KVL(timing=0):
    """根据电路中的电压源、电容，合并KCL方程，并增加KVL方程，更新电容记忆值，更新交流电压源的电压值"""
    conbine_nodes = list()  # 记录要合并的节点
    global kclM, powM
    for i in range(len(elements)):
        ele = elements[i]
        if ele.label == 'DC_VS' or ele.label == 'AC_VS' or ele.label == 'C':
            pair_set = {ele.num_n, ele.num_p}
            pair_flag = -1
            for j in range(len(conbine_nodes)):
                exist_pair = conbine_nodes[j]
                if (exist_pair & pair_set) != set():
                    pair_flag = j
                    break
            if ele.label == 'AC_VS':  # 更新交流电压源的电压值
                ele.vtg_update_AC(timing)
            if ele.label == 'C':  # 更新电容的记忆
                ele.sum_crt += ele.crt
                ele.vtg_update(timing)
            if pair_flag == -1:
                conbine_nodes.append(copy.copy(pair_set))
            else:
                conbine_nodes[pair_flag] |= pair_set

    for exist_pair in conbine_nodes:  # 将许多方程合并成一个KCL方程，并增加若干KVL方程
        pair_list = list()
        for i in exist_pair:
            pair_list.append(i)
        for i in range(1, len(pair_list)):
            for j in range(2 * M):
                kclM[pair_list[0], j] += kclM[pair_list[i], j]
                kclM[pair_list[i], j] = 0
            powM[pair_list[0], 0] += powM[pair_list[i], 0]
            vs = 0
            p_part = n_part = 0
            for j in range(len(elements)):
                ele = elements[j]
                if ele.label == 'DC_VS' or ele.label == 'AC_VS' or ele.label == 'C':
                    if ele.num_p in pair_list and ele.num_n in pair_list:
                        if  ele.num_p == pair_list[i] or ele.num_n == pair_list[i]:
                            p_part = j * 2
                            n_part = j * 2 + 1
                            if ele.label == 'C':
                                vs = ele.vs
                            else:
                                vs = ele.val
                            break
            powM[pair_list[i], 0] = vs
            kclM[pair_list[i], p_part] = 1
            kclM[pair_list[i], n_part] = -1

def matrix_reconstruct_del():
    """根据地参考点选取，删除矩阵中的已知量"""
    global cctM
    del_list = list()
    for port_num in nodes[port_to_node[ground]].ports():
        voltageM[port_num, 0] = 0
        if NODES.is_positive(port_num):  # 同步更新元件对象的端口电压值
            elements[NODES.port2element(port_num)].vtg_p = 0
        else:
            elements[NODES.port2element(port_num)].vtg_n = 0
        del_list.append(port_num)
    cctM = np.delete(cctM, del_list, axis=1)

@jit(nopython=True)
def p_inv(mat):
    """求解广义逆加速"""
    return np.linalg.pinv(mat)

def analyzing(times):
    """求解各个电压、电流"""
    global voltageM
    temp_voltage = np.dot(p_inv(cctM), powM)
    j = 0
    for i in range(2*M):
        if not nodes[port_to_node[ground]].find(i):
            voltageM[i, 0] = temp_voltage[j, 0]
            if NODES.is_positive(i):  # 同步更新元件对象的端口电压值
                elements[NODES.port2element(i)].vtg_p = voltageM[i, 0]
            else:
                elements[NODES.port2element(i)].vtg_n = voltageM[i, 0]
            j += 1
    voltage_list.append(copy.copy(voltageM))  # 存储当前时间步电压解
    for i in range(len(elements)):  # 更新电阻的电流值
        ele = elements[i]
        if ele.label == 'R' or ele.label == 'DC_IS' or ele.label == 'AC_IS':
            ele.crt_update(0)
            ele_current_update_flag[i] = True
    for i in nodes_current_update_priority:  # 根据优先级更新节点处的元件电流
        for j in nodes[i].ports():
            if not ele_current_update_flag[NODES.port2element(j)]:  # 如果没有更新，则更新
                ele = elements[NODES.port2element(j)]
                ele.crt_update(i, times)
                ele_current_update_flag[NODES.port2element(j)] = True
    current_list.append(copy.copy(currentM))  # 存储当前时间步电流解

def vibration_elimination():
    """消振，非常重要"""
    if step < 5 or step % 2 == 1:
        return
    voltage_list[step - 1] = (voltage_list[step - 2] + voltage_list[step]) / 2
    current_list[step - 1] = (current_list[step - 2] + current_list[step]) / 2


def main_initializing(gnd):
    """电路分析初始化"""
    global ground, step
    ground = gnd
    step = 0

    KCL_priority()  # KCL方程优先级预处理

    connect_matrix_initializing()  # 连接矩阵初始化
    construct_connect_matrix()  # 构建连接矩阵

    KCL_matrix_initializing()  # KCL矩阵初始化
    construct_kcl_matrix()  # 构建KCL矩阵

    power_matrix_initializing()  # 电源矩阵初始化
    construct_power_matrix(start_time)  # 构建电源矩阵

    voltage_matrix_initializing()  # 电压解矩阵初始化
    current_matrix_initializing()  # 电流解矩阵初始化

    matrix_reconstruct_add_KVL()  # 重构KCL矩阵，添加KVL方程
    construct_coefficient_matrix()  # 合并KCL矩阵与连接矩阵为系数矩阵

    matrix_reconstruct_del()  # 这里以ground端口为地，整理整个矩阵表达式

def main_analyzing():
    """电路分析主程序"""
    global analyzing_stop, timing

    for times in range(int((end_time - start_time) / dt)):

        if analyzing_stop:  # 结束标志判断
            analyzing_stop = False
            return

        timing = times * dt + start_time  # 时间记录
        ele_current_update_flag_clear()  # 清除电流更新标记
        analyzing(times)
        vibration_elimination()  # 消振

        global step, lzy_times
        step += 1
        if step >= lzy:
            lzy_times += 1
            step %= lzy  # 膜大佬，乞求防爆内存
            voltage_matrix_initializing()  # 电压解矩阵清空
            current_matrix_initializing()  # 电流解矩阵清空

        if times == int((end_time - start_time) / dt) - 1:
            break

        power_matrix_initializing()  # 电源矩阵初始化
        construct_power_matrix(timing)  # 构建电源矩阵

        KCL_matrix_initializing()  # KCL矩阵初始化
        construct_kcl_matrix()  # 构建KCL矩阵

        matrix_reconstruct_add_KVL(timing)  # 重构KCL矩阵，添加KVL方程
        construct_coefficient_matrix()  # 合并KCL矩阵与连接矩阵为系数矩阵

        matrix_reconstruct_del()  # 整理整个矩阵表达式

if __name__ == '__main__':
    layout_remove()

    place_elements(AC_VS=0, A=10, f=5)  # 放置元件
    place_elements(R=10)
    place_elements(C=0.1)

    layout_initializing(3)  # 3代表元件数，以确定矩阵的大小

    connecting(0, 2)  # 连接端口
    connecting(3, 4)
    connecting(5, 1)

    main_initializing(1)  # 分析初始化，并选取参考地端口
    end_time = 0.2
    main_analyzing()  # 开始分析
    #
    # print(port_to_node)
    # for i in elements:
    #     print("elements", i.num_p, i.num_n)
    # for i in nodes:
    #     print("nodes", i.ports())
    #
    # print("pow", powM.T)
    # print(nodes_current_update_priority)
    #
    # file = open(r"temp.csv", 'w')
    for i in range(len(voltage_list)):
         print(voltage_list[i][0, 0], voltage_list[i][4, 0])
    #     file.write('{}\n'.format(current_list[i][2, 0]))
    # file.close()