from django.db import models


# 存储系统各项指标的数据
class ServerInfo(models.Model):
    date = models.DateTimeField(primary_key=True, auto_now=True)
    cpu = models.FloatField(null=True)
    memory = models.FloatField(null=True)
    disk = models.FloatField(null=True)
    network = models.FloatField(null=True)
    network_recv = models.FloatField(null=True)
    network_sent = models.FloatField(null=True)


# 存储除本机以外所有CRM服务器的IP地址
class ServerList(models.Model):
    server_ip = models.GenericIPAddressField(primary_key=True)
    server_name = models.CharField(null=True, max_length=20)


# 存储Ping的结果
class PingResults(models.Model):
    id = models.AutoField(primary_key=True)
    server_ip = models.ForeignKey(ServerList, on_delete=models.CASCADE)
    ping_result = models.FloatField(null=True)
    date = models.DateTimeField(auto_now=True, null=True)


# 存储对CRM服务器的iPerf测试的结果
class iPerfTestResults(models.Model):
    id = models.AutoField(primary_key=True)
    server_ip = models.ForeignKey(ServerList, on_delete=models.CASCADE)
    sent_Mbps = models.FloatField()
    received_Mbps = models.FloatField()
    retransmits = models.FloatField(null=True)
    tcp_mss_default = models.FloatField()
    date = models.DateTimeField(auto_now=True, null=True)


class PingResult(models.Model):
    """
    抽象模型, 用于初始化PingResultSerializer
    """
    id = models.AutoField(primary_key=True)
    server_ip = models.GenericIPAddressField()
    ping_result = models.FloatField(null=True)

    class Meta:
        abstract = True


# 存储需要检测H5访问时长的网址列表
class HTMLTestList(models.Model):
    url = models.URLField(primary_key=True)
    url_name = models.CharField(null=True, max_length=20)


# 存储检测H5访问时长的结果
class HTMLTestResults(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.ForeignKey(HTMLTestList, on_delete=models.CASCADE)
    dns_query = models.FloatField(null=True)
    tcp_connection = models.FloatField(null=True)
    request = models.FloatField(null=True)
    dom_parse = models.FloatField(null=True)
    blank_screen = models.FloatField(null=True)
    onload = models.FloatField(null=True)
    dom_ready = models.FloatField(null=True)
    date = models.DateTimeField(auto_now=True)
