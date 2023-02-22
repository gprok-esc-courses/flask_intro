from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///alchemy.sqlite3")

con = engine.connect()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

class Car(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    brand = Column(String)


Base.metadata.create_all(engine)

# Insert values
# username = input("Username: ")
# password = input("Password: ")

Session = sessionmaker(bind=engine)
session = Session()

# user = User(username=username, password=password)
# session.add(user)

result = session.query(User).all()

for row in result:
    print(row.id, row.username)

session.commit()


