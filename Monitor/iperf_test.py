import iperf3
from .models import ServerList, iPerfTestResults


def iperf3_test(server_ip):
    """
    接受一个IP地址, 进行iPerf3测试,将测试结果以字典形式返回
    :param server_ip:
    :return: iperf3_result
    """
    client = iperf3.Client()
    client.server_hostname = server_ip
    result = client.run()
    if result.error:
        # 需要在这里放个重新测试的函数
        return
    else:
        iperf3_result = {
            'server_ip': server_ip,
            'sent_Mbps': result.sent_Mbps,
            'received_Mbps': result.received_Mbps,
            'tcp_mss_default': result.tcp_mss_default,
            'retransmits': result.retransmits,
        }
    return iperf3_result


def iperf3_result_to_database():
    ip = ServerList.objects.all()
    total_ip = ip.count()
    i = 0
    while i < total_ip:
        iperf3_result = iperf3_test(ip[i].server_ip)
        data = iPerfTestResults()
        data.server_ip_id = iperf3_result['server_ip']
        data.sent_Mbps = iperf3_result['sent_Mbps']
        data.received_Mbps = iperf3_result['received_Mbps']
        data.tcp_mss_default = iperf3_result['tcp_mss_default']
        data.retransmits = iperf3_result['retransmits']
        data.save()
        i = i + 1
    return


"""
        ip = PingList.objects.all()
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
"""