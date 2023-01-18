from flask import Flask, jsonify
from utils import get_all, get_one


app = Flask(__name__)


@app.route('/movie/<title>')
def get_movie_by_title(title):
    query = f"""SELECT * FROM netflix WHERE title = '{title}' ORDER BY date_added DESC"""

    result = get_one(query)

    if result is None:
        return jsonify(status=404)

    movie = {
        'title': result['title'],
        'country': result['country'],
        'release_year': result['release_year'],
        'genre': result['listed_in'],
        'description': result['description'],
    }

    return jsonify(movie)


@app.route('/movie/<year1>/to/<year2>')
def get_movie_by_year(year1, year2):
    query = f"""SELECT * FROM netflix WHERE release_year BETWEEN {year1} AND {year2} LIMIT 100"""

    result = []

    for item in get_all(query):
        result.append(
            {
                'title': item['title'],
                'release_year': item['release_year'],
            }
        )

    return jsonify(result)


@app.route('/movie/rating/<rating>')
def get_movie_by_rating(rating):
    if rating == 'children':
        query = """SELECT * FROM netflix WHERE rating = 'G'"""
    elif rating == 'family':
        query = """SELECT * FROM netflix WHERE rating = 'G' OR rating = 'PG' OR rating = 'PG-13'"""
    elif rating == 'adult':
        query = """SELECT * FROM netflix WHERE rating = 'R' OR rating = 'NC-17'"""
    else:
        return jsonify(status=400)

    result = []

    for item in get_all(query):
        result.append(
            {
                'title': item['title'],
                'rating': item['rating'],
                'description': item['description'],
            }
        )

    return jsonify(result)


@app.route('/genre/<genre>')
def get_movie_by_genre(genre):
    query = f"""SELECT * FROM netflix WHERE listed_in LIKE '%{genre}%' ORDER BY date_added DESC LIMIT 10"""

    result = []

    for item in get_all(query):
        result.append(
            {
                'title': item['title'],
                'description': item['description'],
            }
        )

    return jsonify(result)


app.run()
