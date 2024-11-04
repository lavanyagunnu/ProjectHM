from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import WardModel
from schemas import WardSchema

blp = Blueprint("Wards", __name__, description="Operations on wards")


@blp.route("/ward/<int:ward_id>")
class Ward(MethodView):
    @blp.response(200, WardSchema)
    def get(self, ward_id):
        """Get a ward by ID."""
        ward = WardModel.query.get_or_404(ward_id)
        return ward

    def delete(self, ward_id):
        """Delete a ward."""
        ward = WardModel.query.get_or_404(ward_id)
        db.session.delete(ward)
        db.session.commit()
        return {"message": "Ward deleted."}

    @blp.arguments(WardSchema)
    @blp.response(200, WardSchema)
    def put(self, ward_data, ward_id):
        """Update a ward."""
        ward = WardModel.query.get(ward_id)

        if ward:
            ward.name = ward_data["name"]
            ward.capacity = ward_data["capacity"]
            ward.current_occupancy = ward_data["current_occupancy"]
        else:
            ward = WardModel(id=ward_id, **ward_data)

        db.session.add(ward)
        db.session.commit()
        return ward


@blp.route("/ward")
class WardList(MethodView):
    @blp.response(200, WardSchema(many=True))
    def get(self):
        """Get all wards."""
        return WardModel.query.all()

    @blp.arguments(WardSchema)
    @blp.response(201, WardSchema)
    def post(self, ward_data):
        """Create a new ward."""
        ward = WardModel(**ward_data)

        try:
            db.session.add(ward)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the ward.")

        return ward
