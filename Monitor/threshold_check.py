from .models import ServerInfoThreshold

# 从数据库中获取各项指标阈值
Threshold = ServerInfoThreshold.objects.get(id=1)
cpu_threshold = Threshold.cpu_threshold
memory_threshold = Threshold.memory_threshold
disk_threshold = Threshold.disk_threshold
bandwidth_threshold = Threshold.bandwidth_threshold
HTML_open_time_threshold = Threshold.HTML_open_time_threshold
backend_management_system_open_time_threshold = Threshold.backend_management_system_open_time_threshold
microservices_exec_time_threshold = Threshold.microservices_exec_time_threshold
tcp_sent_Mbps_threshold = Threshold.tcp_sent_Mbps_threshold
tcp_received_Mbps_threshold = Threshold.tcp_received_Mbps_threshold
ping_threshold = Threshold.ping_threshold


def server_info_check(server_info):
    """
    接收server_info的数据, 逐一检查是否超过阈值, 如果超过就报警
    :param server_info:
    """

    if (server_info['cpu'] > cpu_threshold) or (server_info['memory'] > memory_threshold) or (server_info[
            'disk'] > disk_threshold) or (
            server_info['bandwidth'] > bandwidth_threshold):
        print('Server Information !!!!!!!!!!!!!!!!!!!!!!!')
    return


def iperf_test_check(iperf3_result):
    """
    接收iperf3_result的数据, 逐一检查是否小于阈值, 如果超过就报警(返回速度低于阈值的服务器IP)
    :param iperf3_result:
    """

    if (iperf3_result['sent_Mbps'] < tcp_sent_Mbps_threshold) or (
            iperf3_result['received_Mbps'] < tcp_received_Mbps_threshold):
        print(iperf3_result['server_ip'])
    return


def ping_check(ping_result):
    """
    接收ping_result数据, 检测延迟是否超过阈值, 如果超过就报警(返回速度低于阈值的服务器IP)
    :param ping_result:
    """

    if ping_result['result'] > ping_threshold:
        print(ping_result['server_ip'])
    return


def html_performance_check(html_performance_test_result):
    """
    接受html_performance_test_result数据, 检测整体页面打开时间是否超过阈值, 如果超过就报警(返回超过阈值的URL)
    :param html_performance_test_result:
    """

    if html_performance_test_result['onload'] > HTML_open_time_threshold:
        print(html_performance_test_result['url_id'])
