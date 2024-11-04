from db import db

class DoctorModel(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)

    # Relationship to appointments
    appointments = db.relationship("AppointmentModel", back_populates="doctor")

    # Relationship to prescriptions
    prescriptions = db.relationship("PrescriptionModel", back_populates="doctor")

