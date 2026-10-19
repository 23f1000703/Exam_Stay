from flask import jsonify, make_response, request
from flask_security import auth_required, current_user
from datetime import datetime

from controllers.database import db
from controllers.model import Customer, ExamTrip, Booking, Property, Room, Amenity
from flask_restful import Resource
from datetime import date


class StudentDashboardApi(Resource):

    @auth_required()
    def get(self):
        # Logged-in user ka student profile
        customer = Customer.query.filter_by(
            user_id=current_user.id
        ).first()

        if not customer:
            return make_response(
                jsonify({
                    'message': 'Student profile not found.'
                }),
                404
            )

        # Total exam trips
        total_trips = ExamTrip.query.filter_by(
            customer_id=customer.id
        ).count()

        # Total bookings (all statuses)
        total_bookings = Booking.query.filter_by(
            customer_id=customer.id
        ).count()

        # Upcoming or ongoing confirmed stays
        now = datetime.utcnow()

        upcoming_stays = Booking.query.filter(
            Booking.customer_id == customer.id,
            Booking.check_out >= now,
            db.func.lower(Booking.status) == 'confirmed'
        ).count()

        return make_response(
            jsonify({
                'message': 'Student dashboard fetched successfully.',
                'student': {
                    'id': customer.id,
                    'name': customer.name
                },
                'stats': {
                    'trips': total_trips,
                    'bookings': total_bookings,
                    'upcoming_stays': upcoming_stays
                }
            }),
            200
        )

class StudentPropertiesApi(Resource):

    @auth_required()
    def get(self):
        # Sirf logged-in student ko access
        if not current_user.has_role('customer'):
            return make_response(
                jsonify({'message': 'Student access required.'}),
                403
            )

        # Search filters
        search = request.args.get('search', '').strip()
        city = request.args.get('city', '').strip()

        # Sirf verified properties
        query = Property.query.filter(
            Property.verification_status == 'verified'
        )

        if search:
            query = query.filter(
                Property.name.ilike(f'%{search}%')
            )

        if city:
            query = query.filter(
                Property.city.ilike(f'%{city}%')
            )

        properties = query.order_by(
            Property.created_at.desc()
        ).all()

        result = []

        for prop in properties:
            # Available rooms
            available_rooms = Room.query.filter_by(
                property_id=prop.id,
                available=True
            ).all()

            # Property images
            images = [
                {
                    'id': image.id,
                    'image_url': image.image_url,
                    'is_primary': image.is_primary
                }
                for image in prop.images
            ]

            prices = [
                room.price_per_night
                for room in available_rooms
                if room.price_per_night is not None
            ]

            rooms_data = []

            for room in available_rooms:
                room_amenity_ids = room.amenities or []

                if not isinstance(room_amenity_ids, list):
                    room_amenity_ids = []

                room_amenities = Amenity.query.filter(
                    Amenity.id.in_(room_amenity_ids)
                ).all() if room_amenity_ids else []

                amenities_by_id = {
                    amenity.id: {
                        'id': amenity.id,
                        'name': amenity.name
                    }
                    for amenity in room_amenities
                }

                rooms_data.append({
                    'id': room.id,
                    'room_number': room.room_number,
                    'room_type': room.room_type,
                    'price_per_night': room.price_per_night,
                    'amenities': [
                        amenities_by_id[amenity_id]
                        for amenity_id in room_amenity_ids
                        if amenity_id in amenities_by_id
                    ]
                })

            result.append({
                'id': prop.id,
                'name': prop.name,
                'description': prop.description,
                'address': prop.address,
                'city': prop.city,
                'district': prop.district,
                'state': prop.state,
                'pincode': prop.pincode,
                'verification_status': prop.verification_status,
                'available_rooms': len(available_rooms),
                'starting_price': min(prices) if prices else None,
                'images': images,
                'rooms': rooms_data
            })

        return make_response(
            jsonify({
                'message': 'Verified properties fetched successfully.',
                'total_properties': len(result),
                'properties': result
            }),
            200
        )


class StudentBookingHistoryApi(Resource):

    @auth_required()
    def get(self):
        if not current_user.has_role('customer'):
            return make_response(
                jsonify({'message': 'Student access required.'}),
                403
            )

        customer = Customer.query.filter_by(
            user_id=current_user.id
        ).first()

        if not customer:
            return make_response(
                jsonify({'message': 'Student profile not found.'}),
                404
            )

        bookings = (
            Booking.query
            .filter_by(customer_id=customer.id)
            .order_by(Booking.created_at.desc())
            .all()
        )

        booking_history = []

        for booking in bookings:
            prop = booking.property
            room = booking.room

            booking_history.append({
                'id': booking.id,
                'property': {
                    'id': prop.id if prop else None,
                    'name': prop.name if prop else 'Property unavailable',
                    'address': prop.address if prop else '',
                    'city': prop.city if prop else ''
                },
                'room': {
                    'id': room.id if room else None,
                    'room_number': room.room_number if room else '',
                    'room_type': room.room_type if room else ''
                },
                'check_in': (
                    booking.check_in.isoformat()
                    if booking.check_in else None
                ),
                'check_out': (
                    booking.check_out.isoformat()
                    if booking.check_out else None
                ),
                'number_of_guests': booking.number_of_guests,
                'total_amount': booking.total_amount,
                'status': booking.status,
                'created_at': (
                    booking.created_at.isoformat()
                    if booking.created_at else None
                )
            })

        return make_response(
            jsonify({
                'message': 'Booking history fetched successfully.',
                'total_bookings': len(booking_history),
                'bookings': booking_history
            }),
            200
        )

