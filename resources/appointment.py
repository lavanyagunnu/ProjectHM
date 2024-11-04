from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import AppointmentModel
from schemas import AppointmentSchema

blp = Blueprint("Appointments", __name__, description="Operations on appointments")


@blp.route("/appointment/<int:appointment_id>")
class Appointment(MethodView):
    @blp.response(200, AppointmentSchema)
    def get(self, appointment_id):
        """Get an appointment by ID."""
        appointment = AppointmentModel.query.get_or_404(appointment_id)
        return appointment

    def delete(self, appointment_id):
        """Delete an appointment."""
        appointment = AppointmentModel.query.get_or_404(appointment_id)
        db.session.delete(appointment)
        db.session.commit()
        return {"message": "Appointment deleted."}

