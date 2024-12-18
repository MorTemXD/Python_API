from flask import Flask, jsonify, request
from config import Config
from models import db, Movie, Director, Actor, ProductionCompany, Genre
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return jsonify([movie.to_dict() for movie in movies])

@app.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return jsonify(movie.to_dict())

@app.route('/movies', methods=['POST'])
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
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return '', 204

@app.route('/directors', methods=['GET'])
def get_directors():
    directors = Director.query.all()
    return jsonify([director.to_dict() for director in directors])

@app.route('/directors/<int:director_id>', methods=['GET'])
def get_director(director_id):
    director = Director.query.get_or_404(director_id)
    return jsonify(director.to_dict())

@app.route('/directors', methods=['POST'])
def create_director():
    data = request.get_json()
    director = Director(
        first_name=data['first_name'],
        last_name=data['last_name'],
        birth_date=datetime.strptime(data['birth_date'], '%Y-%m-%d').date() if data.get('birth_date') else None,
        nationality=data.get('nationality'),
        biography=data.get('biography')
    )
    db.session.add(director)
    db.session.commit()
    return jsonify(director.to_dict()), 201

@app.route('/directors/<int:director_id>', methods=['PUT'])
def update_director(director_id):
    director = Director.query.get_or_404(director_id)
    data = request.get_json()

    if 'first_name' in data:
        director.first_name = data['first_name']
    if 'last_name' in data:
        director.last_name = data['last_name']
    if 'birth_date' in data:
        director.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
    if 'nationality' in data:
        director.nationality = data['nationality']
    if 'biography' in data:
        director.biography = data['biography']

    db.session.commit()
    return jsonify(director.to_dict())

@app.route('/directors/<int:director_id>', methods=['DELETE'])
def delete_director(director_id):
    director = Director.query.get_or_404(director_id)
    db.session.delete(director)
    db.session.commit()
    return '', 204

@app.route('/actors', methods=['GET'])
def get_actors():
    actors = Actor.query.all()
    return jsonify([actor.to_dict() for actor in actors])

@app.route('/actors/<int:actor_id>', methods=['GET'])
def get_actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    return jsonify(actor.to_dict())

@app.route('/actors', methods=['POST'])
def create_actor():
    data = request.get_json()
    actor = Actor(
        first_name=data['first_name'],
        last_name=data['last_name'],
        birth_date=datetime.strptime(data['birth_date'], '%Y-%m-%d').date() if data.get('birth_date') else None,
        nationality=data.get('nationality'),
        biography=data.get('biography')
    )
    db.session.add(actor)
    db.session.commit()
    return jsonify(actor.to_dict()), 201

@app.route('/actors/<int:actor_id>', methods=['PUT'])
def update_actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    data = request.get_json()

    if 'first_name' in data:
        actor.first_name = data['first_name']
    if 'last_name' in data:
        actor.last_name = data['last_name']
    if 'birth_date' in data:
        actor.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
    if 'nationality' in data:
        actor.nationality = data['nationality']
    if 'biography' in data:
        actor.biography = data['biography']

    db.session.commit()
    return jsonify(actor.to_dict())

@app.route('/actors/<int:actor_id>', methods=['DELETE'])
def delete_actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    db.session.delete(actor)
    db.session.commit()
    return '', 204

@app.route('/companies', methods=['GET'])
def get_companies():
    companies = ProductionCompany.query.all()
    return jsonify([company.to_dict() for company in companies])

@app.route('/companies/<int:company_id>', methods=['GET'])
def get_company(company_id):
    company = ProductionCompany.query.get_or_404(company_id)
    return jsonify(company.to_dict())

@app.route('/companies', methods=['POST'])
def create_company():
    data = request.get_json()
    company = ProductionCompany(
        name=data['name'],
        country=data.get('country'),
        founding_date=datetime.strptime(data['founding_date'], '%Y-%m-%d').date() if data.get('founding_date') else None,
        description=data.get('description')
    )
    db.session.add(company)
    db.session.commit()
    return jsonify(company.to_dict()), 201

@app.route('/companies/<int:company_id>', methods=['PUT'])
def update_company(company_id):
    company = ProductionCompany.query.get_or_404(company_id)
    data = request.get_json()

    if 'name' in data:
        company.name = data['name']
    if 'country' in data:
        company.country = data['country']
    if 'founding_date' in data:
        company.founding_date = datetime.strptime(data['founding_date'], '%Y-%m-%d').date()
    if 'description' in data:
        company.description = data['description']

    db.session.commit()
    return jsonify(company.to_dict())

@app.route('/companies/<int:company_id>', methods=['DELETE'])
def delete_company(company_id):
    company = ProductionCompany.query.get_or_404(company_id)
    db.session.delete(company)
    db.session.commit()
    return '', 204

@app.route('/genres', methods=['GET'])
def get_genres():
    genres = Genre.query.all()
    return jsonify([genre.to_dict() for genre in genres])

@app.route('/genres/<int:genre_id>', methods=['GET'])
def get_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    return jsonify(genre.to_dict())

@app.route('/genres', methods=['POST'])
def create_genre():
    data = request.get_json()
    genre = Genre(
        name=data['name'],
        description=data.get('description')
    )
    db.session.add(genre)
    db.session.commit()
    return jsonify(genre.to_dict()), 201

@app.route('/genres/<int:genre_id>', methods=['PUT'])
def update_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    data = request.get_json()

    if 'name' in data:
        genre.name = data['name']
    if 'description' in data:
        genre.description = data['description']

    db.session.commit()
    return jsonify(genre.to_dict())

@app.route('/genres/<int:genre_id>', methods=['DELETE'])
def delete_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    db.session.delete(genre)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
