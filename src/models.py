from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    
    favorites_people = db.relationship("Favorites_People", back_populates="user")
    favorites_planets = db.relationship("Favorites_Planet", back_populates="user")


    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model):
    __tablename__='planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    climate = db.Column(db.String(80), nullable=False)
    terrain = db.Column(db.String(80), nullable=False)

    favorites_planets = db.relationship("Favorites_Planet", back_populates="planet")
    
    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain
        }
    


class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    birth_year = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(80), nullable=False)

    favorites_people = db.relationship("Favorites_People", back_populates="people")
    
    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender
        }



class Favorites_People(db.Model):
    __tablename__ = 'favorites_people'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", back_populates="favorites_people")
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    
    people = db.relationship("People", back_populates="favorites_people")

     
    def __repr__(self):
         return '<Favorites_People %r>' % self.id

    def serialize(self):
         return {
            "id": self.id,
            "people_name": self.people.name
         }



class Favorites_Planet(db.Model):
   __tablename__ = 'favorites_planet'
   id = db.Column(db.Integer, primary_key=True)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
   user = db.relationship("User", back_populates="favorites_planets")
   planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)
   
   planet = db.relationship("Planet", back_populates="favorites_planets")

   def __repr__(self):
         return '<Favorites_Planet %r>' % self.id

   def serialize(self):
        return {
             "id": self.id,
             "planet_name": self.planet.name if self.planet else None
         }