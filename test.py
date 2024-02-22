from flask import Flask,render_template
from OBS_TEST_READ_OBJ import OBS_MANAGER
app = Flask(__name__)
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
import base64
matplotlib.use('TkAgg')  # or another compatible backend

@app.route('/')
def index():
    AK = 'YXPNIT7QUJUHAI1GSUL2'
    SK = 'tIWOjoAbXaxZYd8bfb6P9ZWgwhLbUsYHX5e7VEZ7'
    server = 'https://obs.cn-north-4.myhuaweicloud.com'
    bucket_name = "tuofeng"
    object_key = "TuoFeng/Data_rh_temp"

    obs_manager = OBS_MANAGER(AK, SK, server, bucket_name, object_key)
    rh,temp,vol,time = obs_manager.download_object()
    fig, axes = plt.subplots(1,3,figsize=(12, 4))

    # 设置横坐标间隔和时间格式
    for ax in axes:
        time_point = len(time)
        if time_point <=120:
            interval_minutes = int(time_point/20)
            ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=interval_minutes))
        else:
            interval_hour = int(time_point/120)
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=interval_hour))
        
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        ax.tick_params(rotation=45, labelright=True, labelleft=False)  # 倾斜标签，避免重叠
    
    # 绘制数据
    axes[0].plot(time, rh,'r')
    axes[1].plot(time, temp,'g')
    axes[2].plot(time[::5], vol,'y')
    axes[0].set_title('Relative Humidity')
    axes[1].set_title('Temperature')
    axes[2].set_title('Voltage')
    # 设置图表标题
    fig.suptitle('TuoFeng Zero IoT Environmental Monitoring Station')
    
    # 显示图表
    plt.tight_layout()  # 可选，确保子图布局合理
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_data = base64.b64encode(img.getvalue()).decode()

    # 清除图表以便下次使用
    plt.clf()

    # 将图像数据传递给模板
    rh_new =  rh[-1]
    temp_new = temp[-1]
    vol_new = vol[-1]

    return render_template('index.html', img_data=img_data,rh_new=rh_new,temp_new=temp_new,voltage_new=vol_new)

if __name__ == '__main__':
    app.run(debug=True)
