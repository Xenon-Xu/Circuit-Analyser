"""
    节点、各电路元件类定义
"""

from math import cos, sin, pi

nodes = list()  # 整个电路的节点列表
elements = list()  # 整个电路的元件列表

POS = "positive"  # 正端符号
NEG = "negative"  # 负端符号
INF = float("inf")  # 无限值
VS_label = ["DC_VS", "AC_VS", "C"]  # 电压元件标识
AC_label = ["AC_VS", "AC_IS"]  # 交流源标识
PWR_label = ["DC_VS", "AC_VS"]  # 电压源标识
CRT_label = ["DC_IS", "AC_IS"]  # 电流源标识
dt = 0.00001  # 时间步
start_time = 0  # 分析开始时刻
end_time = 1e+5  # 分析结束时刻
# end_time = 50  # 分析结束时刻

class AwithB():
    """一个(a, b)的向量类"""
    a = b = 0
    def __init__(self, a, b):
        self.a = a
        self.b = b

class NODES:
    """节点类定义"""

    port = set()  # 储存连接端口的集合
    voltage = 0  # 节点电压

    def __init__(self, *port_list):
        self.port = set()
        for obj in port_list:
            self.port.add(obj)
        self.voltage = 0

    def insert(self, num):
        self.port.add(num)

    def update(self, ports):
        self.port.update(ports)

    def find(self, port):
        if port in self.port:
            return True
        else:
            return False

    def ports(self):
        """返回端口的列表"""
        temp = list()
        for obj in self.port:
            temp.append(obj)
        temp.sort()
        return temp

    @staticmethod
    def is_positive(num):
        """判断连接元件端口的极性"""
        if num % 2 == 0:
            return True
        else:
            return False

    @staticmethod
    def port2element(port_num):
        """已知端口编号，求其元件在element中的编号"""
        return port_num // 2

class ELEMENT:
    """二端元件的基类"""

    num_p = num_n = -1  # 正负端口连接节点编号，-1表示未连接
    vtg_p = vtg_n = 0  # 正负端口的电压值
    crt = 0  # 由正端流入负端的电流

    def __init__(self):
        self.num_p = self.num_n = 0
        self.vtg_p = self.vtg_n = 0
        self.crt = 0
        self.feq = 0

    def connect(self, num, side):
        """元件连接标记"""
        if side == POS:
            self.num_p = num
        elif side == NEG:
            self.num_n = num

    def crt_update(self, node, timing=0):
        """更新当前时间步的电流值"""
        pass

    def vtg_update(self, timing=0):
        """更新当前时间步的电压值"""
        pass

    def clear(self):
        """恢复仿真前的零响应初状态"""
        self.vtg_n = self.vtg_p = self.crt = 0

    def reattach(self):
        """恢复连线前的状态"""
        self.clear()
        self.num_n = self.num_p = 0

class R(ELEMENT):
    """电阻元件类"""

    val = INF  # 电阻阻值
    k = 1/val  # KCL系数矩阵对应值
    label = "R"  # 电阻标识

    def __init__(self, value=INF):
        super().__init__()
        self.val = value
        self.k = 1/value

    def crt_update(self, node, timing=0):
        self.crt = (self.vtg_p - self.vtg_n) / self.val

class DC_VS(ELEMENT):
    """直流电压源类"""

    val = INF  # 供电电压值
    k = 0  # KCL系数矩阵对应值
    label = "DC_VS"  # 直流电压源标识

    def __init__(self, value=INF):
        super().__init__()
        self.val = value

    def crt_update(self, node, timing=0):
        """利用node节点处KCL方程求解电流"""
        temp = 0
        for port_num in nodes[node].ports():
            #elements[NODES.port2element(port_num)].crt_update()
            if port_num != self.num_p and port_num != self.num_n:
                if NODES.is_positive(port_num):
                    temp -= elements[NODES.port2element(port_num)].crt
                else:
                    temp += elements[NODES.port2element(port_num)].crt
        self.crt = temp

