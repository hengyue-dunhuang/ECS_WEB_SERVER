from obs import ObsClient, GetObjectHeader
import traceback
import json
from datetime import datetime, timedelta
from numpy import array,append


class OBS_MANAGER:
    def __init__(self, access_key, secret_key, server, bucket_name, object_key):
        self.access_key = access_key
        self.secret_key = secret_key
        self.server = server
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.obs_client = ObsClient(access_key_id=access_key, secret_access_key=secret_key, server=server)

    def download_object(self):
        '''return rh_array,temp_array,voltage_array,time_array'''
        try:
            headers = GetObjectHeader()
            resp = self.obs_client.getObject(self.bucket_name, self.object_key, loadStreamInMemory=True)

            if resp.status < 300:
                print('Get Object Succeeded')
                print('requestId:', resp.requestId)
                json_str = resp.body.buffer.decode('utf-8')
                json_strings = json_str.split('\n')
                rh_array,temp_array,voltage_array,time_array = array([]),array([]),array([]),array([])
                for js in json_strings:
                    data = json.loads(js)
                    时间 = data['event_time']
                    时间 = datetime.strptime(时间, "%Y%m%dT%H%M%SZ")
                    for i in range(5):
                        # 提取温度和湿度数据
                        湿度 = data['notify_data']['body']['services'][0]['properties']['r'+str(i+1)]
                        温度 = data['notify_data']['body']['services'][0]['properties']['t'+str(i+1)]
                        北京时间 = 时间+timedelta(hours=8)+timedelta(minutes=i)
                        rh_array = append(rh_array,湿度)
                        temp_array = append(temp_array,温度)
                        time_array = append(time_array,北京时间)

                    电压 = data['notify_data']['body']['services'][0]['properties']['voltage']
                    # 将数据添加到数组    
                    voltage_array = append(voltage_array,电压)                


                print('buffer:', resp.body.buffer)
                print('size:', resp.body.size)
            else:
                print('Get Object Failed')
                print('requestId:', resp.requestId)
                print('errorCode:', resp.errorCode)
                print('errorMessage:', resp.errorMessage)
        except Exception as e:
            print('Get Object Failed')
            print(traceback.format_exc())
        rh_array = 100*rh_array/65535#第一列数据 湿度
        temp_array = -45+175*temp_array/65535#第二列数据 温度
        voltage_array = 2*3.3*voltage_array/4095
        return rh_array,temp_array,voltage_array,time_array

if __name__ == "__main__":
    AK = 'YXPNIT7QUJUHAI1GSUL2'
    SK = 'tIWOjoAbXaxZYd8bfb6P9ZWgwhLbUsYHX5e7VEZ7'
    server = 'https://obs.cn-north-4.myhuaweicloud.com'
    bucket_name = "tuofeng"
    object_key = "TuoFeng/Data_rh_temp"

    obs_manager = OBS_MANAGER(AK, SK, server, bucket_name, object_key)
    obs_manager.download_object()

