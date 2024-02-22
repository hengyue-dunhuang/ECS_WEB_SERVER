from __future__ import print_function
from obs import ObsClient, Rule, Expiration, DateTime, NoncurrentVersionExpiration, WebsiteConfiguration, \
    IndexDocument, ErrorDocument, CorsRule, Options, Lifecycle, Logging, TagInfo

AK = 'YXPNIT7QUJUHAI1GSUL2'
SK = 'tIWOjoAbXaxZYd8bfb6P9ZWgwhLbUsYHX5e7VEZ7'
server = 'https://obs.cn-north-4.myhuaweicloud.com'

bucketName = 'my-obs-bucket-pythonsdk-demo'

# Constructs a obs client instance with your account for accessing OBS
obsClient = ObsClient(access_key_id=AK, secret_access_key=SK, server=server)

bucketClient = obsClient.bucketClient(bucketName)

def getBucketLocation():

    resp = bucketClient.getBucketLocation()
    if resp.status < 300:
        print('Getting bucket location ' + str(resp.body) + ' \n')
    else:
        print(resp.errorCode)

def createBucket():

    resp = bucketClient.createBucket(location = "cn-north-4")
    if resp.status < 300:
        print('Create bucket:' + bucketName + ' successfully!\n')
    else:
        print(resp.errorCode)

if __name__ == '__main__':
    createBucket()