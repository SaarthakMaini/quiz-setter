from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    
    import models
    
    with app.app_context():
        db.create_all()
        
        admin = models.User.query.filter_by(email='admin@quizmaster.com').first()
        if not admin:
            admin = models.User(
                username='admin',
                email='admin@quizmaster.com',
                full_name='Quiz Master Administrator',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: admin@quizmaster.com / admin123")
        else:
            print("Admin user already exists")