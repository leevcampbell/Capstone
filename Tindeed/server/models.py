from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates, relationships
from sqlalchemy.ext.associationproxy import association_proxy
from flask import Flask, request



metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False) 
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    bio = db.Column(db.String, nullable=True, default='')
    image = db.Column(db.String, nullable=True, default='https://static.vecteezy.com/system/resources/previews/008/442/086/original/illustration-of-human-icon-user-symbol-icon-modern-design-on-blank-background-free-vector.jpg') 
    experience = db.Column(db.Integer)
    matched_projects = db.relationship('MatchedUsers', backref='user', lazy=True)
    projects = association_proxy('matched_users', 'project')

    equipment = db.relationship('UserEquip', backref='user', lazy=True)
    equip = association_proxy('userequip', 'equipment')
    

    def __repr__(self):
        return f'<User {self.name} {self.username} {self.email} {self.location} {self.experience} {self.bio} >'


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'location': self.location,
            'bio': self.bio,
            'experience': self.experience,
        }

        @validates('email')
        def validate_email(self, key, email):
            if email == '':
                raise ValueError('Email must not be blank')
            if User.query.filter(User.email == email).first():
                raise AssertionError('Email is already in use')
            return email

        @validates('username')
        def validate_username(self, key, username):
            if username == '':
                raise ValueError('Username must not be blank')
            if User.query.filter(User.username == username).first():
                raise AssertionError('Username is already in use. Please choose another')
            return username

        @validates('password')
        def validate_password(self, key, password):
            if password == '':
                raise AssertionError('No password provided')
            if len(password) < 4:
                raise AssertionError('Password must be at least 8 characters')
            return password

        @validates('location')
        def validate_location(self, key, location):
            parts = location.split(',')
            if len(parts) >= 2:
                city = parts[0].strip()
                state = parts[1].strip()
                if city and state:
                    return f'{city}, {state}'
                else:
                    return {'Must provide a city and state/country'}

        @validates('experience')
        def validate_experience(self, key, experience):
            if type(experience) != int:
                raise AssertionError('Experience must be a number')
            if experience < 0:
                raise AssertionError('Experience must be a positive number')
            return experience


class Projects(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)
    location = db.Column(db.String, nullable=True, default='')
    genre = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=True, default='https://static.vecteezy.com/system/resources/previews/005/903/347/original/gold-abstract-letter-s-logo-for-negative-video-recording-film-production-free-vector.jpg')
    matched_users = db.relationship('MatchedUsers', backref='project', lazy=True)
    users = association_proxy('matched_users', 'user')

    def __repr__(self):
        return f'<Projects {self.title} owner= {self.owner_id} {self.description} {self.location} {self.genre} {self.image}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'owner_id': self.owner_id,
            'location': self.location,
            'genre': self.genre,
            'image': self.image,
            'users': [user.to_dict() for user in self.users]
        }

    @validates('title')
    def validate_title(self, key, title):
        if title == '':
            raise ValueError('Project must have a title')
        return title

    @validates('description')
    def validate_description(self, key, description):
        if description == '':
            raise ValueError('Project must have a description')
        return description

    @validates('genre')
    def validate_genre(self, key, genre):
        if genre == '':
            raise ValueError('Project must have a genre')
        return genre



class OwnerUser(db.Model):
    __tablename__ = 'owner'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    bio = db.Column(db.String, nullable=True, default="")
    experience = db.Column(db.Integer)
    projects = db.relationship('Projects', backref='owner', lazy=True)

    def __repr__(self):
        return f'<Owner {self.name} {self.username} {self.email} {self.location} {self.bio} {self.experience}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'location': self.location,
            'bio': self.bio,
            'experience': self.experience,
            'projects': [project.to_dict() for project in self.projects]
        }

        @validates('email')
        def validate_email(self, key, email):
            if email == '':
                raise ValueError('Email must not be blank')
            if User.query.filter(User.email == email).first():
                raise AssertionError('Email is already in use')
            return email

        @validates('username')
        def validate_username(self, key, username):
            if username == '':
                raise ValueError('Username must not be blank')
            if User.query.filter(User.username == username).first():
                raise AssertionError('Username is already in use. Please choose another')
            return username

        @validates('password')
        def validate_password(self, key, password):
            if password == '':
                raise AssertionError('No password provided')
            if len(password) < 4:
                raise AssertionError('Password must be at least 8 characters')
            return password

        @validates('location')
        def validate_location(self, key, location):
            parts = location.split(',')
            if len(parts) >= 2:
                city = parts[0].strip()
                state = parts[1].strip()
                if city and state:
                    return f'{city}, {state}'
                else:
                    return {'Must provide a city and state/country'}

        @validates('experience')
        def validate_experience(self, key, experience):
            if type(experience) != int:
                raise AssertionError('Experience must be a number')
            if experience < 0:
                raise AssertionError('Experience must be a positive number')
            return experience


#JOIN TABLES FOR USERS TO OWNERS 
class MatchedUsers(db.Model):
    __tablename__ = 'matched_users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    def __repr__(self):
        return f'<MatchedUsers {self.user_id} {self.project_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'project_id': self.project_id,
        }

#JOIN TABLE FOR USERS TO EQUIPMENT
class UserEquip(db.Model):
    __tablename__ = 'user_equip'
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<UserEquip {self.equipment_id} {self.user_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'equipment_id': self.equipment_id,
            'user_id': self.user_id,
        }

class Equipment(db.Model):
    __tablename__ = 'equipment'
    id = db.Column(db.Integer, primary_key=True)
    camera = db.Column(db.Boolean, nullable=False)
    lights = db.Column(db.Boolean, nullable=False)
    audio = db.Column(db.Boolean, nullable=False)
    props = db.Column(db.Boolean, nullable=False)
    editing_software = db.Column(db.Boolean, nullable=False)
    users = db.relationship('UserEquip', backref='equipment', lazy=True)
    user= association_proxy('userequip', 'user')

    



    


    



    