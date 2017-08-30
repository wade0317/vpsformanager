#!/usr/bin/python


import socket
import fcntl
import struct
import json
import time

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import CreateInstanceRequest

from aliyunsdkecs.request.v20140526 import StopInstanceRequest
from aliyunsdkecs.request.v20140526 import DeleteInstanceRequest;
from aliyunsdkecs.request.v20140526 import StartInstanceRequest
from aliyunsdkecs.request.v20140526 import AllocatePublicIpAddressRequest;

from  aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest;
from  aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest;


client = AcsClient(
    "LTAIXtBhdaff",
    "fasdfadfadfadfadfafafaf",
    "cn-hongkong"
);


dnsRequest = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest();
dnsRequest.set_DomainName('weishq.com')
dnsRequest.set_PageSize(30)
dnsReponse = client.do_action_with_exception(dnsRequest)
dnsReponseJson = json.loads(dnsReponse);
iDnsCount = dnsReponseJson['TotalCount']

appDNS = {}
if iDnsCount > 0:
    recordItems = dnsReponseJson['DomainRecords']['Record']
    for index in range(iDnsCount):
        recordItem = recordItems[index]
        if recordItem['RR'] == 'greatvpn':
            vpnDNS = recordItem;
            break;


descInstansListRequest = DescribeInstancesRequest.DescribeInstancesRequest()
descInstansListResponce = client.do_action_with_exception(descInstansListRequest)
descInstansListResponceJson = json.loads(descInstansListResponce);

currentInstance = {}
currentInstanceId = ''
instancePublicIpAddress = ''
print "Instance Count:"
print descInstansListResponceJson['TotalCount']

if vpnDNS['RecordId'] != '':
    if descInstansListResponceJson['TotalCount'] > 0:
        instanArray = descInstansListResponceJson['Instances']['Instance']
        for instanceIndex in range(descInstansListResponceJson['TotalCount']):
            instance = instanArray[instanceIndex]
            instancePublicIpAddress = instance['PublicIpAddress']['IpAddress']
            isThisInstance ='false'
            for ipIndex in range(len(instancePublicIpAddress)):
                if  instancePublicIpAddress[ipIndex] == vpnDNS['Value']:
                    isThisInstance = 'true'
                    currentInstance = instance
                    currentInstanceId = instance['InstanceId']
                    currentPublicIpAddress = instance['PublicIpAddress']['IpAddress']
                    break
            if isThisInstance == 'true':
                break;



if currentInstanceId != '':

    delRequest = DeleteInstanceRequest.DeleteInstanceRequest();
    delRequest.set_InstanceId(currentInstanceId)
    delReponse = client.do_action_with_exception(delRequest)
    delReponseJson = json.loads(delReponse);
    print "Stop VPN Instance !"
else:
    print "No Fount VPN Instance !"

# if descInstansListResponceJson['TotalCount'] > 0:
#     instanArray = descInstansListResponceJson['Instances']['Instance']
#     for instanceIndex in range(descInstansListResponceJson['TotalCount']):
#         instance = instanArray[instanceIndex]
#         instancePublicIpAddress = instance['PublicIpAddress']['IpAddress']
#         if  instance['InstanceName'] == 'myhkautovps':
#             if instance['InstanceId'] != '':
#                 delRequest = DeleteInstanceRequest.DeleteInstanceRequest();
#                 delRequest.set_InstanceId(instance['InstanceId'])
#                 delReponse = client.do_action_with_exception(delRequest)
#                 delReponseJson = json.loads(delReponse);





