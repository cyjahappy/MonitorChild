import iperf3
from .models import ServerList, iPerfTestResults
from .threshold_check import iperf_check, iperf_alert


def iperf3_test(server_ip):
    """
    接受一个IP地址, 进行iPerf3测试,将测试结果以字典形式返回
    :param server_ip:
    :return: iperf3_result
    """

    client = iperf3.Client()
    client.server_hostname = server_ip
    iperf3_error_result = {
        'server_ip': server_ip,
        'error': '',
    }
    try:
        result = client.run()
    except:
        print('error')

    # 当无法与服务器通信时, 返回错误信息
    if result.error:
        iperf3_error_result['error'] = result.error
        return iperf3_error_result

    # 正常进行测试, 返回测试结果
    else:
        # TCP重传的次数是0的话, 把None改成0, 便于传值
        if result.retransmits is None:
            result.retransmits = 0
        iperf3_result = {
            'server_ip': server_ip,
            'sent_Mbps': round(result.sent_Mbps, 2),
            'received_Mbps': round(result.received_Mbps, 2),
            'tcp_mss_default': round(result.tcp_mss_default, 2),
            'retransmits': result.retransmits,
        }
    return iperf3_result


def iperf3_result_to_database():
    """
    对ServerList中的IP地址逐个进行iPerf3测试, 将结果存入数据库, 并进行阈值检测报警.
    """

    # 声明一个列表用于存储检测中不达标的ip地址
    iperf3_problematic_server_ip = []
    iperf3_problematic_result = []
    iperf3_problematic_results = []

    ip = ServerList.objects.all()
    total_ip = ip.count()
    i = 0
    while i < total_ip:
        iperf3_result = iperf3_test(ip[i].server_ip)
        iPerfTestResultsInstance = iPerfTestResults()
        if 'error' in iperf3_result:
            iPerfTestResultsInstance.error = iperf3_result['error']
        else:
            # 进行阈值检测, 并将检测不达标的IP地址添加进列表尾部
            if iperf_check(iperf3_result) is True:
                iperf3_problematic_server_ip.append(iperf3_result['server_ip'])
                iperf3_problematic_result.append(iperf3_result['sent_Mbps'])
                iperf3_problematic_result.append(iperf3_result['received_Mbps'])
                iperf3_problematic_result.append(iperf3_result['tcp_mss_default'])
                iperf3_problematic_result.append(iperf3_result['retransmits'])
                iperf3_problematic_results.append(iperf3_problematic_result)
                iperf3_problematic_result = []

            iPerfTestResultsInstance.server_ip_id = iperf3_result['server_ip']
            iPerfTestResultsInstance.sent_Mbps = iperf3_result['sent_Mbps']
            iPerfTestResultsInstance.received_Mbps = iperf3_result['received_Mbps']
            iPerfTestResultsInstance.tcp_mss_default = iperf3_result['tcp_mss_default']
            iPerfTestResultsInstance.retransmits = iperf3_result['retransmits']
        iPerfTestResultsInstance.save()
        i = i + 1

    # 如果problematic_server_ip不为空, 则调用警报函数
    if len(iperf3_problematic_server_ip) > 0:
        iperf3_alert_message_dict = dict(zip(iperf3_problematic_server_ip, iperf3_problematic_results))
        iperf_alert(iperf3_alert_message_dict)
    return
