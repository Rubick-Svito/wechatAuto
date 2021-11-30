import requests
import json
import hashlib
se = requests.session()

def api(name, args):
  res = ''
  if name == '历史上的今天':
    # api doc https://www.free-api.com/doc/533
    url = 'https://api.oick.cn/lishi/api.php'
    r = se.get(url)
    dict = r.json()
    res += '今天是' + dict['day']
    for item in dict['result']:
      res += '\n'
      res += item['date']
      res += ' '
      res += item['title']
  elif name == '天气':
    # api doc https://www.free-api.com/doc/518
    url = 'http://aider.meizu.com/app/weather/listWeather'
    cityName = args[0]
    if cityName == '':
      res = '未获取到城市名，请以例如"天气 上海" 格式回复'
    else:
      with open('cityId.json','r',encoding='utf-8') as fp:
        json_data = json.load(fp)
        cityIdCheck = [item for item in json_data if item['countyname'] == cityName]
        if len(cityIdCheck) == 0:
          res = '未查询到城市'
        else:
          cityId = [item for item in json_data if item['countyname'] == cityName][0]['areaid']
          r = se.get(url,params={'cityIds' : cityId})
          data = r.json()
          value = data['value'][0]
          if data['code'] == '200':
            res ='今日'+ cityName +'天气：' + value['weathers'][0]['weather'] + '\n'
            res += '日间温度：' + value['weathers'][0]['temp_day_c'] + '℃ \n' + '夜间温度：' + value['weathers'][0]['temp_night_c'] + '℃ \n'
            res += '实时温度：' + value['realtime']['temp'] + '\n风力：' + value['realtime']['wD'] + value['realtime']['wS'] + '\n'
            for item in value['indexes']:
              res += '\n' + item['name'] + '：' + item['content']
            res += '\n更新时间：' + value['weatherDetailsInfo']['publishTime']
          else:
            res = '网络错误，查询失败'
  elif name == '翻译':
    # 百度翻译免费接口，appid secret需自行申请
    url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    appid = ''
    sec = ''
    salt = '118'
    q = args[0]
    s = appid + q + salt + sec
    md5 = hashlib.md5(bytes(s, encoding='utf8')).hexdigest()
    r = se.get(url, params={'q':q,'from':'auto','to':'en','appid':appid,'salt':salt,'sign':md5})
    data = r.json()
    res = data['trans_result'][0]['dst']
  # 自动回复
  else:
    resp = requests.get("http://api.qingyunke.com/api.php", {'key': 'free', 'appid': 0, 'msg': name})
    resp.encoding = 'utf8'
    resp = resp.json()
    res = resp['content']
  
  return res
