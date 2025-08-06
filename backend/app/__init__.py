from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studysync.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Disable automatic slash handling that causes 308 redirects
    app.url_map.strict_slashes = False
    
    db.init_app(app)
    
    # Configure CORS properly
    CORS(app, 
         origins=['http://localhost:3000'],
         methods=['GET', 'POST', 'OPTIONS'],
         allow_headers=['Content-Type'])
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from app.controllers.note_controller import note_bp
    app.register_blueprint(note_bp)
    
    @app.route('/')
    def home():
        return {'message': 'StudySync API is running!'}
    
    return app