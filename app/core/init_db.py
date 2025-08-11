from app.core.database import engine, Base

# forțează încărcarea tuturor modelelor din proiect

# creează tabelele
Base.metadata.create_all(bind=engine)
