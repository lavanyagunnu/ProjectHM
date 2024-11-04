from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import PatientModel
from schemas import PatientSchema

blp = Blueprint("Patients", __name__, description="Operations on patients")


@blp.route("/patient/<int:patient_id>")
class Patient(MethodView):
    @blp.response(200, PatientSchema)
    def get(self, patient_id):
        """Get a patient by ID."""
        patient = PatientModel.query.get_or_404(patient_id)
        return patient

    def delete(self, patient_id):
        """Delete a patient."""
        patient = PatientModel.query.get_or_404(patient_id)
        db.session.delete(patient)
        db.session.commit()
        return {"message": "Patient deleted."}

    @blp.arguments(PatientSchema)
    @blp.response(200, PatientSchema)
    def put(self, patient_data, patient_id):
        """Update a patient."""
        patient = PatientModel.query.get(patient_id)

        if patient:
            patient.name = patient_data["name"]
            patient.age = patient_data["age"]
            patient.gender = patient_data["gender"]
            patient.medical_history = patient_data["medical_history"]
        else:
            patient = PatientModel(id=patient_id, **patient_data)

        db.session.add(patient)
        db.session.commit()
        return patient


@blp.route("/patient")
class PatientList(MethodView):
    @blp.response(200, PatientSchema(many=True))
    def get(self):
        """Get all patients."""
        return PatientModel.query.all()

    @blp.arguments(PatientSchema)
    @blp.response(201, PatientSchema)
    def post(self, patient_data):
        """Create a new patient."""
        patient = PatientModel(**patient_data)

        try:
            db.session.add(patient)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the patient.")

        return patient
