from .serializers import ServerInfoSerializer, PingResultSerializer, iPerfTestResultsSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .psutil_get_server_info import get_server_info
from .get_ping_result import ping_result_to_database, get_ping_result
from .html_performance_test import html_performance_test_to_database
from .iperf_test import iperf3_result_to_database, iperf3_test


class ServerInfo_to_Database(APIView):
    """
    将服务器各项指标数据存入远端的数据库中
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
    对HTMLTestList表中指定的URL进行前端性能测试, 并将测试结果存储在远端数据库中
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
    接受一个GET请求, 从请求中提取需要ping的ip地址, ping之后将结果返回(还没测试!)
    """

    def get(self, request, format=None):
        server_ip = request.GET.get('server_ip')
        if server_ip:
            ping_result = get_ping_result(server_ip)
            serializer = PingResultSerializer(data=ping_result)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    """

    def post(self, request, format=None):
        server_ip = request.data['server_ip']
        result = iperf3_test(server_ip)
        serializer = iPerfTestResultsSerializer(data=result)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
