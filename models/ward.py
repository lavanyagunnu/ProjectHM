from db import db

class WardModel(db.Model):
    __tablename__ = "wards"

    id = db.Column(db.Integer, primary_key=True)
    ward_name = db.Column(db.String(80), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    current_occupancy = db.Column(db.Integer, default=0)

    rooms = db.relationship("RoomModel", back_populates="ward")
