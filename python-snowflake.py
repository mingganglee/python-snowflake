import const
import time

# 每一部分占用的位数
const.TIMESTAMP_BIT = 41 # 时间戳占用位数
const.SEQUENCE_BIT = 5 # 序列号占用的位数
const.MACHINE_BIT = 5 # 机器标识占用的位数
const.DATACENTER_BIT = 12 # 数据中心占用的位数

# 每一部分的最大值
const.MAX_DATACENTER_NUM = -1 ^ (-1 << const.DATACENTER_BIT)
const.MAX_MACHINE_NUM = -1 ^ (-1 << const.MACHINE_BIT)
const.MAX_SEQUENCE = -1 ^ (-1 << const.SEQUENCE_BIT)

# 每一部分向左的位移
const.MACHINE_LEFT = const.SEQUENCE_BIT
const.DATACENTER_LEFT = const.SEQUENCE_BIT + const.MACHINE_BIT
const.TIMESTMP_LEFT = const.DATACENTER_LEFT + const.DATACENTER_BIT

class TimeGenerator(object):

    class SnowflakeOverflowError(TypeError):
        """
        分布式ID生成算法占位符溢出异常，会导致生成ID为负数
        """
        pass

    class RuntimeError(TypeError):
        """
        运行时间错误，在此项目中当前运行时间小于上一次运行时间。出现此错误一般是本地时间呗修改
        """
        pass

    def __init__(self):
        if const.TIMESTAMP_BIT + \
           const.SEQUENCE_BIT + \
           const.MACHINE_BIT + \
           const.DATACENTER_BIT != 63:
        	raise self.SnowflakeOverflowError("TIMESTAMP_BIT + SEQUENCE_BIT + MACHINE_BIT + DATACENTER_BIT not equal to 63bit")
        self.datacenterId = 0 # 数据中心编号
        self.machineId = 0 # 机器标示编号
        self.sequence = 0 # 序列号
        self.last_stmp = -1  # 上一次时间戳



    def nextID(self):
        curr_stmp = self.getNewstmp()
        if curr_stmp < self.last_stmp:
            raise self.RuntimeError("Clock moved backwards.  Refusing to generate id")

        if curr_stmp == self.last_stmp:
            # 相同毫秒内，序列号自增
            self.sequence = (self.sequence + 1) & const.MAX_SEQUENCE
            # 同一秒的序列数已经达到最大
            if self.sequence == 0:
                curr_stmp = self.getNextMill()
        else:
            # 不同秒内，序列号为0
            self.sequence = 0

        self.last_stmp = curr_stmp
        return curr_stmp << const.TIMESTMP_LEFT \
                | self.datacenterId << const.DATACENTER_LEFT \
                | self.machineId << const.MACHINE_LEFT \
                | self.sequence


    def getNextMill(self):
        mill = self.getNewstmp()
        while mill <= self.last_stmp:
            mill = self.getNewstmp()
        return mill

    def getNewstmp(self):
        nowTimestamp = lambda: int(round(time.time() * 1000))
        return nowTimestamp()

if __name__ == "__main__":
    g = TimeGenerator()
    # 循环调用1000次id
    for x in range(1,1000):
    	print(g.nextID())

