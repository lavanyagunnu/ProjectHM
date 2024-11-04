from flask import Flask
from flask_smorest import Api
from db import db

def create_app(db_url=None):
    app = Flask(__name__)
    app.config["API_TITLE"] = "Hospital Management API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True

    db.init_app(app)
    api = Api(app)

    with app.app_context():
        db.create_all()

    # Register blueprints for each resource
    from resources.patient import blp as PatientBlueprint
    from resources.doctor import blp as DoctorBlueprint
    from resources.room import blp as RoomBlueprint
    from resources.ward import blp as WardBlueprint
    from resources.appointment import blp as AppointmentBlueprint
    from resources.prescription import blp as PrescriptionBlueprint
    from resources.billing import blp as BillingBlueprint
    from resources.department import blp as DepartmentBlueprint
    from resources.employee import blp as EmployeeBlueprint

    api.register_blueprint(PatientBlueprint)
    api.register_blueprint(DoctorBlueprint)
    api.register_blueprint(RoomBlueprint)
    api.register_blueprint(WardBlueprint)
    api.register_blueprint(AppointmentBlueprint)
    api.register_blueprint(PrescriptionBlueprint)
    api.register_blueprint(BillingBlueprint)
    api.register_blueprint(DepartmentBlueprint)
    api.register_blueprint(EmployeeBlueprint)

    return app
