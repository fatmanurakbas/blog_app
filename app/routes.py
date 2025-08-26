# app/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
# Formlarınız varsa bu import kalmalı, yoksa silebilirsiniz
# from app.forms import RegistrationForm, LoginForm 

# Projenizdeki tüm modelleri buradan import ediyoruz
from app.models import User, Hero, About, Projects, Blogs, Experiences, Skills, Reference

# __init__.py'den gelen db nesnesini import ediyoruz
from app import db 
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import RegistrationForm, LoginForm, ContactForm 

# 'main' adında bir Blueprint oluşturuyoruz
main = Blueprint('main', __name__)


# --- TÜM SAYFA ROUTE'LARI ARTIK BURADA ---

@main.route('/')
def index():
    # Hero tablosundan ilk kaydı çekiyoruz
    hero_data = Hero.query.first() 
    # Veriyi şablona gönderiyoruz
    return render_template('index.html', hero=hero_data)

@main.route("/about")
def about():
    # About tablosundan ilk kaydı çekiyoruz.
    about_data = About.query.first()
    
    # Çektiğimiz veriyi 'about_info' adıyla şablona gönderiyoruz.
    return render_template("about.html", about_info=about_data)

@main.route("/projects")
def projects():
    # Projects tablosundaki tüm kayıtları çekiyoruz.
    all_projects = Projects.query.all()
    
    # Proje listesini 'project_list' adıyla şablona gönderiyoruz.
    return render_template("projects.html", project_list=all_projects)

@main.route("/blogs")
def blogs():
    # Blogs tablosundaki tüm kayıtları, yayınlanma tarihine göre azalan şekilde (en yeni en üstte) sıralayarak çekiyoruz.
    all_posts = Blogs.query.order_by(Blogs.published_date.desc()).all()
    
    # Çektiğimiz yazı listesini 'blog_list' adıyla şablona gönderiyoruz.
    return render_template("blogs.html", blog_list=all_posts)

@main.route("/skills")
def skills():
    # Skills tablosundaki tüm yetenekleri çekiyoruz.
    all_skills = Skills.query.all()
    
    # Yetenek listesini 'skill_list' adıyla şablona gönderiyoruz.
    return render_template("skills.html", skill_list=all_skills)

@main.route("/experiences")
def experiences():
    # Experiences tablosundaki tüm kayıtları başlangıç tarihine göre azalan şekilde (en yeni en üstte) sıralayarak çekiyoruz.
    all_experiences = Experiences.query.order_by(Experiences.start_date.desc()).all()
    
    # Deneyim listesini 'experience_list' adıyla şablona gönderiyoruz.
    return render_template("experiences.html", experience_list=all_experiences)


@main.route("/references")
def references():
    # Reference tablosundaki tüm kayıtları çekiyoruz.
    all_references = Reference.query.all()
    
    # Referans listesini 'reference_list' adıyla şablona gönderiyoruz.
    return render_template("references.html", reference_list=all_references)


# app/routes.py

# ...diğer importlarınızın en üstüne formumuzu ve YENİ modelimizi ekleyin
from app.forms import ContactForm 
from app.models import ContactMessage # <-- BU SATIRI EKLEYİN

# ...diğer route'larınız...

@main.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Form gönderildiğinde ve geçerli olduğunda bu blok çalışır
        
        # YENİ KOD: Gelen veriyi bir model nesnesine aktar
        new_message = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        
        # YENİ KOD: Veritabanına ekle ve kaydet
        db.session.add(new_message)
        db.session.commit()
        
        # Eski print() satırını silebilirsiniz.
        
        flash('Mesajınız gönderildi.', 'success')
        return redirect(url_for('main.contact'))
        
    # Sayfa ilk yüklendiğinde (GET request) veya form geçersizse bu blok çalışır
    return render_template("contact.html", form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Kayıt başarılı!', 'success')
        return redirect(url_for('main.index'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('Giriş başarılı!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Hatalı e-posta veya şifre!', 'danger')
    elif request.method == 'POST':
        flash(f'Form doğrulanamadı: {form.errors}', 'warning')
    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Başarıyla çıkış yapıldı.', 'success')
    return redirect(url_for('main.index'))