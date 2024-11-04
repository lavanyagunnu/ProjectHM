from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import PrescriptionModel  # Assume this model exists
from schemas import PrescriptionSchema, PrescriptionUpdateSchema  # Assume these schemas exist

blp = Blueprint("Prescriptions", __name__, description="Operations on prescriptions")

@blp.route("/prescription/<int:prescription_id>")
class Prescription(MethodView):
    @blp.response(200, PrescriptionSchema)
    def get(self, prescription_id):
        prescription = PrescriptionModel.query.get_or_404(prescription_id)
        return prescription

    def delete(self, prescription_id):
        prescription = PrescriptionModel.query.get_or_404(prescription_id)
        db.session.delete(prescription)
        db.session.commit()
        return {"message": "Prescription deleted."}

    @blp.arguments(PrescriptionUpdateSchema)
    @blp.response(200, PrescriptionSchema)
    def put(self, prescription_data, prescription_id):
        prescription = PrescriptionModel.query.get(prescription_id)

        if prescription:
            prescription.patient_id = prescription_data["patient_id"]
            prescription.medication = prescription_data["medication"]
            prescription.dosage = prescription_data["dosage"]
            prescription.instructions = prescription_data["instructions"]
        else:
            prescription = PrescriptionModel(id=prescription_id, **prescription_data)

        db.session.add(prescription)
        db.session.commit()
        return prescription


@blp.route("/prescription")
class PrescriptionList(MethodView):
    @blp.response(200, PrescriptionSchema(many=True))
    def get(self):
        return PrescriptionModel.query.all()

    @blp.arguments(PrescriptionSchema)
    @blp.response(201, PrescriptionSchema)
    def post(self, prescription_data):
        prescription = PrescriptionModel(**prescription_data)

        try:
            db.session.add(prescription)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the prescription.")

        return prescription
