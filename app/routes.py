from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app.forms import RegistrationForm, LoginForm
from app.models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Şifreyi hash'le
        hashed_password = generate_password_hash(form.password.data)
        
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
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
        if user:
            # Şifre kontrolü
            if check_password_hash(user.password, form.password.data):
                session['user_id'] = user.id
                flash('Giriş başarılı!', 'success')
                return redirect(url_for('main.index'))
            else:
                flash('Hatalı e-posta veya şifre!', 'danger')
        else:
            flash('Hatalı e-posta veya şifre!', 'danger')
    # Formun neden doğrulanmadığını görmek için
    elif request.method == 'POST':
        flash(f'Form doğrulanamadı: {form.errors}', 'warning')
        
    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Başarıyla çıkış yapıldı.', 'success')
    return redirect(url_for('main.index'))

@main.route('/')
def index():
    return render_template('index.html')
