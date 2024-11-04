from db import db

class BillingModel(db.Model):
    __tablename__ = "billings"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"))
    total_amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    payment_status = db.Column(db.String(20), nullable=False)

    patient = db.relationship("PatientModel", back_populates="billing")
    doctor = db.relationship("DoctorModel", back_populates="billing")
