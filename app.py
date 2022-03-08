import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

SECRET_KEY = 'bread'

app = Flask(__name__)

# DB연결
from pymongo import MongoClient
client = MongoClient('mongodb+srv://gibeks:1234@Cluster0.htlw2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/login', methods=["POST"])
def signin(SECRET_KEY=None):
    # 로그인
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    result = db.busers.find_one({'id': id_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/reg')
def register():
    msg = request.args.get("msg")
    return render_template('register.html', msg=msg)

@app.route('/reg/checkIdDup', methods=["POST"])
def checkiddup():
    id_receive = request.form['id_give']
    exists = bool(db.busers.find_one({"id": id_receive}))
    return jsonify({'result': 'success', 'exists': exists})

@app.route('/reg/checkNickDup', methods=["POST"])
def checknickdup():
    nick_receive = request.form['nick_give']
    exists = bool(db.busers.find_one({"nick": nick_receive}))
    return jsonify({'result': 'success', 'exists': exists})

@app.route('/reg/save', methods=['POST'])
def join():
    id_receive = request.form['id_give']
    nick_receive = request.form['nick_give']
    pw_receive = request.form['pw_give']
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    doc = {
        "id": id_receive,                                           # 아이디
        "nick": nick_receive,                                       # 닉네임
        "pw": pw_hash,                                              # 비밀번호
    }
    db.busers.insert_one(doc)
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5050, debug=True)