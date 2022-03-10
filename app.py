from pymongo import MongoClient
client = MongoClient('mongodb+srv://gibeks:1234@Cluster0.htlw2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.dbsparta
# css수정 커밋
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
app = Flask(__name__)
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

SECRET_KEY = 'bread'

@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    title = "빵수다 | 메인페이지"
    user_info = ''
    if (token_receive is not None) :
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"id": payload["id"]})
    return render_template('index.html',title=title, user_info=user_info)

@app.route('/login')
def login():
    title = "빵수다 | 로그인"
    return render_template('login.html',title=title)


@app.route('/login/success', methods=["POST"])
def signin():
    # 로그인
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'id': id_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/reg')
def register():
    msg = request.args.get("msg")
    title = "빵수다 | 회원가입"
    return render_template('register.html', msg=msg, title=title)

@app.route('/reg/checkIdDup', methods=["POST"])
def checkiddup():
    id_receive = request.form['id_give']
    exists = bool(db.users.find_one({"id": id_receive}))
    return jsonify({'result': 'success', 'exists': exists})

@app.route('/reg/checkNickDup', methods=["POST"])
def checknickdup():
    nick_receive = request.form['nick_give']
    exists = bool(db.users.find_one({"nick": nick_receive}))
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
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

@app.route('/writing')
def write():
    title = "빵수다 | 리뷰 작성"
    token_receive = request.cookies.get('mytoken')
    user_info = ''
    if (token_receive is not None):
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"id": payload["id"]})
    return render_template('write.html', title=title, user_info=user_info)

@app.route("/writing/save", methods=["POST"])
def save_review():
    token_receive = request.cookies.get('mytoken')
    if (token_receive is not None):
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        id_receive = db.users.find_one({"id": payload["id"]})['id']

    store_receive = request.form['store_give']
    city_receive = request.form['city_give']
    city2_receive = request.form['city2_give']
    bread_name_receive = request.form['bread_name_give']
    comment_receive = request.form['comment_give']
    star_receive = request.form['star_give']

    # 파일 업로드 코드
    file = request.files["file_give"]

    extension = file.filename.split('.')[-1]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'file-{mytime}'

    save_to = f'static/{filename}.{extension}'
    file.save(save_to)

    review_list = list(db.review.find({}, {'_id': False}))
    count = len(review_list) + 1

    doc = {
        'id' : id_receive,
        'num': count,
        'store': store_receive,
        'city': city_receive,
        'city2': city2_receive,
        'bread_name': bread_name_receive,
        'comment': comment_receive,
        'star': star_receive,
        'file': f'{filename}.{extension}'
    }

    db.review.insert_one(doc)

    return jsonify({'msg': '등록 완료!!'})

# 리뷰 데이터 전달
@app.route("/api/read", methods=["GET"])
def review_get():
    review_list = list(db.review.find({}, {'_id': False}))
    return jsonify({'reviews': review_list})

# 로그인 정보를 메인페이지로 전달
@app.route('/')
def home_test():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        users_info = db.users.find_one({"id": payload["id"]})
        reviews = list(db.review.find({}))
        reviews.reverse()
        for review in reviews:
            review["review_id"] = str(review["_id"])
            print(review)

        return render_template('index.html', users_info=users_info, review=review)

    except jwt.ExpiredSignatureError:
       return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))

# 마이페이지로 정보전달
@app.route('/mypage/<id>')
def mypage(id):
    users_info = db.users.find_one({"id": id})
    nick = users_info['nick']
    reviews = list(db.review.find({"nick":nick}))
    return render_template('mypage.html', nick=nick, reviews=reviews, user_info=users_info)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)