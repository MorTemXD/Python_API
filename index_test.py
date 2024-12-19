from app import create_app
from models import db
from datetime import date
import time
from sqlalchemy import text

app = None

def create_indexes():
    global app
    with app.app_context():
        db.session.execute(text('''
            CREATE INDEX IF NOT EXISTS idx_movie_budget ON movie(budget);
            CREATE INDEX IF NOT EXISTS idx_movie_release_date ON movie(release_date);
            CREATE INDEX IF NOT EXISTS idx_movie_box_office ON movie(box_office);
            CREATE INDEX IF NOT EXISTS idx_movie_director ON movie(director_id);
            CREATE INDEX IF NOT EXISTS idx_movie_company ON movie(production_company_id);
            CREATE INDEX IF NOT EXISTS idx_movie_genres ON movie_genres(movie_id, genre_id);
            CREATE INDEX IF NOT EXISTS idx_movie_actors ON movie_actors(movie_id, actor_id);
        '''))
        db.session.commit()

def test_operations(num_executions):
    global app
    with app.app_context():
        results = {}
        
        # SELECT test
        start_time = time.time()
        for _ in range(num_executions):
            db.session.execute(text('''
                SELECT * FROM movie 
                WHERE budget > 50000000 
                LIMIT 1
            '''))
        results['SELECT'] = time.time() - start_time

        # UPDATE test
        start_time = time.time()
        for _ in range(num_executions):
            db.session.execute(text('''
                UPDATE movie 
                SET budget = budget * 1.01 
                WHERE id = (SELECT id FROM movie LIMIT 1)
            '''))
        results['UPDATE'] = time.time() - start_time

        # INSERT test
        start_time = time.time()
        for _ in range(num_executions):
            db.session.execute(text('''
                INSERT INTO movie (title, release_date, budget) 
                VALUES ('Test Movie', '2024-01-01', 1000000)
            '''))
        results['INSERT'] = time.time() - start_time

        # DELETE test
        start_time = time.time()
        for _ in range(num_executions):
            db.session.execute(text('''
                DELETE FROM movie 
                WHERE id = (SELECT id FROM movie WHERE title = 'Test Movie' LIMIT 1)
            '''))
        results['DELETE'] = time.time() - start_time

        db.session.commit()
        return results

def print_results_table(operation, results):
    print(f"\n{operation} operations:")
    print("-" * 75)
    print(f"{'Count':>12} | {'Total time (sec)':>16} | {'Average time (ms)':>16}")
    print("-" * 75)
    
    for count, time_taken in results:
        avg_time = (time_taken/count) * 1000
        print(f"{count:>12} | {time_taken:>16.2f} | {avg_time:>16.3f}")

def run_tests():
    global app
    app = create_app()
    
    print("\nCreating indexes...")
    create_indexes()
    
    execution_counts = [1000, 10000, 100000, 1000000]
    operation_results = {
        'SELECT': [],
        'UPDATE': [],
        'INSERT': [],
        'DELETE': []
    }
    
    for count in execution_counts:
        print(f"\nTesting {count} queries...")
        times = test_operations(count)
        
        for operation, execution_time in times.items():
            operation_results[operation].append((count, execution_time))
    
    print("\nTEST RESULTS:")
    print("=" * 75)
    
    for operation in ['SELECT', 'UPDATE', 'INSERT', 'DELETE']:
        print_results_table(operation, operation_results[operation])

if __name__ == '__main__':
    run_tests() 