from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta
import redis
from flask_migrate import Migrate
from flask_cors import CORS
from database import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'
app.config['JWT_SECRET_KEY'] = 'secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

jwt = JWTManager(app)
migrate = Migrate(app, db)
cors = CORS(app)

try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_client.ping()
    redis_available = True
except:
    redis_client = None
    redis_available = False
    print("Warning: Redis is not available. Caching will be disabled.")

if redis_available:
    from celery_app import celery
    celery.conf.update(
        broker_url='redis://localhost:6379',
        result_backend='redis://localhost:6379',
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
    )
else:
    celery = None
    print("Warning: Celery is disabled due to Redis unavailability.")

@app.route("/")
def index():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    
    from database import init_db
    init_db(app)
    
    from routes.auth import auth_bp
    from routes.subject import subject_bp
    from routes.chapter import chapter_bp
    from routes.quiz import quiz_bp
    from routes.score import score_bp
    from routes.question import question_bp
    from routes.dashboard import dashboard_bp
    from routes.tasks import task_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(subject_bp)
    app.register_blueprint(chapter_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(score_bp)
    app.register_blueprint(question_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(task_bp)
    
    app.run(debug=True, port=5000)
