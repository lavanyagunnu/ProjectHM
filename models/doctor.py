from db import db

class DoctorModel(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    specialization = db.Column(db.String(80), nullable=False)
    availability = db.Column(db.String(80), nullable=True)

    appointments = db.relationship("AppointmentModel", back_populates="doctor")
