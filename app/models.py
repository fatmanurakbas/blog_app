# app/models.py

# YENİ BİR NESNE OLUŞTURMAK YERİNE, __init__.py'DEKİ MEVCUT NESNEYİ İÇERİ AKTARIN
from app import db 
from datetime import datetime

# BU SATIRI SİLİN:
# from flask_sqlalchemy import SQLAlchemy
# BU SATIRI DA SİLİN:
# db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Post {self.title}>"

class Hero(db.Model):
    __tablename__ = 'Hero'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    title = db.Column(db.String(150))
    description = db.Column(db.String(500))
    background_image_url = db.Column(db.String(250))

    def __repr__(self):
        return f'<Hero {self.full_name}>'
    
class About(db.Model):
    __tablename__ = 'About'
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text)
    profile_image_url = db.Column(db.String(250))

    def __repr__(self):
        return f'<About {self.id}>'
    
class Projects(db.Model):
    __tablename__ = 'Projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(250))
    project_url = db.Column(db.String(250))
    

    def __repr__(self):
        return f'<Project {self.title}>'
    
class Blogs(db.Model):
    __tablename__ = 'Blogs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    cover_image_url = db.Column(db.String(250))
    published_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Blog {self.title}>'
    
class Experiences(db.Model):
    __tablename__ = 'Experiences'
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(200))
    role = db.Column(db.String(150))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date, nullable=True)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Experience {self.company} - {self.role}>'

class Skills(db.Model):
    __tablename__ = 'Skills'
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(100))
    level = db.Column(db.String(50))

    def __repr__(self):
        return f'<Skill {self.skill_name} - {self.level}>'
    
class Reference(db.Model):
    __tablename__ = 'Reference'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150))
    role = db.Column(db.String(150))
    company = db.Column(db.String(200))
    testimonial = db.Column(db.Text)
    image_url = db.Column(db.String(250))

    def __repr__(self):
        return f'<Reference {self.full_name} - {self.company}>'
    
class ContactMessage(db.Model):
    __tablename__ = 'ContactMessage'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ContactMessage from {self.name}>'    