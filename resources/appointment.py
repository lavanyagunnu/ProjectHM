from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import AppointmentModel  # Assume this model exists
from schemas import AppointmentSchema, AppointmentUpdateSchema  # Assume these schemas exist

blp = Blueprint("Appointments", __name__, description="Operations on appointments")

@blp.route("/appointment/<int:appointment_id>")
class Appointment(MethodView):
    @blp.response(200, AppointmentSchema)
    def get(self, appointment_id):
        """
        Retrieve a specific appointment by ID.
        """
        appointment = AppointmentModel.query.get_or_404(appointment_id)
        return appointment

    def delete(self, appointment_id):
        """
        Delete a specific appointment by ID.
        """
        appointment = AppointmentModel.query.get_or_404(appointment_id)
        db.session.delete(appointment)
        db.session.commit()
        return {"message": "Appointment deleted."}

    @blp.arguments(AppointmentUpdateSchema)
    @blp.response(200, AppointmentSchema)
    def put(self, appointment_data, appointment_id):
        """
        Update a specific appointment by ID. If the appointment doesn't exist,
        it will create a new appointment with the given ID.
        """
        appointment = AppointmentModel.query.get(appointment_id)

        if appointment:
            appointment.patient_id = appointment_data["patient_id"]
            appointment.doctor_id = appointment_data["doctor_id"]
            appointment.date = appointment_data["date"]
            appointment.time = appointment_data["time"]
        else:
            appointment = AppointmentModel(id=appointment_id, **appointment_data)

        db.session.add(appointment)
        db.session.commit()
        return appointment


@blp.route("/appointment")
class AppointmentList(MethodView):
    @blp.response(200, AppointmentSchema(many=True))
    def get(self):
        """
        Retrieve all appointments.
        """
        return AppointmentModel.query.all()

    @blp.arguments(AppointmentSchema)
    @blp.response(201, AppointmentSchema)
    def post(self, appointment_data):
        """
        Create a new appointment.
        """
        appointment = AppointmentModel(**appointment_data)

        try:
            db.session.add(appointment)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the appointment.")

        return appointment
