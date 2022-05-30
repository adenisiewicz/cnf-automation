import schedule
import time
import json
import urllib.request
from urllib.request import urlopen
import logging
import os
import http.client
import certifi
import subprocess


def send_onset_up():
    stream = os.popen('./onset_up.sh')
    output = stream.read()
    print(output)
    exit()

def send_onset_down():
    stream = os.popen('./onset_down.sh')
    output = stream.read()
    print(output)
    exit()




def func():
    #nazwaMetryki = "container_cpu_load_average_10s"
    nazwaMetryki = "container_cpu_usage_seconds_total"
    namespace = "monitoring"
    pod1 = "rel-1-apache-7bd87fdb75-7tsjz"

    #url = 'http://portal.api.simpledemo.onap.org:30333/api/v1/query?query=' + urllib.parse.quote('sum(rate(container_cpu_usage_seconds_total{namespace="test-ad", pod="rel-1-apache-9dc8fb74c-vdcsn"}[5m])) /sum(container_spec_cpu_quota{namespace="test-ad", pod="rel-1-apache-9dc8fb74c-vdcsn"}/container_spec_cpu_period{namespace="test-ad", pod="rel-1-apache-9dc8fb74c-vdcsn"})')
    url = 'http://portal.api.simpledemo.onap.org:30333/api/v1/query?query=sum(rate('+nazwaMetryki+'{namespace=\"'+namespace+'\",pod=\"'+pod1+'\"}[1m]))'
    #print(url)

    response = urlopen(url)
    data = json.loads(response.read())
    try:
        metryka = float(data["data"]["result"][0]["value"][1])/1e-2
        print("%.10f" % metryka)
        if metryka > 10:
            print("send_onset_up()")
            #send_onset_up()
        if metryka < 0.2:
            print("send_onset_down()")
            #send_onset_down()


    except:
        print("Prometheus reading error")

    #print(data)

schedule.every(10).seconds.do(func)
func()
while True:
    schedule.run_pending()
    time.sleep(1)
                                                                                                                                                                                                      