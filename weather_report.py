import os
import requests
import smtplib
from email.message import EmailMessage

#读取对应城市天气信息
def get_weather():
    api_key = os.environ.get('WEATHER_KEY')
    city = os.environ.get('CITY', 'shenzhen')
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=zh_cn'
    
    try:
        res = requests.get(url).json()
        if res.get('cod') == 200:
            temp = round(res['main']['temp'])
            weather = res['weather'][0]['description']
            return f"今日{city}天气：{weather}，气温：{temp}°C。祝你开心！"
    except Exception as e:
        print(f"获取天气出错: {e}")
    return None

#调用与发送的邮箱
def send_email(content):
    msg_from = os.environ.get('MAIL_USER')
    password = os.environ.get('MAIL_PASS')
    mail_to_raw = os.environ.get('MAIL_TO', '')
    
    receivers = [addr.strip() for addr in mail_to_raw.split(',') if addr.strip()]

    if not receivers:
        print("未设置收件人名单")
        return

    try:
        with smtplib.SMTP_SSL('smtp.qq.com', 465) as smtp:
            smtp.login(msg_from, password)
            for msg_to in receivers:
                msg = EmailMessage()
                msg['Subject'] = "☀️ 每日天气播报"
                msg['From'] = msg_from
                msg['To'] = msg_to
                msg.set_content(content)
                smtp.send_message(msg)
                print(f"成功发送至: {msg_to}")
    except Exception as e:
        print(f"邮件发送失败: {e}")

if __name__ == "__main__":
    weather_info = get_weather()
    if weather_info:
        send_email(weather_info)
