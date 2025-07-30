from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route("/")
def index():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    # Initialize database
    from database import init_db
    init_db(app)
    
    app.run(debug=True, port=5000)
