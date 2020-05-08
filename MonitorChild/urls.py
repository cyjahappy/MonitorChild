from django.urls import path
from Monitor import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('server-info-api', views.ServerInfoList.as_view()),
    path('server-info-to-db', views.ServerInfo_to_Database.as_view()),
    path('ping-results-to-db', views.PingResults_to_Database.as_view()),
    path('html-test-results-to-db', views.HTMLTestResults_to_Database.as_view()),
    path('iperf3-test-results-to-db', views.iPerfResults_to_Database.as_view()),
    path('iperf3-test-result-api', views.iPerfResults.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
