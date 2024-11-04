from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import DepartmentModel  # Assume this model exists
from schemas import DepartmentSchema, DepartmentUpdateSchema  # Assume these schemas exist

blp = Blueprint("Departments", __name__, description="Operations on departments")

@blp.route("/department/<int:department_id>")
class Department(MethodView):
    @blp.response(200, DepartmentSchema)
    def get(self, department_id):
        """
        Retrieve a specific department by ID.
        """
        department = DepartmentModel.query.get_or_404(department_id)
        return department

    def delete(self, department_id):
        """
        Delete a specific department by ID.
        """
        department = DepartmentModel.query.get_or_404(department_id)
        db.session.delete(department)
        db.session.commit()
        return {"message": "Department deleted."}

    @blp.arguments(DepartmentUpdateSchema)
    @blp.response(200, DepartmentSchema)
    def put(self, department_data, department_id):
        """
        Update a specific department by ID. If the department doesn't exist,
        it will create a new department with the given ID.
        """
        department = DepartmentModel.query.get(department_id)

        if department:
            department.name = department_data["name"]
            department.head = department_data["head"]
        else:
            department = DepartmentModel(id=department_id, **department_data)

        db.session.add(department)
        db.session.commit()
        return department


@blp.route("/department")
class DepartmentList(MethodView):
    @blp.response(200, DepartmentSchema(many=True))
    def get(self):
        """
        Retrieve all departments.
        """
        return DepartmentModel.query.all()

    @blp.arguments(DepartmentSchema)
    @blp.response(201, DepartmentSchema)
    def post(self, department_data):
        """
        Create a new department.
        """
        department = DepartmentModel(**department_data)

        try:
            db.session.add(department)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the department.")

        return department