class StudentProfileApi(Resource):

    def get_profile_data(self, customer):
        return {
            'id': customer.id,
            'name': customer.name,
            'dob': customer.dob.isoformat() if customer.dob else '',
            'gender': customer.gender or '',
            'mobile': customer.mobile or '',
            'alternate_mobile': customer.alternate_mobile or '',
            'id_type': customer.id_type or '',
            'id_number': customer.id_number or '',
            'cor_address': customer.cor_address or '',
            'cor_state': customer.cor_state or '',
            'cor_district': customer.cor_district or '',
            'cor_pincode': customer.cor_pincode or '',
            'per_address': customer.per_address or '',
            'per_state': customer.per_state or '',
            'per_district': customer.per_district or '',
            'per_pincode': customer.per_pincode or '',
            'student_id': customer.student_id or '',
            'college_name': customer.college_name or '',
            'course': customer.course or '',
            'profile_photo': customer.profile_photo or ''
        }


    @auth_required()
    def get(self):
        if not current_user.has_role('customer'):
            return make_response(
                jsonify({'message': 'Student access required.'}),
                403
            )

        customer = Customer.query.filter_by(
            user_id=current_user.id
        ).first()

        if not customer:
            return make_response(
                jsonify({'message': 'Student profile not found.'}),
                404
            )

        return make_response(
            jsonify({
                'message': 'Profile fetched successfully.',
                'profile': self.get_profile_data(customer)
            }),
            200
        )

    @auth_required()
    def put(self):
        if not current_user.has_role('customer'):
            return make_response(
                jsonify({'message': 'Student access required.'}),
                403
            )

        customer = Customer.query.filter_by(
            user_id=current_user.id
        ).first()

        if not customer:
            return make_response(
                jsonify({'message': 'Student profile not found.'}),
                404
            )

        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return make_response(
                jsonify({'message': 'Please provide valid JSON data.'}),
                400
            )

        editable_fields = [
            'name',
            'dob',
            'gender',
            'mobile',
            'alternate_mobile',
            'id_type',
            'id_number',
            'cor_address',
            'cor_state',
            'cor_district',
            'cor_pincode',
            'per_address',
            'per_state',
            'per_district',
            'per_pincode',
            'student_id',
            'college_name',
            'course',
            'profile_photo'
        ]

        if not any(field in data for field in editable_fields):
            return make_response(
                jsonify({'message': 'No editable profile fields provided.'}),
                400
            )

        try:
            for field in editable_fields:
                if field not in data:
                    continue

                value = data[field]

                if field == 'dob':
                    if value in (None, ''):
                        value = None
                    else:
                        try:
                            value = date.fromisoformat(value)
                        except (ValueError, TypeError):
                            return make_response(
                                jsonify({
                                    'message': 'Date of birth must use YYYY-MM-DD format.'
                                }),
                                400
                            )

                elif value is not None:
                    if not isinstance(value, str):
                        return make_response(
                            jsonify({
                                'message': f'{field} must be a string.'
                            }),
                            400
                        )
                    value = value.strip()

                setattr(customer, field, value)

            db.session.commit()

            return make_response(
                jsonify({
                    'message': 'Profile updated successfully.',
                    'profile': self.get_profile_data(customer)
                }),
                200
            )

        except Exception:
            db.session.rollback()
            return make_response(
                jsonify({'message': 'Failed to update profile.'}),
                500
            )


