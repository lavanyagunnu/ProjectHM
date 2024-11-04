from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import EmployeeModel
from schemas import EmployeeSchema

blp = Blueprint("Employees", __name__, description="Operations on employees")


@blp.route("/employee/<int:employee_id>")
class Employee(MethodView):
    @blp.response(200, EmployeeSchema)
    def get(self, employee_id):
        """Get an employee by ID."""
        employee = EmployeeModel.query.get_or_404(employee_id)
        return employee

    def delete(self, employee_id):
        """Delete an employee."""
        employee = EmployeeModel.query.get_or_404(employee_id)
        db.session.delete(employee)
        db.session.commit()
        return {"message": "Employee deleted."}

    @blp.arguments(EmployeeSchema)
    @blp.response(200, EmployeeSchema)
    def put(self, employee_data, employee_id):
        """Update an employee."""
        employee = EmployeeModel.query.get(employee_id)

        if employee:
            employee.name = employee_data["name"]
            employee.department_id = employee_data["department_id"]
            employee.role = employee_data["role"]
        else:
            employee = EmployeeModel(id=employee_id, **employee_data)

        db.session.add(employee)
        db.session.commit()
        return employee


@blp.route("/employee")
class EmployeeList(MethodView):
    @blp.response(200, EmployeeSchema(many=True))
    def get(self):
        """Get all employees."""
        return EmployeeModel.query.all()

    @blp.arguments(EmployeeSchema)
    @blp.response(201, EmployeeSchema)
    def post(self, employee_data):
        """Create a new employee."""
        employee = EmployeeModel(**employee_data)

        try:
            db.session.add(employee)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the employee.")

        return employee
