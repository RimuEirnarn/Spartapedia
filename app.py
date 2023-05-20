"""App"""
from os import environ
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

from crawler import get_data

load_dotenv(join(dirname(__file__), '.env'))

client = MongoClient(environ.get("MONGODB_URI"))
database = client[environ.get("DB_NAME")]
spartapedia = database.spartapedia
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/movie", methods=["POST"])
def movie_post():
    movie_url = request.form['movie']
    rating = request.form['rating']
    comment = request.form['comment']
    try:
        movie = get_data(movie_url)
    except Exception as exc:
        return jsonify({"status": 'error', 'message': str(exc)}), 400
    spartapedia.insert_one({
        'movieData': {
            'title': movie.title,
            'desc': movie.desc,
            'image': movie.image
        },
        'rating': rating,
        'comment': comment
    })
    return jsonify({'status': 'success', 'message': "Post success", "data": {'movie': {"title": movie.title, "desc": movie.desc, "image": movie.image}, "rating": rating, "comment": comment}})


@app.route("/movie", methods=["GET"])
def movie_get():
    data = spartapedia.find(projection={'_id': False})
    return jsonify({'status': 'success', 'request': list(data)})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
