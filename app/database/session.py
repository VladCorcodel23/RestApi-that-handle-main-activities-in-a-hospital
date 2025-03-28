import urllib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Conexiune SQL Server cu driver ODBC și trusted connection
params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=DESKTOP-R77CARD\\SQLEXPRESS;"
    "DATABASE=hospital_db;"
    "Trusted_Connection=yes;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
