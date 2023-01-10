from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

conn_string = "postgresql://postgres:Atkinsons8*@localhost/Example_home_DSP"

engine=create_engine("postgresql://postgres:Atkinsons8*@localhost/Example_home_DSP",
    echo=True
)

Base=declarative_base()

SessionLocal = sessionmaker(bind=engine)