from sqlalchemy import Column, Integer, Unicode, UnicodeText, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from os import path
from datetime import datetime

db_file = path.join(path.dirname(path.abspath(__file__)), "biking.db")
db_file = "sqlite:///" + db_file

engine = create_engine(db_file, echo=True)
Base = declarative_base(bind=engine)

class Incident(Base):
    __tablename__ = 'incident'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    location = Column(Unicode)
    date = Column(DateTime)
    link = Column(Unicode)
    content = Column(Unicode)

    def __init__(self, title, location, link, date, content):
        self.title = title
        self.location = location
        self.link = link
        try:
            self.date = datetime.strptime(date, "%d.%m.%Y")
        except:
            self.date = datetime.now()
        self.content = content

    def __str__(self):
        content = ""
        content += "Bike incident:\n"
        content += " Title: '{}'\n".format(self.title)
        content += " Location: '{}'\n".format(self.location)
        content += " Date: '{}'\n".format(self.date)
        content += " Link: '{}'\n".format(self.link)
        content += " Content: [{}]\n".format(self.content)

        return content



Base.metadata.create_all()

Session = sessionmaker(bind=engine)
s = Session()
