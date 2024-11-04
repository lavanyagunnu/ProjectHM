from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import WardModel  # Assume this model exists
from schemas import WardSchema  # Assume this schema exists

blp = Blueprint("Wards", __name__, description="Operations on wards")

@blp.route("/ward/<int:ward_id>")
class Ward(MethodView):
    @blp.response(200, WardSchema)
    def get(self, ward_id):
        ward = WardModel.query.get_or_404(ward_id)
        return ward

    def delete(self, ward_id):
        ward = WardModel.query.get_or_404(ward_id)
        db.session.delete(ward)
        db.session.commit()
        return {"message": "Ward deleted."}


@blp.route("/ward")
class WardList(MethodView):
    @blp.response(200, WardSchema(many=True))
    def get(self):
        return WardModel.query.all()

    @blp.arguments(WardSchema)
    @blp.response(201, WardSchema)
    def post(self, ward_data):
        ward = WardModel(**ward_data)

        try:
            db.session.add(ward)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the ward.")

        return ward
