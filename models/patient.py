from db import db

class PatientModel(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    medical_history = db.Column(db.Text)

    appointments = db.relationship("AppointmentModel", back_populates="patient")
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"))
    room = db.relationship("RoomModel", back_populates="patient")
