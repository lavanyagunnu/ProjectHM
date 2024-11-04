from db import db

class PrescriptionModel(db.Model):
    __tablename__ = "prescriptions"

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.id"), nullable=False)
    medicine_details = db.Column(db.Text, nullable=False)
    dosage_details = db.Column(db.String(100), nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)

    appointment = db.relationship("AppointmentModel", back_populates="prescription")
