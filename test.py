from app import create_app
from models import db, Movie, Director, Actor, ProductionCompany, Genre
from datetime import date, datetime
import random
import time
import string

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

def generate_random_date():
    year = random.randint(1950, 2024)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return date(year, month, day)

def clear_db():
    with app.app_context():
        db.session.execute(db.table('movie_actors').delete())
        db.session.execute(db.table('movie_genres').delete())
        Movie.query.delete()
        Actor.query.delete()
        Director.query.delete()
        ProductionCompany.query.delete()
        Genre.query.delete()
        db.session.commit()

def populate_db(num_records):
    with app.app_context():
        genres = []
        for i in range(10):
            genre = Genre(
                name=f'Жанр_{i}',
                description=generate_random_string(50)
            )
            db.session.add(genre)
            genres.append(genre)

        companies = []
        for i in range(20):
            company = ProductionCompany(
                name=f'Компания_{i}',
                country=generate_random_string(10),
                founding_date=generate_random_date(),
                description=generate_random_string(50)
            )
            db.session.add(company)
            companies.append(company)

        directors = []
        for i in range(50):
            director = Director(
                first_name=generate_random_string(10),
                last_name=generate_random_string(15),
                birth_date=generate_random_date(),
                nationality=generate_random_string(15),
                biography=generate_random_string(50)
            )
            db.session.add(director)
            directors.append(director)

        actors = []
        for i in range(100):
            actor = Actor(
                first_name=generate_random_string(10),
                last_name=generate_random_string(15),
                birth_date=generate_random_date(),
                nationality=generate_random_string(15),
                biography=generate_random_string(50)
            )
            db.session.add(actor)
            actors.append(actor)

        db.session.commit()

        batch_size = 1000
        for i in range(0, num_records, batch_size):
            batch_movies = []
            for j in range(min(batch_size, num_records - i)):
                movie = Movie(
                    title=f'Фильм_{i+j}',
                    description=generate_random_string(200),
                    release_date=generate_random_date(),
                    budget=random.uniform(1000000, 300000000),
                    box_office=random.uniform(1000000, 1000000000),
                    duration=random.randint(80, 240),
                    director=random.choice(directors),
                    production_company=random.choice(companies)
                )
                movie.actors.extend(random.sample(actors, random.randint(2, 5)))
                movie.genres.extend(random.sample(genres, random.randint(1, 3)))
                batch_movies.append(movie)
            
            db.session.add_all(batch_movies)
            db.session.commit()

def test_select(num_records):
    with app.app_context():
        start_time = time.time()
        movies = Movie.query.all()
        end_time = time.time()
        return end_time - start_time

def test_update(num_records):
    with app.app_context():
        start_time = time.time()
        movies = Movie.query.limit(num_records // 2).all()
        for movie in movies:
            movie.description = generate_random_string(200)
        db.session.commit()
        end_time = time.time()
        return end_time - start_time

def test_insert(num_records):
    with app.app_context():
        start_time = time.time()
        director = Director.query.first()
        company = ProductionCompany.query.first()
        
        for i in range(100):
            movie = Movie(
                title=f'Новый_фильм_{i}',
                description=generate_random_string(200),
                release_date=generate_random_date(),
                budget=random.uniform(1000000, 300000000),
                box_office=random.uniform(1000000, 1000000000),
                duration=random.randint(80, 240),
                director=director,
                production_company=company
            )
            db.session.add(movie)
        db.session.commit()
        end_time = time.time()
        return end_time - start_time

def test_delete(num_records):
    with app.app_context():
        start_time = time.time()
        movies = Movie.query.limit(100).all()
        for movie in movies:
            db.session.delete(movie)
        db.session.commit()
        end_time = time.time()
        return end_time - start_time

def run_performance_tests():
    record_counts = [1000, 10000, 100000, 1000000]
    results = {}

    for count in record_counts:
        print(f"\nТестирование для {count} записей:")
        clear_db()
        populate_db(count)
        
        results[count] = {
            'select': test_select(count),
            'update': test_update(count),
            'insert': test_insert(count),
            'delete': test_delete(count)
        }
        
        print(f"SELECT: {results[count]['select']:.2f} сек")
        print(f"UPDATE: {results[count]['update']:.2f} сек")
        print(f"INSERT: {results[count]['insert']:.2f} сек")
        print(f"DELETE: {results[count]['delete']:.2f} сек")

    return results

if __name__ == '__main__':
    app = create_app()
    results = run_performance_tests() 