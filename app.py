from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt, get_jwt_identity
from config import Config
from models import db, Movie, Director, Actor, ProductionCompany, Genre
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

revoked_tokens = set()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    JWTManager(app)
    return app

app = create_app()
jwt = JWTManager(app)

class User:
    USERS = {
        "user1": generate_password_hash("password1"),
        "user2": generate_password_hash("password2"),
    }

    @classmethod
    def verify(cls, username, password):
        if username in cls.USERS and check_password_hash(cls.USERS[username], password):
            return True
        return False

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return jwt_payload["jti"] in revoked_tokens

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not User.verify(username, password):
        return jsonify({"msg": "Invalid username or password"}), 401

    access_token = create_access_token(identity=username, expires_delta=timedelta(hours=1))
    return jsonify(access_token=access_token)

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    revoked_tokens.add(jti)
    return jsonify({"msg": "Access token revoked"}), 200

@app.route('/movies', methods=['GET'])
@jwt_required()
def get_movies():
    movies = Movie.query.all()
    return jsonify([movie.to_dict() for movie in movies])

@app.route('/movies/<int:movie_id>', methods=['GET'])
@jwt_required()
def get_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return jsonify(movie.to_dict())

@app.route('/movies', methods=['POST'])
@jwt_required()
def create_movie():
    data = request.get_json()
    movie = Movie(
        title=data['title'],
        description=data.get('description'),
        release_date=datetime.strptime(data['release_date'], '%Y-%m-%d').date(),
        budget=data.get('budget'),
        box_office=data.get('box_office'),
        duration=data.get('duration'),
        director_id=data.get('director_id'),
        production_company_id=data.get('production_company_id')
    )

    if 'actor_ids' in data:
        actors = Actor.query.filter(Actor.id.in_(data['actor_ids'])).all()
        movie.actors.extend(actors)

    if 'genre_ids' in data:
        genres = Genre.query.filter(Genre.id.in_(data['genre_ids'])).all()
        movie.genres.extend(genres)

    db.session.add(movie)
    db.session.commit()
    return jsonify(movie.to_dict()), 201

@app.route('/movies/<int:movie_id>', methods=['PUT'])
@jwt_required()
def update_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    data = request.get_json()

    if 'title' in data:
        movie.title = data['title']
    if 'description' in data:
        movie.description = data['description']
    if 'release_date' in data:
        movie.release_date = datetime.strptime(data['release_date'], '%Y-%m-%d').date()
    if 'budget' in data:
        movie.budget = data['budget']
    if 'box_office' in data:
        movie.box_office = data['box_office']
    if 'duration' in data:
        movie.duration = data['duration']
    if 'director_id' in data:
        movie.director_id = data['director_id']
    if 'production_company_id' in data:
        movie.production_company_id = data['production_company_id']

    if 'actor_ids' in data:
        movie.actors = []
        actors = Actor.query.filter(Actor.id.in_(data['actor_ids'])).all()
        movie.actors.extend(actors)

    if 'genre_ids' in data:
        movie.genres = []
        genres = Genre.query.filter(Genre.id.in_(data['genre_ids'])).all()
        movie.genres.extend(genres)

    db.session.commit()
    return jsonify(movie.to_dict())

@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@jwt_required()
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return '', 204


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
