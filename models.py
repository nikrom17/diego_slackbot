from sqlalchemy import Column, String, Integer, DateTime, Boolean, create_engine, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.sqltypes import Date

database_name = "diego"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    initializeDb()

def setup_db(flask_app):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = flask_app
    db.init_app(flask_app)
    db.create_all()
    db_drop_and_create_all()

'''
people

'''


class Employee(db.Model):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    birthday = Column(Date)
    avatar = Column(String)
    title = Column(String)

    def __init__(self, name, birthday, avatar, title):
        self.name = name,
        self.birthday = birthday
        self.avatar = avatar
        self.title = title

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'birthday': self.birthday,
            'avatar': self.avatar,
            'title': self.title,
            
        }
        
# ---------------------------------------------------------------------------- #
# Initialize Database
# ---------------------------------------------------------------------------- #

def addEmployeeData():
    for data in employee_default_data:
        employee = Employee(
            data["name"],
            data["birthday"],
            data["avatar"],
            data["title"],
        )
        employee.insert()

def initializeDb():
    print('****** Initializing DB ******')
    addEmployeeData()
   

# ---------------------------------------------------------------------------- #
# Initial App Data
# ---------------------------------------------------------------------------- #

employee_default_data = [
    {
        "name": "Nik Roman",
        "birthday": "1991-10-17",
        "avatar": "https://ca.slack-edge.com/T02MFSUNZ-U018Z7BA4R0-e74d75d65f24-512",
        "title": "React Engineer",
    },
    {
        "name": "Camille Douglass",
        "birthday": "1991-10-17",
        "avatar": "https://ca.slack-edge.com/T02MFSUNZ-U02PHNLBU-4b6ae73e1653-512",
        "title": "React Engineer",
    },
    {
        "name": "Bryant Miano",
        "birthday": "1991-10-17",
        "avatar": "https://ca.slack-edge.com/T02MFSUNZ-UHS120E8M-ac1f2511cef3-512",
        "title": "Technology Manager",
    },
        {
        "name": "Rob Probst",
        "birthday": "1991-10-17",
        "avatar": "https://ca.slack-edge.com/T02MFSUNZ-U8N13GWJJ-e15a9d26f56c-512",
        "title": "UI Software Tester",
    },
]