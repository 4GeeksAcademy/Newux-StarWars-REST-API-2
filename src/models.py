from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

favorite_planets = db.Table(
    'favorite_planets',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('planet_id', db.Integer, db.ForeignKey('planets.id'), primary_key=True)
)

favorite_people = db.Table(
    'favorite_people',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('person_id', db.Integer, db.ForeignKey('people.id'), primary_key=True)
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_planets = db.relationship("Planets", secondary=favorite_planets, lazy='subquery')
    favorite_people = db.relationship("People", secondary=favorite_people, lazy='subquery')


    def __repr__(self):
        return '<User %r >' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorite_planets": list(map(lambda x: x.serialize(), self.favorite_planets)),
            "favorite_people": list(map(lambda x: x.serialize(), self.favorite_people))
        }


class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    population = db.Column((db.Integer), nullable=False)
    climate = db.Column((db.String(50)), nullable=False)
    diameter = db.Column((db.Integer), nullable=False)
    terrain = db.Column(db.String(50), nullable=False)
    rotation_period = db.Column((db.Integer), nullable=False)

    def __repr__(self):
        return '<Planets %r >' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "climate": self.climate,
            "diameter": self.diameter,
            "terrain": self.terrain,
            "rotation_period": self.rotation_period
        }

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    height = db.Column((db.String(50)), nullable=False)
    hair_color = db.Column(db.String(50), nullable=False)
    eye_color = db.Column(db.String(50), nullable=False)
    birth_year = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<People %r >' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "height": self.height,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year
        }
    
