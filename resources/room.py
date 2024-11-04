from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import RoomModel
from schemas import RoomSchema

blp = Blueprint("Rooms", __name__, description="Operations on rooms")


@blp.route("/room/<int:room_id>")
class Room(MethodView):
    @blp.response(200, RoomSchema)
    def get(self, room_id):
        """Get a room by ID."""
        room = RoomModel.query.get_or_404(room_id)
        return room

    def delete(self, room_id):
        """Delete a room."""
        room = RoomModel.query.get_or_404(room_id)
        db.session.delete(room)
        db.session.commit()
        return {"message": "Room deleted."}

    @blp.arguments(RoomSchema)
    @blp.response(200, RoomSchema)
    def put(self, room_data, room_id):
        """Update a room."""
        room = RoomModel.query.get(room_id)

        if room:
            room.ward_id = room_data["ward_id"]
            room.patient_id = room_data["patient_id"]
            room.bed_number = room_data["bed_number"]
            room.room_status = room_data["room_status"]
        else:
            room = RoomModel(id=room_id, **room_data)

        db.session.add(room)
        db.session.commit()
        return room


@blp.route("/room")
class RoomList(MethodView):
    @blp.response(200, RoomSchema(many=True))
    def get(self):
        """Get all rooms."""
        return RoomModel.query.all()

    @blp.arguments(RoomSchema)
    @blp.response(201, RoomSchema)
    def post(self, room_data):
        """Create a new room."""
        room = RoomModel(**room_data)

        try:
            db.session.add(room)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the room.")

        return room
