from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(200), unique=False, nullable=False)
    done = db.Column(db.Boolean, unique=False, default=False)
    #user = db.relationship(User)
    #user_id = db.Column(Integer, ForeignKey('users.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def serialize(self):
        return {
            "label": self.label,
            "done": self.done
        }

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=False, nullable=False)
    tasks = db.relationship('Task', backref='users', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

# class Person(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return '<Person %r>' % self.username

#     def serialize(self):
#         return {
#             "username": self.username,
#             "email": self.email
#         }