from selenium import webdriver
from .models import HTMLTestList, HTMLTestResults
from .threshold_check import html_performance_check, html_performance_alert


def get_html_performance_test_result(url):
    """
    接收一个URL地址, 进行前端性能测试, 将结果以字典形式返回
    :param url:
    :return:
    """
    # 设置测试的时候浏览器后台运行
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    # 使用Chrome浏览器来模拟测试环境
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # 使用浏览器打开对应的URL
    driver.get(url)
    # pull window.performance.timing after loading the page and add information about url and number of run
    perf_timings = driver.execute_script("return window.performance.timing")
    # DNS查询耗时
    dns_query = (perf_timings['domainLookupEnd'] - perf_timings['domainLookupStart']) / 1000
    # TCP连接耗时
    tcp_connection = (perf_timings['connectEnd'] - perf_timings['connectStart']) / 1000
    # request请求耗时
    request = (perf_timings['responseEnd'] - perf_timings['responseStart']) / 1000
    # 解析dom树耗时
    dom_parse = (perf_timings['domComplete'] - perf_timings['domInteractive']) / 1000
    # 白屏时间
    blank_screen = (perf_timings['responseStart'] - perf_timings['navigationStart']) / 1000
    # dom ready时间
    dom_ready = (perf_timings['domContentLoadedEventEnd'] - perf_timings['navigationStart']) / 1000
    # 整体页面完全加载完毕的时间
    onload = (perf_timings['loadEventEnd'] - perf_timings['navigationStart']) / 1000
    # 关闭浏览器
    driver.quit()
    html_performance_test_result = {
        'url_id': url,
        'dns_query': dns_query,
        'tcp_connection': tcp_connection,
        'request': request,
        'dom_parse': dom_parse,
        'blank_screen': blank_screen,
        'dom_ready': dom_ready,
        'onload': onload
    }
    return html_performance_test_result


def html_performance_test_to_database():
    """
    从HTMLTestList中提取所有需要测试性能的URL地址, 都测试一遍一遍之后将结果存储到数据库
    :return:
    """

    # 声明一个列表用于存储检测中不达标的URL地址
    html_performance_problematic_url = []
    url = HTMLTestList.objects.all()
    total_url = url.count()
    i = 0
    while i < total_url:
        html_performance_test_result = get_html_performance_test_result(url[i].url)

        # 进行阈值检查, 并将检测不达标的URL地址添加进列表尾部
        if html_performance_check(html_performance_test_result) is True:
            html_performance_problematic_url.append(html_performance_test_result['url_id'])

        # 将结果存入数据库
        HTMLTestResults_instance = HTMLTestResults()
        HTMLTestResults_instance.url_id = html_performance_test_result['url_id']
        HTMLTestResults_instance.dns_query = html_performance_test_result['dns_query']
        HTMLTestResults_instance.tcp_connection = html_performance_test_result['tcp_connection']
        HTMLTestResults_instance.request = html_performance_test_result['request']
        HTMLTestResults_instance.dom_parse = html_performance_test_result['dom_parse']
        HTMLTestResults_instance.blank_screen = html_performance_test_result['blank_screen']
        HTMLTestResults_instance.dom_ready = html_performance_test_result['dom_ready']
        HTMLTestResults_instance.onload = html_performance_test_result['onload']
        HTMLTestResults_instance.save()
        i = i + 1

    # 如果html_performance_problematic_url不为空, 则调用警报函数
    if len(html_performance_problematic_url) > 0:
        html_performance_alert(html_performance_problematic_url)
    return
