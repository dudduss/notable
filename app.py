# app.py
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask.json import jsonify

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schools.sqlite3'
db = SQLAlchemy(app)

db.Model.metadata.reflect(db.engine)

class Physician(db.Model):
    __tablename__ = 'physician'
    __table_args__ = { 'extend_existing': True }
    id = db.Column(db.VARCHAR, primary_key=True)   

class Patient(db.Model):
    __tablename__ = 'patient'
    __table_args__ = { 'extend_existing': True }
    id = db.Column(db.VARCHAR, primary_key=True)   

class Appointment(db.Model):
    __tablename__ = 'appointment'
    __table_args__ = { 'extend_existing': True }
    id = db.Column(db.VARCHAR, primary_key=True)  

class CompleteAppointment(object):
    name = ""
    time = ""
    kind = ""

    def __init__(self, name, time, kind):
        self.name = name
        self.time = time
        self.kind = kind

@app.route("/")
def index():
    school_count = School.query.count()
    zip_schools = School.query.filter_by(ZIP='10466').all()
    return render_template("appointments.html")

@app.route('/physicians')
def physicians():
    physicians = Physician.query.all()
    selected_physician = physicians[0].id
    appointments = Appointment.query.filter_by(physicianId=selected_physician).all()
    complete_appointments = []
    print(appointments)
    for appointment in appointments:
        patient = Patient.query.filter_by(id=appointment.patientId).first()
        complete_appointment = CompleteAppointment(patient.firstName + ' ' + patient.lastName, appointment.time, appointment.type )
        complete_appointments.append(complete_appointment)
    return render_template("appointments.html", physicians=physicians, selectedPhysician=physicians[0], appointments=complete_appointments)

@app.route('/appointments/<physicianId>')
def appointments(physicianId):
    physicians = Physician.query.all()
    physician = Physician.query.filter_by(id=physicianId).first()
    appointments = Appointment.query.filter_by(physicianId=physicianId).all()
    complete_appointments = []
    for appointment in appointments:
        patient = Patient.query.filter_by(id=appointment.patientId).first()
        complete_appointment = CompleteAppointment(patient.firstName + ' ' + patient.lastName, appointment.time, appointment.type )
        complete_appointments.append(complete_appointment)
    return render_template("appointments.html", physicians=physicians, selectedPhysician=physician, appointments=complete_appointments)

if __name__ == '__main__':
    app.run(debug=True)