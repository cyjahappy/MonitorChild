# -*- coding: utf-8 -*-
import psutil
import time
from .models import ServerInfo


def get_server_info():
    """
    使用psutil库来获取系统的各项指标
    :return: 字典格式存储的server_info
    """

    # CPU使用率(%)
    cpu = psutil.cpu_percent(interval=1)

    # 内存总量(转换为GB)
    memory_total = psutil.virtual_memory().total / 1073741824

    # 已使用的内存(转换为GB)
    memory_used = round((psutil.virtual_memory().used / 1073741824), 2)

    # 内存使用率(%)
    memory = round((memory_used / memory_total) * 100, 2)

    # 磁盘使用率(%)(需要使用"df -h"命令 to list all mounted disk partitions, 然后选择对的那个来获取磁盘使用率)
    disk = psutil.disk_usage("/System/Volumes/Data").percent

    # 直到当前服务器网络已经上传和下载的MB总和
    last_network = round((psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv) / 1048576, 2)

    # 停一秒以便接下来获取这一秒的网络带宽信息
    time.sleep(1)

    # 直到当前服务器网络已经上传的MB
    network_recv = round((psutil.net_io_counters().bytes_recv / 1048576), 2)

    # 直到当前服务器网络已经下载的MB
    network_sent = round((psutil.net_io_counters().bytes_sent / 1048576), 2)

    # 得到这一秒服务器网络上传和下载的总和 单位MB
    network = round((network_sent + network_recv - last_network), 2)
    server_info = {'cpu': cpu,
                   'memory': memory,
                   'memory_used': memory_used,
                   'disk': disk,
                   'network': network,
                   'network_recv': network_recv,
                   'network_sent': network_sent
                   }
    return server_info


# 将服务器各项指标的值传入数据库
def server_info_to_database(server_info):
    data = ServerInfo()
    data.cpu = server_info['cpu']
    data.memory = server_info['memory']
    data.disk = server_info['disk']
    data.network = server_info['network']
    data.network_recv = server_info['network_recv']
    data.network_sent = server_info['network_sent']
    data.save()
    return
