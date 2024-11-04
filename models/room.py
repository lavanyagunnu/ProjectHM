from db import db

class RoomModel(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    ward_id = db.Column(db.Integer, db.ForeignKey("wards.id"))
    bed_number = db.Column(db.String(10), nullable=False)
    room_status = db.Column(db.String(20), nullable=False)

    ward = db.relationship("WardModel", back_populates="rooms")
    patient = db.relationship("PatientModel", back_populates="room", uselist=False)
