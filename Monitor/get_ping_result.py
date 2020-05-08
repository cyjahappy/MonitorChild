from ping3 import ping
from .models import ServerList, PingResults


# 接受一个IP地址,返回ping的结果(给前端实时更新Line Chart数据使用)
def get_ping_result(server_ip):
    ping_result = {
        'server_ip': server_ip,
        'ping_result': ping(server_ip)
    }
    return ping_result


def ping_result_to_database():
    """
    从PingList中提取所有需要ping的IP, ping一遍之后将结果存储到数据库(给后端使用的)
    :return:
    """
    ip = ServerList.objects.all()
    total_ip = ip.count()
    i = 0
    while i < total_ip:
        data = PingResults()
        data.server_ip_id = ip[i].server_ip
        ping_result = ping(ip[i].server_ip)
        if ping_result:
            data.ping_result = round(ping_result, 2)
            data.save()
        i = i + 1
    return


'''
# 从PingList中提取所有的需要ping的IP, ping一遍之后返回ping的结果的字典(给前端实时用表格展示结果使用的)
def get_ping_results():
    ip = PingList.objects.all()
    total_ip = ip.count()
    ping_results = {
        'server_name': [],
        'server_ip': [],
        'ping_result': []
    }
    i = 0
    while i < total_ip:
        ping_results['server_name'].append(ip[i].server_name)
        ping_results['server_ip'].append(ip[i].server_ip)
        ping_results['ping_result'].append(ping(ip[i].server_ip))
        i = i + 1
    return ping_results
'''
