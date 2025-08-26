# run.py

# Gerekli olan sadece bu iki import
from app import create_app, db

# create_app fonksiyonu ile uygulama nesnesini oluştur
app = create_app()

# Bu blok, sadece 'python run.py' komutuyla çalıştırıldığında devreye girer
if __name__ == '__main__':
    # 'with app.app_context()' bloğu, veritabanı işlemlerinin
    # uygulama bağlamında yapılmasını sağlar.
    with app.app_context():
        # Veritabanı tabloları yoksa oluşturur
        db.create_all()  
    
    # Uygulamayı debug modunda çalıştır
    app.run(debug=True)