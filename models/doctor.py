from db import db

class DoctorModel(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    specialization = db.Column(db.String(80), nullable=False)
    availability = db.Column(db.String(50))

    appointments = db.relationship("AppointmentModel", back_populates="doctor")
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    department = db.relationship("DepartmentModel", back_populates="doctors")
