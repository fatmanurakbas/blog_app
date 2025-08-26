#config.py
import os
import urllib

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bu-bir-gizli-anahtar'

    # ODBC bağlantı stringi
    params = urllib.parse.quote_plus(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=FATMANUR\\SQLEXPRESS;"
        "DATABASE=BlogDB;"
        "Trusted_Connection=yes;"
        "Encrypt=no;"
        "TrustServerCertificate=yes;"
    )

    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
    SQLALCHEMY_TRACK_MODIFICATIONS = False
