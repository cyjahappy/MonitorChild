from django.urls import path
from Monitor import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url

urlpatterns = [
    path('server-info-api', views.ServerInfoList.as_view()),
    path('server-info-to-db', views.ServerInfo_to_Database.as_view()),
    path('ping-results-to-db', views.PingResults_to_Database.as_view()),
    path('html-performance-test-result-api', views.HTMLPerformanceTestResult.as_view()),
    path('html-performance-test-results-to-db', views.HTMLTestResults_to_Database.as_view()),
    path('iperf3-test-results-to-db', views.iPerfResults_to_Database.as_view()),
    path('iperf3-test-result-api', views.iPerfResults.as_view()),
    path('server-info-threshold-api', views.ServerInfoThresholdList.as_view()),
    url(r'^server-info-threshold-update/(?P<pk>[0-9]+)/$', views.ServerInfoThresholdUpdate.as_view()),
    path('clean-database-api', views.CleanDatabase.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
