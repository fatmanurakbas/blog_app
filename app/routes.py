# app/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, session
from app import db 
from app.models import User, Hero, About, Projects, Blogs, Skills, Experiences, Reference, ContactMessage
from app.forms import RegistrationForm, LoginForm, ContactForm
from werkzeug.security import generate_password_hash, check_password_hash
main = Blueprint('main', __name__)


@main.route('/')
def index():

    hero_data = None
    about_data = None
    project_list = []


    try:
        # Veritabanından verileri çek ve değişkenlerin üzerine yaz
        hero_data = Hero.query.first()
        about_data = About.query.first()
        project_list = Projects.query.order_by(Projects.id.desc()).all()
        skill_list = Skills.query.all()
        experience_list = Experiences.query.order_by(Experiences.start_date.desc()).all()
        reference_list = Reference.query.all()
        blog_list = Blogs.query.order_by(Blogs.published_date.desc()).limit(3).all()

    except Exception as e:
        # Eğer sorguda hata olursa sadece bir uyarı göster. 
        # Değişkenler varsayılan boş değerlerinde kalacağı için sayfa çökmeyecek.
        flash(f"Veritabanından bilgi alınırken bir sorun oluştu: {e}", "danger")

    # Formu her zaman oluştur
    contact_form = ContactForm()

    # Tüm verileri (dolu veya boş) şablona gönder
    return render_template('index.html', 
                           hero=hero_data,
                           about_info=about_data,
                           project_list=project_list,
                           skill_list=skill_list,
                           experience_list=experience_list,
                           reference_list=reference_list,
                           blog_list=blog_list,
                           form=contact_form)

@main.route('/blog/<int:post_id>')
def blog_post(post_id):
    post = Blogs.query.get_or_404(post_id)
    return render_template('blog_detail.html', post=post)

# --- FORM İŞLEMLERİ İÇİN AYRI ROUTE'LAR ---

@main.route("/submit_contact", methods=['POST'])
def submit_contact():
    """
    Bu route SADECE iletişim formundan gelen POST isteğini işler.
    """
    form = ContactForm()
    if form.validate_on_submit():
        # Veriyi veritabanına kaydet
        new_message = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        db.session.add(new_message)
        db.session.commit()
        flash('Mesajınız başarıyla gönderildi. Teşekkürler!', 'success')
    else:
        # Form geçerli değilse, hataları flash mesajı olarak göster
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')

    # İşlem bittikten sonra kullanıcıyı anasayfanın iletişim bölümüne geri yönlendir
    return redirect(url_for('main.index') + '#iletisim')


# --- KULLANICI İŞLEMLERİ (AYNI KALABİLİR) ---

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Kayıt başarılı! Lütfen giriş yapın.', 'success')
        return redirect(url_for('main.login')) # Kayıttan sonra login'e yönlendirmek daha mantıklı
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('Giriş başarılı!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Hatalı kullanıcı adı veya şifre!', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Başarıyla çıkış yapıldı.', 'success')
    return redirect(url_for('main.index'))