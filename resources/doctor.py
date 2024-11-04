from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import DoctorModel  # Assume this model exists
from schemas import DoctorSchema, DoctorUpdateSchema  # Assume these schemas exist

blp = Blueprint("Doctors", __name__, description="Operations on doctors")

@blp.route("/doctor/<int:doctor_id>")
class Doctor(MethodView):
    @blp.response(200, DoctorSchema)
    def get(self, doctor_id):
        doctor = DoctorModel.query.get_or_404(doctor_id)
        return doctor

    def delete(self, doctor_id):
        doctor = DoctorModel.query.get_or_404(doctor_id)
        db.session.delete(doctor)
        db.session.commit()
        return {"message": "Doctor deleted."}

    @blp.arguments(DoctorUpdateSchema)
    @blp.response(200, DoctorSchema)
    def put(self, doctor_data, doctor_id):
        doctor = DoctorModel.query.get(doctor_id)

        if doctor:
            doctor.name = doctor_data["name"]
            doctor.specialization = doctor_data["specialization"]
            doctor.availability = doctor_data["availability"]
        else:
            doctor = DoctorModel(id=doctor_id, **doctor_data)

        db.session.add(doctor)
        db.session.commit()
        return doctor


@blp.route("/doctor")
class DoctorList(MethodView):
    @blp.response(200, DoctorSchema(many=True))
    def get(self):
        return DoctorModel.query.all()

    @blp.arguments(DoctorSchema)
    @blp.response(201, DoctorSchema)
    def post(self, doctor_data):
        doctor = DoctorModel(**doctor_data)

        try:
            db.session.add(doctor)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the doctor.")

        return doctor
