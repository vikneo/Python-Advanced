import json
from pprint import pprint

from flask import make_response, jsonify, Flask, request, url_for

from config.hotel_base import object_db

app = Flask(__name__)


@app.route('/room', methods = ['GET'])
def get_room():
    try:
        rooms = object_db.all()
        data = [
            {'roomId': room[0], 'floor': room[1], 'guestNum': room[3], 'beds': room[2], 'price': room[4]}
            for room in rooms
        ]
        return jsonify({'rooms': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/room/<int:room_id>', methods = ['GET', "POST"])
def room_detail(room_id):
    try:
        room = object_db.filter(room_id = room_id)[0]
        if room is None:
            return jsonify({'error': 'Room not found'}), 409
        if request.method == 'GET':
            response = make_response(
                jsonify(
                    susses = True,
                    bookedRoom = {'floor': room[1], 'beds': room[2], 'questNum': room[3], 'price': room[4]},
                    booking=room[5],
                    description = "Здесь доступно описание о комнате. Доступна для бронирования"
                ), 200
            )
            return response
        elif request.method == 'POST':
            object_db.update(booking = False, room_id = room_id)
            response = make_response(
                jsonify(
                    susses = True,
                    bookedRoom = {'floor': room[1], 'beds': room[2], 'questNum': room[3], 'price': room[4]},
                    booking = room[5],
                    description = f"Room `ID-{room_id}` has been booking"
                ), 201
            )
            return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/add-room', methods = ['POST'])
def add_room():
    data = request.json
    try:
        object_db.create(data)
        return jsonify(success = True), 200
    except Exception as e:
        pprint(data)
        return jsonify({'error': str(e)}), 500


@app.route('/booking', methods = ['GET'])
def booking():
    try:
        rooms_for_booking = object_db.all(booking = True)
        data = [
            {'roomId': room[0],
             'floor': room[1],
             'questNum': room[3],
             'beds': room[2],
             'price': room[4],
             'booking': {
                 'booked': url_for('booking_detail', room_id = room[0]),
             }}
            for room in rooms_for_booking
        ]
        return jsonify({'rooms': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/booking/<int:room_id>', methods = ['GET', 'POST'])
def booking_detail(room_id):
    try:
        room = object_db.get(room_id)
        if room is None:
            return jsonify({'error': 'Room not found'}), 409
        if request.method == 'GET':
            response = make_response(
                jsonify(
                    susses = True,
                    bookedRoom = {'floor': room[1], 'beds': room[2], 'questNum': room[3], 'price': room[4]},
                    booking={'booked': 'The room is available' if room[5] else 'The room is booked'},
                ), 200
            )
            return response
        if request.method == 'POST':
            object_db.update(booking = False, room_id = room_id)
            response = make_response(
                jsonify(
                    success = True,
                    bookedRoom = {
                        'floor': room[1],
                        'beds': room[2],
                        'questNum': room[3],
                        'price': room[4],
                    },
                    description = f"Room `ID-{room_id}` has been booking"
                ), 200)
            return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/del-booking/<int:room_id>', methods = ['POST'])
def del_booking(room_id):
    try:
        room = object_db.get(room_id)
        if room is None:
            return jsonify({'error': 'Room not found'}), 409
        object_db.update(booking = True, room_id = room_id)
        response = make_response(
            jsonify(
                susses = True,
                bookedRoom = {'floor': room[1], 'beds': room[2], 'questNum': room[3], 'price': room[4]},
                booking = {'booked': 'The room is available' if room[5] else 'The room is booked'},
            ), 200
        )
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug = True)
