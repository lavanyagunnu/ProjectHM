from db import db

class EmployeeModel(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))

    department = db.relationship("DepartmentModel", back_populates="employees")
