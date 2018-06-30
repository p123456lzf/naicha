# -*- coding: utf-8 -*-
from config import app,db
from models import User2
import datetime
import requests
import random
import threading
from flask import render_template
#from gevent.wsgi import WSGIServer

#注销支付码
# Done
@app.route('/delete_paynum/<user_id>')
def delete_paynum(user_id):
    User2.query.filter_by(user_id=user_id).update({'pay_num': '------'})
    db.session.commit()

@app.route('/image/<image>')
def hello_world(image):
    img_path = image + '.jpg'
    import base64
    with open(img_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream)
    return img_stream

@app.route('/')
def hello():
    return 'hello'

# 用于获取openId
#  需要修改id和secret
@app.route('/code_naicha/<code>')
def get_openid2(code):
    appid = 'wxf46a09a2913f802f'
    secret = '507dac807276f7f7a116480f9a9d9ca5'
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + appid + '&secret=' + secret + '&grant_type=authorization_code&js_code=' + code
    result = requests.get(url,headers={'content-type': 'application/json'})
    return result.text

# 用于第一次登陆，如果此人是第一次登陆，则建库储存个人基本信息(ok为0表示此用户第一次登陆，为1表示老用户）
#  Done
@app.route('/user2/<user_id>/name/<name>')
def setup_user2(user_id,name):
    the_user = User2.query.filter_by(user_id=user_id).first()
    if the_user == None:
        user = User2(user_id=user_id, user_name=name, phone_num='', money=0, record='', pay_num='------' )
        db.session.add(user)
        db.session.commit()
        results_json = "{\"ok\":0,\"data\":[{"
        results_json += "\"user_id\":" + "\"" + user_id + "\","
        results_json += "\"user_name\":" + "\"" + name + "\","
        results_json += "\"phone_num\":" + "\"\","
        results_json += "\"money\":" + "0,"
        results_json += "\"record\":" + "\"\","
        results_json += "\"pay_num\":" + "\"\"}]}"
    else:
        results_json = "{\"ok\":1,\"data\":[{"
        results_json += "\"user_id\":" + "\"" + user_id + "\","
        results_json += "\"user_name\":" + "\"" + name + "\","
        results_json += "\"phone_num\":" + "\"" + the_user.phone_num + "\","
        results_json += "\"money\":" + the_user.money + ","
        results_json += "\"record\":" + "\"" + the_user.record + "\","
        results_json += "\"pay_num\":" + "\"\"}]}"
    return results_json

#根据user_id储存手机号
# Done (前端要注意返回结果）
@app.route('/user/<user_id>/phone/<num>')
def save_phone(user_id,num):
    try:
        User2.query.filter_by(user_id=user_id).update({'phone_num': str(num)})
        db.session.commit()
    except Exception as e:
        return "{\"ok\":0}"
    return "{\"ok\":1}"

#根据用户id生成他的六位支付码，并在2分钟后注销掉
# Done
@app.route('/pay_num/<user_id>')
def get_paynum(user_id):
    try:
        num = random.randint(100000,999999)
        User2.query.filter_by(user_id=user_id).update({'pay_num': str(num)})
        db.session.commit()
        result_json = "{\"pay_num\":" + str(num) + ",\"ok\":1}"
        timer = threading.Timer(120, delete_paynum, (user_id,))
        timer.start()
    except:
        return "{\"ok\":0}"
    return result_json

#根据手机号充值，返回余额（有被破解风险，网址给些乱码感觉好一点）还要储存充值记录
# Done
@app.route('/nvaueph8793q/phone_num/<phone_num>/money/<money>')
def recharge(phone_num,money):
    the_user = User2.query.filter_by(phone_num=phone_num).first()
    new_money = float(the_user.money) + float(money)
    User2.query.filter_by(phone_num=phone_num).update({'money': str(new_money)})
    record = the_user.record
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    record += str(nowTime) + "充值：" + str(money) + "元；余额：" + str(new_money) + "元,"
    User2.query.filter_by(phone_num=phone_num).update({'record': record})
    db.session.commit()
    result_json = "{\"money\":" + str(new_money) + ",\"ok\":1}"
    return result_json

#根据支付密码消费，返回余额，还要储存消费记录
@app.route('/pay_num/<pay_num>/money/<money>')
def consume(pay_num,money):
    the_user = User2.query.filter_by(pay_num=pay_num).first()
    new_money = float(the_user.money) - float(money)
    if(new_money < 0):
        return "{\"ok\":0}"
    else:
        User2.query.filter_by(pay_num=pay_num).update({'money': str(new_money)})
        record = the_user.record
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        record += str(nowTime) + "消费：" + str(money) + "元；余额：" + str(new_money) + "元,"
        User2.query.filter_by(pay_num=pay_num).update({'record': record})
        db.session.commit()
        result_json = "{\"money\":" + str(new_money) + ",\"ok\":1}"
        return result_json

#根据id返回账单记录
# Done
@app.route('/record/<phone_num>')
def record(phone_num):
    the_user = User2.query.filter_by(phone_num=phone_num).first()
    result_json = "{\"record\":\"" + the_user.record + "\",\"ok\":1}"
    return result_json

if __name__ == "__main__":
    #print(get_openid("0334rMMm0mBAPr1c4vQm0D1tMm04rMMm"))
    app.run()
    #WSGIServer(('0.0.0.0', 80), app).serve_forever()