class DC_IS(ELEMENT):
    """直流电流源类"""

    val = 0  # 供电电流值
    k = 0  # KCL系数矩形对应值
    crt = -val  # 元件电流值恒定，关联参考方向相反
    label = "DC_IS"  # 直流电流源标识

    def __init__(self, value=0):
        super().__init__()
        self.val = value
        self.crt = -value

    def crt_update(self, node, timing=0):
        self.crt = -self.val

class AC_VS(ELEMENT):
    """交流电压源类"""

    val = 0  # 供电电压值
    amp = 0 # 电压幅值
    feq = 0 # 交流频率
    k = 0  # KCL系数矩阵对应值
    label = "AC_VS"  # 交流电压源标识

    def __init__(self, value=0, amp=0, feq=0):
        super().__init__()
        self.val = value
        self.amp = amp
        self.feq = feq

    def crt_update(self, node, timing=0):
        """利用node节点处KCL方程求解电流"""
        temp = 0
        for port_num in nodes[node].ports():
            if port_num != self.num_p and port_num != self.num_n:
                #elements[NODES.port2element(port_num)].crt_update()
                if NODES.is_positive(port_num):
                    temp -= elements[NODES.port2element(port_num)].crt
                else:
                    temp += elements[NODES.port2element(port_num)].crt
        self.crt = temp

    def vtg_update_AC(self, t):
        """交流电压更新"""
        self.val = self.amp * sin(2 * pi * self.feq * t)

class AC_IS(ELEMENT):
    """交流电流源类"""

    val = 0  # 供电电流值
    amp = 0 # 电流幅值
    feq = 0 # 交流频率
    k = 0  # KCL系数矩阵对应值
    label = "AC_IS"  # 交流电压源标识

    def __init__(self, value=0, amp=0, feq=0):
        super().__init__()
        self.val = value
        self.amp = amp
        self.feq = feq

    def crt_update(self, node, timing=0):
        self.crt = - self.val

    def crt_update_AC(self, t):
        """交流电流更新"""
        self.val = self.amp * sin(2 * pi * self.feq * t)

class C(ELEMENT):
    """电容类"""

    val = INF  # 电容值
    vs = 0  # 作为电压源的电压值
    k = 0  # KCL系数矩阵对应值
    sum_crt = 0  # 每个时间步的电流值总和
    label = "C"  # 电容标识

    def __init__(self, value=INF):
        super().__init__()
        self.val = value
        self.sum_crt = 0

    def crt_update(self, node, timing=0):
        """利用node节点处KCL方程求解电流"""
        temp = 0
        for port_num in nodes[node].ports():
            if port_num != self.num_p and port_num != self.num_n:
                #elements[NODES.port2element(port_num)].crt_update()
                if NODES.is_positive(port_num):
                    temp -= elements[NODES.port2element(port_num)].crt
                else:
                    temp += elements[NODES.port2element(port_num)].crt
        self.crt = temp

    def vtg_update(self, timing=0):
        """利用每个时间步的电流总和计算"""
        if timing == start_time:
            self.vs = 0
        else:
            self.vs = dt / self.val * self.sum_crt

    def clear(self):
        """清除电容的电压记忆"""
        ELEMENT.clear(self)
        self.sum_crt = 0
        self.vs = 0


class L(ELEMENT):
    """电感类"""

    val = 0  # 电感值
    cs = 0  # 作为电流源的电流值
    k = 0  # KCL系数矩阵对应值
    sum_vtg_pos = 0  # 每个时间步的正端电压值总和
    sum_vtg_neg = 0  # 每个时间步的负端电压值总和
    label = "L"  # 电感标识

    def __init__(self, value=INF):
        super().__init__()
        self.val = value
        self.sum_vtg_pos = self.sum_vtg_neg = 0

    def crt_update(self, node, timing=0):
        """利用每个时间步的电压总和计算"""
        self.crt = dt / self.val * (self.sum_vtg_pos - self.sum_vtg_neg)
        self.cs = -self.crt

    def clear(self):
        """清除电感的电流记忆"""
        ELEMENT.clear(self)
        self.sum_vtg_pos = self.sum_vtg_neg = 0
        self.cs = 0