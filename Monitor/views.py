from .serializers import ServerInfoSerializer, PingResultSerializer, iPerfTestResultsSerializer, ServerInfoThresholdSerializer
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .psutil_get_server_info import get_server_info
from .get_ping_result import ping_result_to_database, get_ping_result
from .html_performance_test import html_performance_test_to_database
from .iperf_test import iperf3_result_to_database, iperf3_test
from .models import ServerInfoThreshold


class ServerInfo_to_Database(APIView):
    """
    将服务器各项指标数据存入ServerInfo表中
    """

    def get(self, request):
        serializer = ServerInfoSerializer(data=get_server_info())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ServerInfoList(APIView):
    """
    返回JSON格式的服务器各项指标数据
    """

    def get(self, request, format=None):
        serializer = ServerInfoSerializer(data=get_server_info())
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HTMLTestResults_to_Database(APIView):
    """
    对HTMLTestList表中指定的URL进行前端性能测试, 并将测试结果存储在HTMLTestResults表中
    """

    def get(self, request):
        try:
            html_performance_test_to_database()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PingResults_to_Database(APIView):
    """
    对ServerList表中所有的IP依次进行ping测试, 并将测试结果存储在PingResult表中(还没测试!)
    """

    def get(self, request, format=None):
        try:
            ping_result_to_database()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PingResult(APIView):
    """
    接收一个IP地址, ping之后将结果以JSON形式返回(还没测试!)
    """

    def post(self, request, format=None):
        server_ip = request.data['server_ip']
        ping_result = get_ping_result(server_ip)
        serializer = PingResultSerializer(data=ping_result)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class iPerfResults_to_Database(APIView):
    """
    对ServerList表中所有的IP依次执行iPerf测试, 并将测试结果存储在iPerfTestResults表中
    """

    def get(self, request, format=None):
        try:
            iperf3_result_to_database()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class iPerfResults(APIView):
    """
    接收一个IP地址, 进行iPerf测试, 并将测试结果以JSON形式返回

    :HTTP Request:
    POST http://localhost:8000/iperf3-test-result-api
    Content-Type: application/json

    {"server_ip":  "129.204.183.108"}

    :return:
        {
          "server_ip": "129.204.183.108",
          "sent_Mbps": 4.37,
          "received_Mbps": 3.18,
          "retransmits": null,
          "tcp_mss_default": 8960.0
        }
    """

    def post(self, request, format=None):
        server_ip = request.data['server_ip']
        result = iperf3_test(server_ip)
        serializer = iPerfTestResultsSerializer(data=result)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ServerInfoThresholdList(generics.ListAPIView):
    """
    定义GET操作,返回JSON格式的服务器各项指标阈值
    """
    queryset = ServerInfoThreshold.objects.all()
    serializer_class = ServerInfoThresholdSerializer


class ServerInfoThresholdUpdate(generics.UpdateAPIView):
    """
    定义PUT操作,更新服务期各项指标阈值

    HTTP Request:
    PUT http://localhost:8000/server-info-threshold-update/1/
    Content-Type: application/json

    {
      "cpu_threshold": "91",
      "memory_threshold": "91",
      "disk_threshold": "91",
      "bandwidth_threshold": "91",
      "HTML_open_time_threshold": "91",
      "tcp_sent_Mbps_threshold": "0",
      "tcp_received_Mbps_threshold": "0",
      "microservices_exec_time_threshold": "91",
      "backend_management_system_open_time_threshold": "91"
    }
    """
    queryset = ServerInfoThreshold.objects.all()
    serializer_class = ServerInfoThresholdSerializer