class StudentPropertyDetailApi(Resource):
    @auth_required()
    def get(self, property_id):
        if not current_user.has_role("customer"):
            return make_response(jsonify({"message": "Student access required."}), 403)

        prop = Property.query.filter_by(
            id=property_id,
            verification_status="verified"
        ).first()

        if not prop:
            return make_response(jsonify({"message": "Property not found."}), 404)

        images = [
            {
                "id": image.id,
                "image_url": image.image_url,
                "is_primary": bool(image.is_primary)
            }
            for image in sorted(
                prop.images,
                key=lambda item: (not bool(item.is_primary), item.id)
            )
        ]

        rooms = []
        for room in prop.rooms:
            amenity_names = []
            amenity_ids = room.amenities or []

            if isinstance(amenity_ids, list):
                valid_ids = [
                    item.get("id") if isinstance(item, dict) else item
                    for item in amenity_ids
                ]
                valid_ids = [item for item in valid_ids if isinstance(item, int) or (isinstance(item, str) and item.isdigit())]
                if valid_ids:
                    amenities = Amenity.query.filter(Amenity.id.in_([int(item) for item in valid_ids])).all()
                    amenity_names = [
                        {"id": amenity.id, "name": amenity.name}
                        for amenity in amenities
                    ]
                elif amenity_ids and all(isinstance(item, dict) and item.get("name") for item in amenity_ids):
                    amenity_names = [
                        {"id": item.get("id"), "name": item["name"]}
                        for item in amenity_ids
                    ]

            rooms.append({
                "id": room.id,
                "room_number": room.room_number,
                "room_type": room.room_type,
                "capacity": room.capacity,
                "price_per_night": room.price_per_night,
                "available": bool(room.available),
                "amenities": amenity_names
            })

        data = {
            "id": prop.id,
            "name": prop.name,
            "description": prop.description or "",
            "address": prop.address,
            "city": prop.city,
            "district": prop.district,
            "state": prop.state,
            "pincode": prop.pincode,
            "verification_status": prop.verification_status,
            "images": images,
            "rooms": rooms
        }

        return make_response(jsonify({
            "message": "Property details fetched successfully.",
            "property": data
        }), 200)


class StudentBookingCreateApi(Resource):
    @auth_required()
    def post(self):
        if not current_user.has_role("customer"):
            return make_response(jsonify({"message": "Student access required."}), 403)

        customer = Customer.query.filter_by(user_id=current_user.id).first()
        if not customer:
            return make_response(jsonify({"message": "Student profile not found."}), 404)

        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return make_response(jsonify({"message": "Please provide valid JSON data."}), 400)

        required_fields = ["property_id", "room_id", "check_in", "check_out"]
        missing_fields = [field for field in required_fields if data.get(field) in (None, "")]
        if missing_fields:
            return make_response(jsonify({
                "message": "Required fields are missing.",
                "missing_fields": missing_fields
            }), 400)

        try:
            property_id = int(data["property_id"])
            room_id = int(data["room_id"])
            number_of_guests = int(data.get("number_of_guests", 1))
            check_in = datetime.fromisoformat(str(data["check_in"]).replace("Z", "+00:00"))
            check_out = datetime.fromisoformat(str(data["check_out"]).replace("Z", "+00:00"))
        except (TypeError, ValueError):
            return make_response(jsonify({
                "message": "property_id, room_id, guests or dates are invalid."
            }), 400)

        if check_in.tzinfo is not None:
            check_in = check_in.replace(tzinfo=None)
        if check_out.tzinfo is not None:
            check_out = check_out.replace(tzinfo=None)

        if check_out <= check_in:
            return make_response(jsonify({
                "message": "Check-out must be after check-in."
            }), 400)

        if check_in.date() < datetime.utcnow().date():
            return make_response(jsonify({
                "message": "Check-in date cannot be in the past."
            }), 400)

        if number_of_guests < 1:
            return make_response(jsonify({
                "message": "At least one guest is required."
            }), 400)

        prop = Property.query.filter_by(
            id=property_id,
            verification_status="verified"
        ).first()
        if not prop:
            return make_response(jsonify({"message": "Property not found."}), 404)

        room = Room.query.filter_by(
            id=room_id,
            property_id=property_id
        ).first()
        if not room:
            return make_response(jsonify({"message": "Room not found for this property."}), 404)

        if not room.available:
            return make_response(jsonify({"message": "This room is not available."}), 409)

        if number_of_guests > room.capacity:
            return make_response(jsonify({
                "message": "Number of guests exceeds room capacity.",
                "room_capacity": room.capacity
            }), 400)

        overlapping_booking = Booking.query.filter(
            Booking.room_id == room.id,
            Booking.status.in_(["pending", "confirmed"]),
            Booking.check_in < check_out,
            Booking.check_out > check_in
        ).first()

        if overlapping_booking:
            return make_response(jsonify({
                "message": "This room is already booked or awaiting confirmation for the selected dates."
            }), 409)

        nights = (check_out.date() - check_in.date()).days
        total_amount = float(room.price_per_night) * nights

        booking = Booking(
            customer_id=customer.id,
            property_id=prop.id,
            room_id=room.id,
            check_in=check_in,
            check_out=check_out,
            number_of_guests=number_of_guests,
            total_amount=total_amount,
            status="confirmed"
        )

        try:
            db.session.add(booking)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return make_response(jsonify({"message": "Failed to create booking."}), 500)

        return make_response(jsonify({
            "message": "Booking request submitted successfully.",
            "booking": {
                "id": booking.id,
                "customer_id": booking.customer_id,
                "property_id": booking.property_id,
                "room_id": booking.room_id,
                "check_in": booking.check_in.isoformat(),
                "check_out": booking.check_out.isoformat(),
                "number_of_guests": booking.number_of_guests,
                "nights": nights,
                "price_per_night": room.price_per_night,
                "total_amount": booking.total_amount,
                "status": booking.status,
                "created_at": booking.created_at.isoformat() if booking.created_at else None
            }
        }), 201)
