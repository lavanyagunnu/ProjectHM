from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import BillingModel  # Assume this model exists
from schemas import BillingSchema, BillingUpdateSchema  # Assume these schemas exist

blp = Blueprint("Billings", __name__, description="Operations on billings")

@blp.route("/billing/<int:billing_id>")
class Billing(MethodView):
    @blp.response(200, BillingSchema)
    def get(self, billing_id):
        billing = BillingModel.query.get_or_404(billing_id)
        return billing

    def delete(self, billing_id):
        billing = BillingModel.query.get_or_404(billing_id)
        db.session.delete(billing)
        db.session.commit()
        return {"message": "Billing record deleted."}

    @blp.arguments(BillingUpdateSchema)
    @blp.response(200, BillingSchema)
    def put(self, billing_data, billing_id):
        billing = BillingModel.query.get(billing_id)

        if billing:
            billing.amount = billing_data["amount"]
            billing.paid = billing_data["paid"]
            billing.patient_id = billing_data["patient_id"]
        else:
            billing = BillingModel(id=billing_id, **billing_data)

        db.session.add(billing)
        db.session.commit()
        return billing


@blp.route("/billing")
class BillingList(MethodView):
    @blp.response(200, BillingSchema(many=True))
    def get(self):
        return BillingModel.query.all()

    @blp.arguments(BillingSchema)
    @blp.response(201, BillingSchema)
    def post(self, billing_data):
        billing = BillingModel(**billing_data)

        try:
            db.session.add(billing)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the billing record.")

        return billing
