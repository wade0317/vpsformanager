#!/usr/bin/python

import json
import time
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import CreateInstanceRequest
from aliyunsdkecs.request.v20140526 import DeleteInstanceRequest
from aliyunsdkecs.request.v20140526 import StopInstanceRequest
from aliyunsdkecs.request.v20140526 import StartInstanceRequest
from aliyunsdkecs.request.v20140526 import AllocatePublicIpAddressRequest;

from  aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest;
from  aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest;


client = AcsClient(
    "LTAIXtBhdaff",
    "fasdfadfadfadfadfafafaf",
    "cn-hongkong"
);

# create instance
request = CreateInstanceRequest.CreateInstanceRequest()
request.set_InstanceName('myhkautovps')
request.set_ImageId('m-j6c5dft4t2aod6w8fdgw')
request.set_InstanceChargeType('PostPaid')
request.set_InternetChargeType('PayByTraffic')
request.set_InternetMaxBandwidthIn(100)
request.set_InternetMaxBandwidthOut(100)
request.set_InstanceType('ecs.xn4.small')
request.set_SecurityGroupId('sg-j6c3av8ns17s21rj3e2f')
request.set_SystemDiskSize(40)
request.set_KeyPairName('id_rsa')
response = client.do_action_with_exception(request)
responseJson = json.loads(response);
print responseJson['InstanceId'];

# start
time.sleep(10)
startRequest = StartInstanceRequest.StartInstanceRequest()
startRequest.set_InstanceId(responseJson['InstanceId'])
startResponse = client.do_action_with_exception(startRequest)
startResponseJson = json.loads(startResponse);


# set ip
time.sleep(30)
publicIpRequest = AllocatePublicIpAddressRequest.AllocatePublicIpAddressRequest();
publicIpRequest.set_InstanceId(responseJson['InstanceId']);
publicIpResponse = client.do_action_with_exception(publicIpRequest)
publicIpResponseJson = json.loads(publicIpResponse);
print publicIpResponseJson['IpAddress'];


# set dns
dnsRequest = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest();
dnsRequest.set_DomainName('weishq.com')
dnsRequest.set_PageSize(30)
dnsReponse = client.do_action_with_exception(dnsRequest)
dnsReponseJson = json.loads(dnsReponse);

iDnsCount = dnsReponseJson['TotalCount']
vpnDNS = {}
if iDnsCount > 0:
    recordItems = dnsReponseJson['DomainRecords']['Record']
    for index in range(iDnsCount):
        recordItem = recordItems[index]
        if recordItem['RR'] == 'greatvpn':
            vpnDNS = recordItem;
            break;

updatednsRequest = UpdateDomainRecordRequest.UpdateDomainRecordRequest();
updatednsRequest.set_RecordId(vpnDNS['RecordId'])
updatednsRequest.set_RR(vpnDNS['RR'])
updatednsRequest.set_Type(vpnDNS['Type'])
updatednsRequest.set_Value(publicIpResponseJson['IpAddress'])
updatednsReponse = client.do_action_with_exception(updatednsRequest)
updatednsReponseJson = json.loads(dnsReponse);




