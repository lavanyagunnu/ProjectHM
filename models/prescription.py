from db import db

class PrescriptionModel(db.Model):
    __tablename__ = "prescriptions"

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.id"))
    medicine_details = db.Column(db.Text, nullable=False)
    dosage_details = db.Column(db.Text, nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)

    appointment = db.relationship("AppointmentModel", back_populates="prescription")
