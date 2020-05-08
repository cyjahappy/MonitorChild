from selenium import webdriver
from .models import HTMLTestList, HTMLTestResults


# 从HTMLTestList中提取所有需要测试性能的URL地址, 都测试一遍一遍之后将结果存储到数据库
def html_performance_test_to_database():
    url = HTMLTestList.objects.all()
    total_url = url.count()
    i = 0
    while i < total_url:
        # 设置测试的时候浏览器后台运行
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')

        # 使用Chrome浏览器来模拟测试环境
        driver = webdriver.Chrome(chrome_options=chrome_options)

        # 初始化一个HTMLTestResults数据库的实例
        HTMLTestResults_instance = HTMLTestResults()

        HTMLTestResults_instance.url_id = url[i].url

        # 使用浏览器打开对应的URL
        driver.get(url[i].url)

        # pull window.performance.timing after loading the page and add information about url and number of run
        perf_timings = driver.execute_script("return window.performance.timing")

        # DNS查询耗时
        HTMLTestResults_instance.dns_query = (perf_timings['domainLookupEnd'] - perf_timings[
            'domainLookupStart']) / 1000

        # TCP连接耗时
        HTMLTestResults_instance.tcp_connection = (perf_timings['connectEnd'] - perf_timings['connectStart']) / 1000

        # request请求耗时
        HTMLTestResults_instance.request = (perf_timings['responseEnd'] - perf_timings['responseStart']) / 1000

        # 解析dom树耗时
        HTMLTestResults_instance.dom_parse = (perf_timings['domComplete'] - perf_timings['domInteractive']) / 1000

        # 白屏时间
        HTMLTestResults_instance.blank_screen = (perf_timings['responseStart'] - perf_timings['navigationStart']) / 1000

        # dom ready时间
        HTMLTestResults_instance.dom_ready = (perf_timings['domContentLoadedEventEnd'] - perf_timings[
            'navigationStart']) / 1000

        # 整体页面完全加载完毕的时间
        HTMLTestResults_instance.onload = (perf_timings['loadEventEnd'] - perf_timings['navigationStart']) / 1000

        # 将实例存储到数据库中
        HTMLTestResults_instance.save()

        # 关闭浏览器
        driver.quit()

        i = i + 1
    return
