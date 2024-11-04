from db import db

class PatientModel(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    # Relationship to appointments
    appointments = db.relationship("AppointmentModel", back_populates="patient")

    # Relationship to prescriptions
    prescriptions = db.relationship("PrescriptionModel", back_populates="patient")

    # Relationship to billing
    billing_records = db.relationship("BillingModel", back_populates="patient")
