from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()
engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String)

Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(bind=engine)

# 启动时插几条假数据（如果表是空的）
with SessionLocal() as db:
    if db.query(Item).count() == 0:
        db.add_all([Item(name="item-one"), Item(name="item-two")])
        db.commit()

@app.get("/items")
def get_items():
    db = SessionLocal()
    items = db.query(Item).all()
    db.close()
    return [{"id": i.id, "name": i.name} for i in items]