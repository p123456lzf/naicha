# -*- coding: utf-8 -*-
from config import db

class User2(db.Model):
    user_id = db.Column(db.String(63),primary_key=True)
    user_name = db.Column(db.String(63), unique=True)
    phone_num =  db.Column(db.String(63), unique=True)
    money = db.Column(db.String(15))
    # 注意定时更新，否则长度会溢出，或者在插入时限制
    record = db.Column(db.Text(4095))
    pay_num = db.Column(db.String(13), unique=True)

    def __init__(self, user_id, user_name, phone_num, money, record, pay_num):
        self.user_id = user_id
        self.user_name = user_name
        self.phone_num = phone_num
        self.money = money
        self.record = record
        self.pay_num = pay_num


if __name__ == "__main__":
    db.create_all()
