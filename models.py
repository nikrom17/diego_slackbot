from sqlalchemy import Column, String, Integer, ARRAY, create_engine, ForeignKey
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
    initializeDb()
    # db_drop_and_create_all()

'''
people

'''


class Employee(db.Model):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True)
    slack_id = Column(String)
    name = Column(String)
    avatar = Column(String)
    title = Column(String)
    out_of_office = relationship("OutOfOffice")

    def __init__(self, slack_id, name, avatar, title):
        self.slack_id = slack_id,
        self.name = name,
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
            'slack_id': self.slack_id,
            'name': self.name,
            'avatar': self.avatar,
            'title': self.title,
        }

class OutOfOffice(db.Model):
    __tablename__ = 'outofoffice'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.id'))
    start = Column(Date)
    end = Column(Date)
    duration = Column(Integer)
    reason = Column(String)

    def __init__(self, employee_id, start, end, duration, reason="PTO"):
        self.employee_id = employee_id,
        self.start = start
        self.end = end
        self.duration = duration
        self.reason = reason

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
            'employee_id': self.employee_id,
            'start': self.start,
            'end': self.end,
            'duration': self.duration,
            'reason': self.reason,
        }
    
class RickyBobby(db.Model):
    __tablename__ = 'ricky_bobby'

    id = Column(Integer, primary_key=True)
    order = Column("data", ARRAY(Integer))
    current = Column(Integer)
    previous = Column(Integer)
    current_override = Column(Integer)

    def __init__(self, order, current, previous, current_override):
        self.order = order
        self.current = current
        self.previous = previous
        self.current_override = current_override

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
            'order': self.order,
            'current': self.current,
            'previous': self.previous,
            'current_override': self.current,
        }
        
# ---------------------------------------------------------------------------- #
# Initialize Database
# ---------------------------------------------------------------------------- #

def addEmployeeData():
    for data in employee_default_data:
        employee = Employee(
            data["name"],
            data["avatar"],
            data["title"],
        )
        employee.insert()

def addOutOfOfficeData():
    for data in ooo_default_data:
        employee = OutOfOffice(
            data["employee_id"],
            data["start"],
            data["end"],
            data["duration"],
            data["reason"],
        )
        employee.insert()
        
def addRickyBobbyData():
    for data in rickyBobby_default_data:
        employee = RickyBobby(
            data["order"],
            data["current"],
            data["previous"],
            data["current_override"],
        )
        employee.insert()

def initializeDb():
    print('****** Initializing DB ******')
    # addEmployeeData()
    addOutOfOfficeData()
    addRickyBobbyData()
   

# ---------------------------------------------------------------------------- #
# Initial App Data
# ---------------------------------------------------------------------------- #

employee_default_data = [
    {
        "name": "Nik Roman",
        "avatar": "https://ca.slack-edge.com/T02MFSUNZ-U018Z7BA4R0-e74d75d65f24-512",
        "title": "React Engineer",
    },
    {
        "name": "Camille Douglass",
        "avatar": "https://ca.slack-edge.com/T02MFSUNZ-U02PHNLBU-4b6ae73e1653-512",
        "title": "React Engineer",
    },
    {
        "name": "Bryant Miano",
        "avatar": "https://ca.slack-edge.com/T02MFSUNZ-UHS120E8M-ac1f2511cef3-512",
        "title": "Technology Manager",
    },
        {
        "name": "Rob Probst",
        "avatar": "https://ca.slack-edge.com/T02MFSUNZ-U8N13GWJJ-e15a9d26f56c-512",
        "title": "UI Software Tester",
    },
]

ooo_default_data = [
    {
        "employee_id": 10,
        "start": "2020-11-28",
        "end": "2020-11-29",
        "duration": 1,
        "reason": "PTO",
    },
    {
        "employee_id": 10,
        "start": "2020-12-7",
        "end": "2020-12-10",
        "duration": 3,
        "reason": "PTO",
    },
    {
        "employee_id": 9,
        "start": "2020-11-28",
        "end": "2020-11-29",
        "duration": 1,
        "reason": "PTO",
    },
    {
        "employee_id": 7,
        "start": "2020-11-28",
        "end": "2020-11-29",
        "duration": 1,
        "reason": "PTO",
    },
]

rickyBobby_default_data = [
    {
        "order": [7, 10, 9, 6],
        "current": 10,
        "previous": 7,
        "current_override": 0,
    },
]