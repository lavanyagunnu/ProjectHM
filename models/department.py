from db import db

class DepartmentModel(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    head_of_department = db.Column(db.String(80), nullable=False)

    doctors = db.relationship("DoctorModel", back_populates="department")
