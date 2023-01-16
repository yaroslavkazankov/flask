from flask_sqlalchemy import SQLAlchemy
from config import app
from flask_migrate import Migrate

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mail = db.Column(db.String(100), nullable=False)
    password = db.Column(db.Text(), nullable=False)

    def __init__(self, name, mail, password):
        self.name = name
        self.mail = mail
        self.password = password

    def __repr__(self):
        return f"Name: {self.name}"

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'mail': self.mail
                }


class Notifications(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title, description, date, owner_id):
        self.title = title
        self.description = description
        self.date = date
        self.owner_id = owner_id

    def __repr__(self):
        return {'id': self.id,
                'title': self.title,
                'description': self.description,
                'date': self.date,
                'owner_id': self.owner_id
                }

    def to_dict(self):
        return {'id': self.id,
                'title': self.title,
                'description': self.description,
                'date': self.date,
                'owner id': self.owner_id
                }
