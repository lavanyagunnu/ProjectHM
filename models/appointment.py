from db import db

class AppointmentModel(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    patient = db.relationship("PatientModel", back_populates="appointments")
    doctor = db.relationship("DoctorModel", back_populates="appointments")
