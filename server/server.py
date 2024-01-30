import json
import logging
import os
from random import sample
from string import ascii_letters, digits
import time
import datetime
import uuid

import sqlite3

from flask import Flask, jsonify, request

from wechatpayv3 import WeChatPay, WeChatPayType

# 微信支付商户号（直连模式）或服务商商户号（服务商模式，即sp_mchid)
MCHID = '1667193471'

# 商户证书私钥
with open('keys/apiclient_key.pem') as f:
    PRIVATE_KEY = f.read()

# 商户证书序列号
CERT_SERIAL_NO = '4CC3C19EBAF0048674DA6BB6D0D7567F4EBF10D2'

# API v3密钥， https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay3_2.shtml
APIV3_KEY = 'Wl6HARMdq4NpJkgHtDy5xcZyVxQXOUdZ'

# APPID，应用ID或服务商模式下的sp_appid
APPID = 'wx2efa605350289bee'

# 回调地址，也可以在调用接口的时候覆盖
NOTIFY_URL = 'https://www.xxxx.com/notify'

# 微信支付平台证书缓存目录，减少证书下载调用次数，首次使用确保此目录为空目录.
# 初始调试时可不设置，调试通过后再设置，示例值:'./cert'
CERT_DIR = None

# 日志记录器，记录web请求和回调细节
logging.basicConfig(filename=os.path.join(os.getcwd(), 'demo.log'), level=logging.DEBUG, filemode='a', format='%(asctime)s - %(process)s - %(levelname)s: %(message)s')
LOGGER = logging.getLogger("demo")

# 接入模式:False=直连商户模式，True=服务商模式
PARTNER_MODE = False

# 代理设置，None或者{"https": "http://10.10.1.10:1080"}，详细格式参见https://docs.python-requests.org/zh_CN/latest/user/advanced.html
PROXY = None

# 初始化
wxpay = WeChatPay(
    wechatpay_type=WeChatPayType.NATIVE,
    mchid=MCHID,
    private_key=PRIVATE_KEY,
    cert_serial_no=CERT_SERIAL_NO,
    apiv3_key=APIV3_KEY,
    appid=APPID,
    notify_url=NOTIFY_URL,
    cert_dir=CERT_DIR,
    logger=LOGGER,
    partner_mode=PARTNER_MODE,
    proxy=PROXY)

def get_db():
    conn = sqlite3.connect('user_data.db')
    return conn

def init_db():
    db = get_db()
    cur = db.cursor()
    # 建表语句
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
                    wxid TEXT,
                    createtime INTEGER,
                    category INTEGER,
                    contactconfig TEXT
            )""")
    # 执行
    db.commit()
    db.close()

def query_db(sql: str):
    db = get_db()
    cur = db.cursor()
    cur.execute(sql)
    records = cur.fetchall()
    db.close()
    return records

def insert_db(wxid: str, createtime: int, category: int, contactconfig: str):
    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (wxid, createtime, category, contactconfig))
    # 执行
    db.commit()
    db.close()

def update_category_db(wxid: str, category: int):
    createtime = int(time.time())
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE users SET createtime = ?, category = ? WHERE wxid = ?", (createtime, category, wxid))
    # 执行
    db.commit()
    db.close()

def update_contactconfig_db(wxid: str, contactconfig: str):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE users SET contactconfig = ? WHERE wxid = ?", (contactconfig, wxid))
    # 执行
    db.commit()
    db.close()

def is_overdue(input_timestamp: int, days: int) -> bool:
    """检测是否超期"""
    input_datetime = datetime.datetime.utcfromtimestamp(input_timestamp)

    current_datetime = datetime.datetime.utcnow()

    time_difference = current_datetime - input_datetime

    return time_difference.days > days



app = Flask(__name__)

@app.route('/get_info', methods=['POST'])
def get_info():
    """获取账户信息"""
    data = request.get_json()
    if data:
        pass
    else:
        data = request.get_data()
        data = json.loads(data)

    wxid = data["wxid"]
    sql = f"SELECT * FROM users WHERE wxid = '{wxid}'"
    result = query_db(sql)  # 查询是否有这个wxid

    if len(result) == 0:
        createtime = int(time.time())
        category = 0
        contactconfig = json.dumps({})
        insert_db(wxid, createtime, category, contactconfig)  # 新用户则插入数据
    else:
        createtime = result[0][1]  # 如果用户重新购买了，则应该更新此项
        if is_overdue(createtime, 30):  # 如果超期则恢复普通身份
            update_category_db(wxid, 0)  # 更新恢复普通身份
            category = 0
        else:
            category = result[0][2]  # 可能是vip可能是普通身份

        contactconfig = result[0][3]  # 储存的联系人配置列表

    versions = ['1.0']  # 所支持的版本列表，如果客户端检测自身版本不在其中，客户端需要更新

    return jsonify({'versions': versions, 'wxid': wxid, 'createtime': createtime, 'category': category, 'contactconfig': contactconfig})


@app.route('/commit_info', methods=['POST'])
def commit_info():
    """提交保存联系人配置文件"""
    data = request.get_json()
    if data:
        pass
    else:
        data = request.get_data()
        data = json.loads(data)

    wxid = data['wxid']
    contactconfig = data['contactconfig']
    update_contactconfig_db(wxid, contactconfig)  # 更新配置文件
    return jsonify({'status': 'ok'})

@app.route('/pay')
def pay():
    # 以native下单为例，下单成功后即可获取到'code_url'，将'code_url'转换为二维码，并用微信扫码即可进行支付测试。
    out_trade_no = ''.join(sample(ascii_letters + digits, 8))
    description = '个人助手月度会员'
    amount = 990
    code, message = wxpay.pay(
        description=description,
        out_trade_no=out_trade_no,
        amount={'total': amount},
        pay_type=WeChatPayType.NATIVE
    )
    return jsonify({'code': code, 'message': message})

@app.route('/notify', methods=['POST'])
def notify():
    result = wxpay.callback(request.headers, request.data)
    if result and result.get('event_type') == 'TRANSACTION.SUCCESS':
        resp = result.get('resource')
        appid = resp.get('appid')
        mchid = resp.get('mchid')
        out_trade_no = resp.get('out_trade_no')
        transaction_id = resp.get('transaction_id')
        trade_type = resp.get('trade_type')
        trade_state = resp.get('trade_state')
        trade_state_desc = resp.get('trade_state_desc')
        bank_type = resp.get('bank_type')
        attach = resp.get('attach')
        success_time = resp.get('success_time')
        payer = resp.get('payer')
        amount = resp.get('amount').get('total')
        # TODO: 根据返回参数进行必要的业务处理，处理完后返回200或204
        return jsonify({'code': 'SUCCESS', 'message': '成功'})
    else:
        return jsonify({'code': 'FAILED', 'message': '失败'}), 500


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
