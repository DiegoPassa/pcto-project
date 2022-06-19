from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_gravatar import Gravatar


from flask_navigation import Navigation

from app.lib.conn import ConnectionData

app = Flask(__name__)
nav = Navigation(app)
app.config['SECRET_KEY'] = 'e617cdbc1721d5469e8345acd2c7e5c3'
app.config['SQLALCHEMY_DATABASE_URI'] = ConnectionData.get_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='mp',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

from app.views.main.routes import main
from app.views.students.routes import students
from app.views.teachers.routes import teachers

app.register_blueprint(main)
app.register_blueprint(students, url_prefix='/student')
app.register_blueprint(teachers, url_prefix='/teacher')

nav.Bar('not_logged', [
    nav.Item('Accedi', 'main.login'),
    nav.Item('Registrati', 'main.register'),
])

nav.Bar('students', [
    nav.Item('Corsi', 'students.dashboard'),
    nav.Item('I miei corsi', 'students.user_courses'),
    # nav.Item('Profilo', 'students.profile'),
    # nav.Item('Logout', 'main.logout'),
])

nav.Bar('teachers', [
    nav.Item('Gestione corsi', 'teachers.dashboard'),
    # nav.Item('Profilo', 'teachers.profile'),
    # nav.Item('Logout', 'main.logout'),
])