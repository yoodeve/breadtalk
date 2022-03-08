from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://gibeks:1234@Cluster0.htlw2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.dbsparta

from datetime import datetime


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/api/writing", methods=["POST"])
def save_review():
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



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)