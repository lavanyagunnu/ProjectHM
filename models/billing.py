from db import db

class BillingModel(db.Model):
    __tablename__ = "billings"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    payment_status = db.Column(db.String(20), nullable=False)

    patient = db.relationship("PatientModel")
    doctor = db.relationship("DoctorModel")
