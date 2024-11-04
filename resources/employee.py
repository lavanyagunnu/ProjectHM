from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import EmployeeModel  # Assume this model exists
from schemas import EmployeeSchema, EmployeeUpdateSchema  # Assume these schemas exist

blp = Blueprint("Employees", __name__, description="Operations on employees")

@blp.route("/employee/<int:employee_id>")
class Employee(MethodView):
    @blp.response(200, EmployeeSchema)
    def get(self, employee_id):
        """
        Retrieve a specific employee by ID.
        """
        employee = EmployeeModel.query.get_or_404(employee_id)
        return employee

    def delete(self, employee_id):
        """
        Delete a specific employee by ID.
        """
        employee = EmployeeModel.query.get_or_404(employee_id)
        db.session.delete(employee)
        db.session.commit()
        return {"message": "Employee deleted."}

    @blp.arguments(EmployeeUpdateSchema)
    @blp.response(200, EmployeeSchema)
    def put(self, employee_data, employee_id):
        """
        Update a specific employee by ID. If the employee doesn't exist,
        it will create a new employee with the given ID.
        """
        employee = EmployeeModel.query.get(employee_id)

        if employee:
            employee.name = employee_data["name"]
            employee.role = employee_data["role"]
            employee.salary = employee_data["salary"]
            employee.department_id = employee_data.get("department_id", employee.department_id)
        else:
            employee = EmployeeModel(id=employee_id, **employee_data)

        db.session.add(employee)
        db.session.commit()
        return employee


@blp.route("/employee")
class EmployeeList(MethodView):
    @blp.response(200, EmployeeSchema(many=True))
    def get(self):
        """
        Retrieve all employees.
        """
        return EmployeeModel.query.all()

    @blp.arguments(EmployeeSchema)
    @blp.response(201, EmployeeSchema)
    def post(self, employee_data):
        """
        Create a new employee.
        """
        employee = EmployeeModel(**employee_data)

        try:
            db.session.add(employee)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the employee.")

        return employee
