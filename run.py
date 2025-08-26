# run.py
from app import create_app, db
from flask import render_template
#from app import app  # veya create_app() sonrası app objesi
from app.models import Reference
app = create_app()

# Ana route’larımızı burada tanımlıyoruz
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/blogs")
def blogs():
    return render_template("blogs.html")

@app.route("/skills")
def skills():
    return render_template("skills.html")

@app.route("/experiences")
def experiences():
    return render_template("experiences.html")

@app.route("/references")
def references():
    return render_template("references.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tabloları oluştur
    app.run(debug=True)
