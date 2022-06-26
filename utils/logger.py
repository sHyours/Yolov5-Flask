import logging
import os

def init():
    # 第一步，创建一个logger
    logger = logging.getLogger("Rune")
    logger.setLevel(logging.INFO)    # Log等级总开关
    
    # 第二步，创建一个handler，用于写入日志文件
    logfile = os.path.split(os.path.realpath(__file__))[0] + "\\..\\log\\logger.txt"
    fh = logging.FileHandler(logfile, mode='a')
    fh.setLevel(logging.INFO)   # 输出到file的log等级的开关
    
    # 第三步，再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)   # 输出到console的log等级的开关
    
    # 第四步，定义handler的输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    # 第五步，将logger添加到handler里面
    logger.addHandler(fh)
    logger.addHandler(ch)

logger = logging.getLogger("Timer")