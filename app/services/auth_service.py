
from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask import current_app

from ..models.user_model import User


def signup_user(data):
    fullname = data['fullname']
    email = data['email']
    password = data['password']

    if not fullname or not email or not password:
        return {'error': 'نام, ایمیل و گذرواژه رو باید وارد کنی'}, 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return {'error': 'این ایمیل قبلا ثبت شده'}, 409

    hashed_password = generate_password_hash(password)

    new_user = User(fullname=fullname, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return {'message': f"ثبت کاربر با ایمیل: {email} با موفقیت انجام شد."}, 200


def login_user(data):
    email = data['email']
    password = data['password']

    if not email or not password:
        return {'error': 'ایمیل و گذرواژه رو باید وارد کنی'}, 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return {'error': 'ایمیل یا گذرواژه رو اشتباه وارد کردی'}, 401
    if not check_password_hash(user.password, password):
        return {'error': 'ایمیل یا گذرواژه رو اشتباه وارد کردی'}, 401

    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')

    return {'message': f'خوش آمدی {user.fullname}',
            'data': {'token': token, 'fullname': user.fullname, 'email': user.email}}, 200
