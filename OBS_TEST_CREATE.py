from obs import CreateBucketHeader
from obs import ObsClient
import os
import traceback

# 推荐通过环境变量获取AKSK，这里也可以使用其他外部引入方式传入，如果使用硬编码可能会存在泄露风险。
# 您可以登录访问管理控制台获取访问密钥AK/SK，获取方式请参见https://support.huaweicloud.com/intl/zh-cn/usermanual-ca/ca_01_0003.html。
AK = 'YXPNIT7QUJUHAI1GSUL2'
SK = 'tIWOjoAbXaxZYd8bfb6P9ZWgwhLbUsYHX5e7VEZ7'
server = 'https://obs.cn-north-4.myhuaweicloud.com'

# server填写Bucket对应的Endpoint, 这里以中国-香港为例，其他地区请按实际情况填写。
# 创建obsClient实例
# 如果使用临时AKSK和SecurityToken访问OBS，需要在创建实例时通过security_token参数指定securityToken值
obsClient = ObsClient(access_key_id=AK, secret_access_key=SK, server=server)
try:
    # 创建桶的附加头域，桶的访问控制策略是私有桶，存储类型是低频访问存储，多AZ方式存储
    header = CreateBucketHeader(aclControl="PRIVATE", storageClass="STANDARD", availableZone="1az")
    # 指定存储桶所在区域，此处以“ap-southeast-1”为例，必须跟传入的Endpoint中Region保持一致。
    location = "cn-north-4"
    
    bucketName = "python-examplebucket"
    # 创建桶
    resp = obsClient.createBucket(bucketName, header, location)
    # 返回码为2xx时，接口调用成功，否则接口调用失败
    if resp.status < 300:
        print('Create Bucket Succeeded')
        print('requestId:', resp.requestId)
    else:
        print('Create Bucket Failed')
        print('requestId:', resp.requestId)
        print('errorCode:', resp.errorCode)
        print('errorMessage:', resp.errorMessage)
except:
    print('Create Bucket Failed')
    print(traceback.format_exc())