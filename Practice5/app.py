from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine("sqlite:///flask_db.db", echo=False)

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contact"
    id = Column(Integer, primary_key=True)
    fname = Column(String)
    email = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)


@app.route("/contact")
def contact_us():
    show_form = False
    fname = ""
    if len(request.args) == 0:
        show_form = True

    else:
        fname = request.args["fname"]
        email = request.args["email"]
        description = request.args["description"]

        session.add(Contact(fname=fname, email=email, description=description))
        session.commit()

    return render_template("contact.html", show_form=show_form, fname=fname)


@app.route('/list')
def list():
    contacts = session.query(Contact).all()
    return render_template('list.html', contacts=contacts)


if __name__ == '__main__':
    app.run()
