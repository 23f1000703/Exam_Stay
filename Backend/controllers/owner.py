'''
from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_security import auth_required, current_user
from datetime import datetime
import os
import uuid

from werkzeug.utils import secure_filename
from controllers.database import db
from controllers.model import Owner, Property, Room, Booking, Payment, PropertyImage ,Amenity

class OwnerDashboardApi(Resource):

    @auth_required()
    def get(self):

        owner = Owner.query.filter_by(
            user_id=current_user.id
        ).first()

        if not owner:
            return make_response(
                jsonify({
                    'message': 'Owner profile not found.'
                }),
                404
            )

        properties = Property.query.filter_by(
            owner_id=owner.id
        ).all()

        property_ids = [property.id for property in properties]
        total_property = len(property_ids)

        if not property_ids:
            return make_response(
                jsonify({
                    'message': 'Dashboard data fetched successfully.',
                    'dashboard': {
                        'total_properties': 0,
                        'total_rooms': 0,
                        'total_bookings': 0,
                        'total_earnings': 0,
                        'upcoming_bookings': 0,
                        'recent_bookings': []
                    }
                }),
                200
            )

        total_rooms = Room.query.filter(
            Room.property_id.in_(property_ids)
        ).count()

        bookings = Booking.query.filter(
            Booking.property_id.in_(property_ids)
        ).all()

        total_bookings = len(bookings)

        total_earnings = db.session.query(
            db.func.coalesce(db.func.sum(Payment.amount), 0)
        ).join(
            Booking,
            Payment.booking_id == Booking.id
        ).filter(
            Booking.property_id.in_(property_ids),
            Payment.status == 'completed'
        ).scalar()

        upcoming_bookings = Booking.query.filter(
            Booking.property_id.in_(property_ids),
            Booking.check_in > datetime.utcnow(),
            Booking.status.in_(['confirmed', 'pending'])
        ).count()

        recent_bookings = Booking.query.filter(
            Booking.property_id.in_(property_ids)
        ).order_by(
            Booking.created_at.desc()
        ).limit(5).all()

        recent_booking_data = []

        for booking in recent_bookings:

            recent_booking_data.append({
                'booking_id': booking.id,
                'property_id': booking.property_id,
                'room_id': booking.room_id,
                'check_in': booking.check_in.isoformat(),
                'check_out': booking.check_out.isoformat(),
                'number_of_guests': booking.number_of_guests,
                'total_amount': booking.total_amount,
                'status': booking.status,
                'created_at': booking.created_at.isoformat()
            })

        return make_response(
            jsonify({
                'message': 'Dashboard data fetched successfully.',
                'dashboard': {
                    'total_properties': total_property,
                    'total_rooms': total_rooms,
                    'total_bookings': total_bookings,
                    'total_earnings': float(total_earnings),
                    'upcoming_bookings': upcoming_bookings,
                    'recent_bookings': recent_booking_data
                }
            }),
            200
        )
    


        data = request.get_json()

        if not data:
            return make_response(
                jsonify({
                    'message': 'Property data is required.'
                }),
                400
            )

        owner = Owner.query.filter_by(
            user_id=current_user.id
        ).first()

        if not owner:
            return make_response(
                jsonify({
                    'message': 'Owner profile not found.'
                }),
                404
            )

        required_fields = [
            'name',
            'address',
            'city',
            'district',
            'state',
            'pincode'
        ]

        for field in required_fields:

            value = data.get(field)

            if value is None or str(value).strip() == '':
                return make_response(
                    jsonify({
                        'message': f'{field} is required.'
                    }),
                    400
                )

        try:

            property = Property(
                owner_id=owner.id,
                name=data.get('name').strip(),
                description=data.get('description'),
                address=data.get('address').strip(),
                city=data.get('city').strip(),
                district=data.get('district').strip(),
                state=data.get('state').strip(),
                pincode=data.get('pincode').strip(),
                latitude=data.get('latitude'),
                longitude=data.get('longitude'),
                verification_status='pending'
            )

            db.session.add(property)
            db.session.commit()

            return make_response(
                jsonify({
                    'message': 'Property added successfully.',
                    'property': {
                        'id': property.id,
                        'owner_id': property.owner_id,
                        'name': property.name,
                        'description': property.description,
                        'address': property.address,
                        'city': property.city,
                        'district': property.district,
                        'state': property.state,
                        'pincode': property.pincode,
                        'latitude': property.latitude,
                        'longitude': property.longitude,
                        'verification_status': property.verification_status
                    }
                }),
                201
            )

        except Exception as e:

            db.session.rollback()
            print('PROPERTY ERROR:', e)

            return make_response(
                jsonify({
                    'message': 'property not added',
                    'error': str(e)
                }),
                500
            )

class OwnerPropertyImageApi(Resource):

    @auth_required()
    def post(self, property_id):

        owner = Owner.query.filter_by(
            user_id=current_user.id
        ).first()

        if not owner:
            return make_response(
                jsonify({
                    'message': 'Owner profile not found.'
                }),
                404
            )

        property = Property.query.filter_by(
            id=property_id,
            owner_id=owner.id
        ).first()

        if not property:
            return make_response(
                jsonify({
                    'message': 'Property not found or you do not have access to this property.'
                }),
                404
            )

        images = request.files.getlist('images')

        if not images:
            return make_response(
                jsonify({
                    'message': 'At least one image is required.'
                }),
                400
            )

        allowed_extensions = {
            'jpg',
            'jpeg',
            'png',
            'webp'
        }

        upload_folder = os.path.join(
            'uploads',
            'properties'
        )

        os.makedirs(
            upload_folder,
            exist_ok=True
        )

        uploaded_images = []

        try:

            existing_images = PropertyImage.query.filter_by(
                property_id=property.id
            ).count()

            for index, image in enumerate(images):

                if image.filename == '':
                    continue

                filename = secure_filename(
                    image.filename
                )

                extension = filename.rsplit(
                    '.',
                    1
                )[-1].lower()

                if extension not in allowed_extensions:
                    return make_response(
                        jsonify({
                            'message': f'Invalid image format: {extension}. Only JPG, JPEG, PNG and WEBP are allowed.'
                        }),
                        400
                    )

                new_filename = (
                    f'{uuid.uuid4().hex}.{extension}'
                )

                file_path = os.path.join(
                    upload_folder,
                    new_filename
                )

                image.save(file_path)

                image_url = (
                    f'/uploads/properties/{new_filename}'
                )

                property_image = PropertyImage(
                    property_id=property.id,
                    image_url=image_url,
                    is_primary=(
                        existing_images == 0 and index == 0
                    )
                )

                db.session.add(property_image)

                uploaded_images.append({
                    'image_url': image_url,
                    'is_primary': property_image.is_primary
                })

            db.session.commit()

            return make_response(
                jsonify({
                    'message': 'Property images uploaded successfully.',
                    'property_id': property.id,
                    'images': uploaded_images
                }),
                201
            )

        except Exception as e:

            db.session.rollback()

            return make_response(
                jsonify({
                    'message': 'Failed to upload property images.',
                    'error': str(e)
                }),
                500
            )

class OwnerPropertiesApi(Resource):

    @auth_required()
    def get(self):

        owner = Owner.query.filter_by(
            user_id=current_user.id
        ).first()

        if not owner:
            return make_response(
                jsonify({'message': 'Owner profile not found.'}),404)

        properties = Property.query.filter_by(owner_id=owner.id).order_by(Property.created_at.desc()).all()

        property_data = []

        for property in properties:

            primary_image = next(
                (
                    image.image_url
                    for image in property.images
                    if image.is_primary
                ),
                None
            )

            if not primary_image and property.images:
                primary_image = property.images[0].image_url

            property_data.append({
                'id': property.id,
                'name': property.name,
                'description': property.description,
                'address': property.address,
                'city': property.city,
                'district': property.district,
                'state': property.state,
                'pincode': property.pincode,
                'latitude': property.latitude,
                'longitude': property.longitude,
                'verification_status': property.verification_status,
                'total_rooms': len(property.rooms),
                'total_images': len(property.images),
                'primary_image': primary_image,
                'created_at': property.created_at.isoformat()
                if property.created_at else None,
                'updated_at': property.updated_at.isoformat()
                if property.updated_at else None
            })

        return make_response(
            jsonify({
                'message': 'Properties fetched successfully.',
                'properties': property_data
            }),
            200
        )
    
    @auth_required()
    def post(self):

        data = request.get_json()

        if not data:
            return make_response(
                jsonify({
                    'message': 'Property data is required.'
                }),
                400
            )

        owner = Owner.query.filter_by(user_id=current_user.id).first()

        if not owner:
            return make_response(jsonify({'message': 'Owner profile not found.'}),404)

        required_fields = [
            'name',
            'address',
            'city',
            'district',
            'state',
            'pincode'
        ]

        for field in required_fields:

            value = data.get(field)

            if value is None or str(value).strip() == '':
                return make_response(
                    jsonify({
                        'message': f'{field} is required.'
                    }),
                    400
                )

        try:

            property = Property(
                owner_id=owner.id,
                name=data.get('name').strip(),
                description=data.get('description'),
                address=data.get('address').strip(),
                city=data.get('city').strip(),
                district=data.get('district').strip(),
                state=data.get('state').strip(),
                pincode=data.get('pincode').strip(),
                latitude=data.get('latitude'),
                longitude=data.get('longitude'),
                verification_status='pending'
            )

            db.session.add(property)
            db.session.commit()

            return make_response(
                jsonify({
                    'message': 'Property added successfully.',
                    'property': {
                        'id': property.id,
                        'owner_id': property.owner_id,
                        'name': property.name,
                        'description': property.description,
                        'address': property.address,
                        'city': property.city,
                        'district': property.district,
                        'state': property.state,
                        'pincode': property.pincode,
                        'latitude': property.latitude,
                        'longitude': property.longitude,
                        'verification_status': property.verification_status
                    }
                }),
                201
            )

        except Exception as e:

            db.session.rollback()
            print('PROPERTY ERROR:', e)

            return make_response(
                jsonify({
                    'message': 'property not added',
                    'error': str(e)
                }),
                500
            )



class OwnerPropertyApi(Resource):

    @auth_required()
    def get(self, property_id):

        owner = Owner.query.filter_by(user_id=current_user.id).first()

        if not owner:
            return make_response(
                jsonify({'message': 'Owner profile not found.'}),404)

        property = Property.query.filter_by(id=property_id,owner_id=owner.id).first()

        if not property:
            return make_response(jsonify({'message': 'Property not found.'}),404)

        images = []

        for image in property.images:
            images.append({
                'id': image.id,
                'image_url': image.image_url,
                'is_primary': image.is_primary
            })

        rooms = []
        for room in property.rooms:
            amenity_ids = room.amenities or []

            room_amenities = Amenity.query.filter(Amenity.id.in_(amenity_ids)).all() if amenity_ids else []

            rooms.append({
                'id': room.id,
                'room_number': room.room_number,
                'room_type': room.room_type,
                'capacity': room.capacity,
                'price_per_night': room.price_per_night,
                'available': room.available,
                'amenities': [{'id': amenity.id,
                                'name': amenity.name
                            }for amenity in room_amenities]})

        return make_response(jsonify({
                'message': 'Property fetched successfully.',
                'property': {
                    'id': property.id,
                    'owner_id': property.owner_id,
                    'name': property.name,
                    'description': property.description,
                    'address': property.address,
                    'city': property.city,
                    'district': property.district,
                    'state': property.state,
                    'pincode': property.pincode,
                    'latitude': property.latitude,
                    'longitude': property.longitude,
                    'verification_status': property.verification_status,
                    'created_at': property.created_at.isoformat()
                    if property.created_at else None,
                    'updated_at': property.updated_at.isoformat()
                    if property.updated_at else None,
                    'images': images,
                    'rooms': rooms,
                }
            }),
            200
        )


    @auth_required()
    def put(self, property_id):

        owner = Owner.query.filter_by(
            user_id=current_user.id
        ).first()

        if not owner:
            return make_response(
                jsonify({
                    'message': 'Owner profile not found.'
                }),
                404
            )

        property = Property.query.filter_by(
            id=property_id,
            owner_id=owner.id
        ).first()

        if not property:
            return make_response(
                jsonify({
                    'message': 'Property not found.'
                }),
                404
            )

        data = request.get_json()

        if not data:
            return make_response(
                jsonify({
                    'message': 'Property data is required.'
                }),
                400
            )

        required_fields = [
            'name',
            'address',
            'city',
            'district',
            'state',
            'pincode'
        ]

        for field in required_fields:

            value = data.get(field)

            if value is None or str(value).strip() == '':
                return make_response(
                    jsonify({
                        'message': f'{field} is required.'
                    }),
                    400
                )

        try:

            property.name = data.get('name').strip()
            property.description = data.get('description')
            property.address = data.get('address').strip()
            property.city = data.get('city').strip()
            property.district = data.get('district').strip()
            property.state = data.get('state').strip()
            property.pincode = data.get('pincode').strip()
            property.latitude = data.get('latitude')
            property.longitude = data.get('longitude')

            db.session.commit()

            return make_response(
                jsonify({
                    'message': 'Property updated successfully.',
                    'property': {
                        'id': property.id,
                        'name': property.name,
                        'description': property.description,
                        'address': property.address,
                        'city': property.city,
                        'district': property.district,
                        'state': property.state,
                        'pincode': property.pincode,
                        'latitude': property.latitude,
                        'longitude': property.longitude,
                        'verification_status': property.verification_status
                    }
                }),
                200
            )

        except Exception as e:

            db.session.rollback()

            return make_response(
                jsonify({
                    'message': 'Failed to update property.',
                    'error': str(e)
                }),
                500
            )


    @auth_required()
    def delete(self, property_id):

        owner = Owner.query.filter_by(
            user_id=current_user.id
        ).first()

        if not owner:
            return make_response(
                jsonify({
                    'message': 'Owner profile not found.'
                }),
                404
            )

        property = Property.query.filter_by(
            id=property_id,
            owner_id=owner.id
        ).first()

        if not property:
            return make_response(
                jsonify({
                    'message': 'Property not found.'
                }),
                404
            )

        try:

            db.session.delete(property)
            db.session.commit()

            return make_response(
                jsonify({
                    'message': 'Property deleted successfully.'
                }),
                200
            )

        except Exception as e:

            db.session.rollback()

            return make_response(
                jsonify({
                    'message': 'Failed to delete property.',
                    'error': str(e)
                }),
                500
            )

class OwnerProfileApi(Resource):

    @auth_required()
    def get(self):

        owner = Owner.query.filter_by(
            user_id=current_user.id
        ).first()

        if not owner:
            return make_response(
                jsonify({
                    'message': 'Owner profile not found.'
                }),
                404
            )

        return make_response(
            jsonify({
                'message': 'Owner profile fetched successfully.',
                'owner': {
                    'id': owner.id,
                    'user_id': owner.user_id,
                    'name': owner.name,
                    'email': owner.user.email if owner.user else None,
                    'mobile': owner.mobile,
                    'id_type': owner.id_type,
                    'id_number': owner.id_number,
                    'property_address': owner.property_address,
                    'per_state': owner.per_state,
                    'per_district': owner.per_district,
                    'per_pincode': owner.per_pincode,
                    'profile_photo': owner.profile_photo,
                    'created_at': owner.created_at.isoformat()
                    if owner.created_at else None,
                    'updated_at': owner.updated_at.isoformat()
                    if owner.updated_at else None
                }
            }),
            200
        )

class OwnerBookingsApi(Resource):

    @auth_required()
    def get(self):

        owner = Owner.query.filter_by(
            user_id=current_user.id
        ).first()

        if not owner:
            return make_response(
                jsonify({
                    'message': 'Owner profile not found.'
                }),
                404
            )

        properties = Property.query.filter_by(
            owner_id=owner.id
        ).all()

        property_ids = [property.id for property in properties]

        if not property_ids:
            return make_response(
                jsonify({
                    'message': 'Bookings fetched successfully.',
                    'bookings': []
                }),
                200
            )

        bookings = Booking.query.filter(
            Booking.property_id.in_(property_ids)
        ).order_by(
            Booking.created_at.desc()
        ).all()

        booking_data = []

        for booking in bookings:

            student_name = None
            student_email = None
            student_mobile = None

            if booking.customer:
                student_name = booking.customer.name
                student_mobile = booking.customer.mobile

                if booking.customer.user:
                    student_email = booking.customer.user.email

            booking_data.append({
                'id': booking.id,
                'property_id': booking.property_id,
                'property_name': booking.property.name
                    if booking.property else None,

                'room_id': booking.room_id,
                'room_number': booking.room.room_number
                    if booking.room else None,

                'student_name': student_name,
                'student_email': student_email,
                'student_mobile': student_mobile,

                'check_in': booking.check_in.isoformat()
                    if booking.check_in else None,

                'check_out': booking.check_out.isoformat()
                    if booking.check_out else None,

                'number_of_guests': booking.number_of_guests,

                'total_amount': float(booking.total_amount)
                    if booking.total_amount is not None else 0,

                'status': booking.status,

                'created_at': booking.created_at.isoformat()
                    if booking.created_at else None
            })

        return make_response(
            jsonify({
                'message': 'Bookings fetched successfully.',
                'bookings': booking_data
            }),
            200
        )


class AmenitiesApi(Resource):

    @auth_required()
    def get(self):
        amenities = Amenity.query.order_by(Amenity.name.asc()).all()

        return make_response(jsonify({
            'message': 'Amenities fetched successfully.',
            'amenities': [
                {'id': item.id, 'name': item.name}
                for item in amenities
            ]
        }), 200)

    @auth_required()
    def post(self):
        if not current_user.has_role('owner'):
            return make_response(
                jsonify({'message': 'Owner access required.'}), 403
            )

        data = request.get_json(silent=True) or {}
        name = data.get('name', '')

        if not isinstance(name, str) or not name.strip():
            return make_response(
                jsonify({'message': 'Amenity name is required.'}), 400
            )

        name = name.strip()
        existing = Amenity.query.filter(
            db.func.lower(Amenity.name) == name.lower()
        ).first()

        if existing:
            return make_response(jsonify({
                'message': 'Amenity already exists.',
                'amenity': {
                    'id': existing.id,
                    'name': existing.name
                }
            }), 200)

        try:
            amenity = Amenity(name=name)
            db.session.add(amenity)
            db.session.commit()

            return make_response(jsonify({
                'message': 'Amenity added successfully.',
                'amenity': {
                    'id': amenity.id,
                    'name': amenity.name
                }
            }), 201)

        except Exception as e:
            db.session.rollback()
            print('AMENITY ERROR:', e)
            return make_response(
                jsonify({'message': 'Failed to add amenity.'}), 500
            )


class OwnerPropertyAmenitiesApi(Resource):

    @auth_required()
    def put(self, property_id):
        if not current_user.has_role('owner'):
            return make_response(
                jsonify({'message': 'Owner access required.'}), 403
            )

        owner = Owner.query.filter_by(user_id=current_user.id).first()

        if not owner:
            return make_response(
                jsonify({'message': 'Owner profile not found.'}), 404
            )

        prop = Property.query.filter_by(
            id=property_id,
            owner_id=owner.id
        ).first()

        if not prop:
            return make_response(
                jsonify({'message': 'Property not found.'}), 404
            )

        data = request.get_json(silent=True) or {}
        amenity_ids = data.get('amenity_ids', [])

        if not isinstance(amenity_ids, list):
            return make_response(
                jsonify({'message': 'amenity_ids must be a list.'}), 400
            )

        try:
            ids = list(set(int(item) for item in amenity_ids))
        except (ValueError, TypeError):
            return make_response(
                jsonify({'message': 'Invalid amenity IDs.'}), 400
            )

        amenities = Amenity.query.filter(Amenity.id.in_(ids)).all()

        if len(amenities) != len(ids):
            return make_response(
                jsonify({'message': 'One or more amenities were not found.'}),
                400
            )

        try:
            prop.amenities = amenities
            db.session.commit()

            return make_response(jsonify({
                'message': 'Property amenities saved successfully.',
                'amenities': [
                    {'id': item.id, 'name': item.name}
                    for item in prop.amenities
                ]
            }), 200)

        except Exception as e:
            db.session.rollback()
            print('PROPERTY AMENITIES ERROR:', e)
            return make_response(
                jsonify({'message': 'Failed to save property amenities.'}),
                500
            )


class OwnerPropertyRoomApi(Resource):

    @auth_required()
    def post(self, property_id):

        owner = Owner.query.filter_by(user_id=current_user.id).first()

        if not owner:
            return make_response(
                jsonify({'message': 'Owner profile not found.'}),404)

        property = Property.query.filter_by(id=property_id,owner_id=owner.id).first()

        if not property:
            return make_response(
                jsonify({'message': 'Property not found.'}),404)

        data = request.get_json()

        if not data:
            return make_response(
                jsonify({'message': 'Room data is required.'}),400)

        required_fields = [
            'room_number',
            'room_type',
            'capacity',
            'price_per_night'
        ]

        for field in required_fields:
            if data.get(field) is None or str(data.get(field)).strip() == '':
                return make_response(
                    jsonify({
                        'message': f'{field} is required.'
                    }),
                    400
                )

        try:
            room = Room(
                property_id=property.id,
                room_number=str(data.get('room_number')).strip(),
                room_type=str(data.get('room_type')).strip(),
                capacity=int(data.get('capacity')),
                price_per_night=float(data.get('price_per_night')),
                available=data.get('available', True)
                amenities=amenity_ids
            )

            db.session.add(room)
            db.session.commit()

            return make_response(
                jsonify({
                    'message': 'Room added successfully.',
                    'room': {
                        'id': room.id,
                        'property_id': room.property_id,
                        'room_number': room.room_number,
                        'room_type': room.room_type,
                        'capacity': room.capacity,
                        'price_per_night': room.price_per_night,
                        'available': room.available,
                        
                    }
                }),
                201
            )

        except (ValueError, TypeError):
            db.session.rollback()

            return make_response(
                jsonify({
                    'message': 'Invalid room data.'
                }),
                400
            )

        except Exception as e:
            db.session.rollback()

            return make_response(
                jsonify({
                    'message': 'Failed to add room.',
                    'error': str(e)
                }),
                500
            )

    @auth_required()
    def put(self, property_id, room_id):

        owner = Owner.query.filter_by(
            user_id=current_user.id
        ).first()

        if not owner:
            return make_response(
                jsonify({
                    'message': 'Owner profile not found.'
                }),
                404
            )

        property = Property.query.filter_by(
            id=property_id,
            owner_id=owner.id
        ).first()

        if not property:
            return make_response(
                jsonify({
                    'message': 'Property not found.'
                }),
                404
            )

        room = Room.query.filter_by(
            id=room_id,
            property_id=property.id
        ).first()

        if not room:
            return make_response(
                jsonify({
                    'message': 'Room not found.'
                }),
                404
            )

        data = request.get_json()

        if not data:
            return make_response(
                jsonify({
                    'message': 'Room data is required.'
                }),
                400
            )

        required_fields = [
            'room_number',
            'room_type',
            'capacity',
            'price_per_night'
        ]

        for field in required_fields:
            if data.get(field) is None or str(data.get(field)).strip() == '':
                return make_response(
                    jsonify({
                        'message': f'{field} is required.'
                    }),
                    400
                )

        try:
            room.room_number = str(
                data.get('room_number')
            ).strip()

            room.room_type = str(
                data.get('room_type')
            ).strip()

            room.capacity = int(
                data.get('capacity')
            )

            room.price_per_night = float(
                data.get('price_per_night')
            )

            room.available = data.get(
                'available',
                True
            )

            db.session.commit()

            return make_response(
                jsonify({
                    'message': 'Room updated successfully.',
                    'room': {
                        'id': room.id,
                        'property_id': room.property_id,
                        'room_number': room.room_number,
                        'room_type': room.room_type,
                        'capacity': room.capacity,
                        'price_per_night': room.price_per_night,
                        'available': room.available
                    }
                }),
                200
            )

        except (ValueError, TypeError):
            db.session.rollback()

            return make_response(
                jsonify({
                    'message': 'Invalid room data.'
                }),
                400
            )

        except Exception as e:
            db.session.rollback()

            return make_response(
                jsonify({
                    'message': 'Failed to update room.',
                    'error': str(e)
                }),
                500
            )

    @auth_required()
    def delete(self, property_id, room_id):

        owner = Owner.query.filter_by(
            user_id=current_user.id
        ).first()

        if not owner:
            return make_response(
                jsonify({
                    'message': 'Owner profile not found.'
                }),
                404
            )

        property = Property.query.filter_by(
            id=property_id,
            owner_id=owner.id
        ).first()

        if not property:
            return make_response(
                jsonify({
                    'message': 'Property not found.'
                }),
                404
            )

        room = Room.query.filter_by(
            id=room_id,
            property_id=property.id
        ).first()

        if not room:
            return make_response(
                jsonify({
                    'message': 'Room not found.'
                }),
                404
            )

        try:
            db.session.delete(room)
            db.session.commit()

            return make_response(
                jsonify({
                    'message': 'Room deleted successfully.'
                }),
                200
            )

        except Exception as e:
            db.session.rollback()

            return make_response(
                jsonify({
                    'message': 'Failed to delete room.',
                    'error': str(e)
                }),
                500
            )

'''

from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_security import auth_required, current_user
from datetime import datetime
import os
import uuid

from werkzeug.utils import secure_filename
from controllers.database import db
from controllers.model import Owner, Property, Room, Booking, Payment, PropertyImage, Amenity


def validate_amenity_ids(amenity_ids):
    """Validate a list of Amenity IDs before storing it in Room.amenities."""
    if not isinstance(amenity_ids, list):
        return None, 'amenities must be a list.'

    try:
        ids = list(dict.fromkeys(int(item) for item in amenity_ids))
    except (ValueError, TypeError):
        return None, 'Invalid amenity IDs.'

    if any(item <= 0 for item in ids):
        return None, 'Invalid amenity IDs.'

    existing_ids = {
        item.id for item in Amenity.query.filter(Amenity.id.in_(ids)).all()
    } if ids else set()

    if existing_ids != set(ids):
        return None, 'One or more amenities were not found.'

    return ids, None

class OwnerDashboardApi(Resource):

    @auth_required()
    def get(self):

        owner = Owner.query.filter_by(
            user_id=current_user.id
        ).first()

        if not owner:
            return make_response(
                jsonify({
                    'message': 'Owner profile not found.'
                }),
                404
            )

        properties = Property.query.filter_by(
            owner_id=owner.id
        ).all()

        property_ids = [property.id for property in properties]
        total_property = len(property_ids)

        if not property_ids:
            return make_response(
                jsonify({
                    'message': 'Dashboard data fetched successfully.',
                    'dashboard': {
                        'total_properties': 0,
                        'total_rooms': 0,
                        'total_bookings': 0,
                        'total_earnings': 0,
                        'upcoming_bookings': 0,
                        'recent_bookings': []
                    }
                }),
                200
            )

        total_rooms = Room.query.filter(
            Room.property_id.in_(property_ids)
        ).count()

        bookings = Booking.query.filter(
            Booking.property_id.in_(property_ids)
        ).all()

        total_bookings = len(bookings)

        total_earnings = db.session.query(
            db.func.coalesce(db.func.sum(Payment.amount), 0)
        ).join(
            Booking,
            Payment.booking_id == Booking.id
        ).filter(
            Booking.property_id.in_(property_ids),
            Payment.status == 'completed'
        ).scalar()

        upcoming_bookings = Booking.query.filter(
            Booking.property_id.in_(property_ids),
            Booking.check_in > datetime.utcnow(),
            Booking.status.in_(['confirmed', 'pending'])
        ).count()

        recent_bookings = Booking.query.filter(
            Booking.property_id.in_(property_ids)
        ).order_by(
            Booking.created_at.desc()
        ).limit(5).all()

        recent_booking_data = []

        for booking in recent_bookings:

            recent_booking_data.append({
                'booking_id': booking.id,
                'property_id': booking.property_id,
                'room_id': booking.room_id,
                'check_in': booking.check_in.isoformat(),
                'check_out': booking.check_out.isoformat(),
                'number_of_guests': booking.number_of_guests,
                'total_amount': booking.total_amount,
                'status': booking.status,
                'created_at': booking.created_at.isoformat()
            })

        return make_response(
            jsonify({
                'message': 'Dashboard data fetched successfully.',
                'dashboard': {
                    'total_properties': total_property,
                    'total_rooms': total_rooms,
                    'total_bookings': total_bookings,
                    'total_earnings': float(total_earnings),
                    'upcoming_bookings': upcoming_bookings,
                    'recent_bookings': recent_booking_data
                }
            }),
            200
        )
    


        data = request.get_json()

        if not data:
            return make_response(
                jsonify({
                    'message': 'Property data is required.'
                }),
                400
            )

        owner = Owner.query.filter_by(
            user_id=current_user.id
        ).first()

        if not owner:
            return make_response(
                jsonify({
                    'message': 'Owner profile not found.'
                }),
                404
            )

        required_fields = [
            'name',
            'address',
            'city',
            'district',
            'state',
            'pincode'
        ]

        for field in required_fields:

            value = data.get(field)

            if value is None or str(value).strip() == '':
                return make_response(
                    jsonify({
                        'message': f'{field} is required.'
                    }),
                    400
                )

        try:

            property = Property(
                owner_id=owner.id,
                name=data.get('name').strip(),
                description=data.get('description'),
                address=data.get('address').strip(),
                city=data.get('city').strip(),
                district=data.get('district').strip(),
                state=data.get('state').strip(),
                pincode=data.get('pincode').strip(),
                latitude=data.get('latitude'),
                longitude=data.get('longitude'),
                verification_status='pending'
            )

            db.session.add(property)
            db.session.commit()

            return make_response(
                jsonify({
                    'message': 'Property added successfully.',
                    'property': {
                        'id': property.id,
                        'owner_id': property.owner_id,
                        'name': property.name,
                        'description': property.description,
                        'address': property.address,
                        'city': property.city,
                        'district': property.district,
                        'state': property.state,
                        'pincode': property.pincode,
                        'latitude': property.latitude,
                        'longitude': property.longitude,
                        'verification_status': property.verification_status
                    }
                }),
                201
            )

        except Exception as e:

            db.session.rollback()
            print('PROPERTY ERROR:', e)

            return make_response(
                jsonify({
                    'message': 'property not added',
                    'error': str(e)
                }),
                500
            )

class OwnerPropertyImageApi(Resource):

    @auth_required()
    def post(self, property_id):

        owner = Owner.query.filter_by(
            user_id=current_user.id
        ).first()

        if not owner:
            return make_response(
                jsonify({
                    'message': 'Owner profile not found.'
                }),
                404
            )

        property = Property.query.filter_by(
            id=property_id,
            owner_id=owner.id
        ).first()

        if not property:
            return make_response(
                jsonify({
                    'message': 'Property not found or you do not have access to this property.'
                }),
                404
            )

        images = request.files.getlist('images')

        if not images:
            return make_response(
                jsonify({
                    'message': 'At least one image is required.'
                }),
                400
            )

        allowed_extensions = {
            'jpg',
            'jpeg',
            'png',
            'webp'
        }

        upload_folder = os.path.join(
            'uploads',
            'properties'
        )

        os.makedirs(
            upload_folder,
            exist_ok=True
        )

        uploaded_images = []

        try:

            existing_images = PropertyImage.query.filter_by(
                property_id=property.id
            ).count()

            for index, image in enumerate(images):

                if image.filename == '':
                    continue

                filename = secure_filename(
                    image.filename
                )

                extension = filename.rsplit(
                    '.',
                    1
                )[-1].lower()

                if extension not in allowed_extensions:
                    return make_response(
                        jsonify({
                            'message': f'Invalid image format: {extension}. Only JPG, JPEG, PNG and WEBP are allowed.'
                        }),
                        400
                    )

                new_filename = (
                    f'{uuid.uuid4().hex}.{extension}'
                )

                file_path = os.path.join(
                    upload_folder,
                    new_filename
                )

                image.save(file_path)

                image_url = (
                    f'/uploads/properties/{new_filename}'
                )

                property_image = PropertyImage(
                    property_id=property.id,
                    image_url=image_url,
                    is_primary=(
                        existing_images == 0 and index == 0
                    )
                )

                db.session.add(property_image)

                uploaded_images.append({
                    'image_url': image_url,
                    'is_primary': property_image.is_primary
                })

            db.session.commit()

            return make_response(
                jsonify({
                    'message': 'Property images uploaded successfully.',
                    'property_id': property.id,
                    'images': uploaded_images
                }),
                201
            )

        except Exception as e:

            db.session.rollback()

            return make_response(
                jsonify({
                    'message': 'Failed to upload property images.',
                    'error': str(e)
                }),
                500
            )

class OwnerPropertiesApi(Resource):

    @auth_required()
    def get(self):

        owner = Owner.query.filter_by(
            user_id=current_user.id
        ).first()

        if not owner:
            return make_response(
                jsonify({'message': 'Owner profile not found.'}),404)

        properties = Property.query.filter_by(owner_id=owner.id).order_by(Property.created_at.desc()).all()

        property_data = []

        for property in properties:

            primary_image = next(
                (
                    image.image_url
                    for image in property.images
                    if image.is_primary
                ),
                None
            )

            if not primary_image and property.images:
                primary_image = property.images[0].image_url

            property_data.append({
                'id': property.id,
                'name': property.name,
                'description': property.description,
                'address': property.address,
                'city': property.city,
                'district': property.district,
                'state': property.state,
                'pincode': property.pincode,
                'latitude': property.latitude,
                'longitude': property.longitude,
                'verification_status': property.verification_status,
                'total_rooms': len(property.rooms),
                'total_images': len(property.images),
                'primary_image': primary_image,
                'created_at': property.created_at.isoformat()
                if property.created_at else None,
                'updated_at': property.updated_at.isoformat()
                if property.updated_at else None
            })

        return make_response(
            jsonify({
                'message': 'Properties fetched successfully.',
                'properties': property_data
            }),
            200
        )
    
    @auth_required()
    def post(self):

        data = request.get_json()

        if not data:
            return make_response(
                jsonify({
                    'message': 'Property data is required.'
                }),
                400
            )

        owner = Owner.query.filter_by(user_id=current_user.id).first()

        if not owner:
            return make_response(jsonify({'message': 'Owner profile not found.'}),404)

        required_fields = [
            'name',
            'address',
            'city',
            'district',
            'state',
            'pincode'
        ]

        for field in required_fields:

            value = data.get(field)

            if value is None or str(value).strip() == '':
                return make_response(
                    jsonify({
                        'message': f'{field} is required.'
                    }),
                    400
                )

        try:

            property = Property(
                owner_id=owner.id,
                name=data.get('name').strip(),
                description=data.get('description'),
                address=data.get('address').strip(),
                city=data.get('city').strip(),
                district=data.get('district').strip(),
                state=data.get('state').strip(),
                pincode=data.get('pincode').strip(),
                latitude=data.get('latitude'),
                longitude=data.get('longitude'),
                verification_status='pending'
            )

            db.session.add(property)
            db.session.commit()

            return make_response(
                jsonify({
                    'message': 'Property added successfully.',
                    'property': {
                        'id': property.id,
                        'owner_id': property.owner_id,
                        'name': property.name,
                        'description': property.description,
                        'address': property.address,
                        'city': property.city,
                        'district': property.district,
                        'state': property.state,
                        'pincode': property.pincode,
                        'latitude': property.latitude,
                        'longitude': property.longitude,
                        'verification_status': property.verification_status
                    }
                }),
                201
            )

        except Exception as e:

            db.session.rollback()
            print('PROPERTY ERROR:', e)

            return make_response(
                jsonify({
                    'message': 'property not added',
                    'error': str(e)
                }),
                500
            )



class OwnerPropertyApi(Resource):

    @auth_required()
    def get(self, property_id):

        owner = Owner.query.filter_by(user_id=current_user.id).first()

        if not owner:
            return make_response(
                jsonify({'message': 'Owner profile not found.'}),404)

        property = Property.query.filter_by(id=property_id,owner_id=owner.id).first()

        if not property:
            return make_response(jsonify({'message': 'Property not found.'}),404)

        images = []

        for image in property.images:
            images.append({
                'id': image.id,
                'image_url': image.image_url,
                'is_primary': image.is_primary
            })

        rooms = []
        for room in property.rooms:
            amenity_ids = room.amenities or []

            room_amenities = Amenity.query.filter(Amenity.id.in_(amenity_ids)).all() if amenity_ids else []

            rooms.append({
                'id': room.id,
                'room_number': room.room_number,
                'room_type': room.room_type,
                'capacity': room.capacity,
                'price_per_night': room.price_per_night,
                'available': room.available,
                'amenities': [{'id': amenity.id,
                                'name': amenity.name
                            }for amenity in room_amenities]})

        return make_response(jsonify({
                'message': 'Property fetched successfully.',
                'property': {
                    'id': property.id,
                    'owner_id': property.owner_id,
                    'name': property.name,
                    'description': property.description,
                    'address': property.address,
                    'city': property.city,
                    'district': property.district,
                    'state': property.state,
                    'pincode': property.pincode,
                    'latitude': property.latitude,
                    'longitude': property.longitude,
                    'verification_status': property.verification_status,
                    'created_at': property.created_at.isoformat()
                    if property.created_at else None,
                    'updated_at': property.updated_at.isoformat()
                    if property.updated_at else None,
                    'images': images,
                    'rooms': rooms,
                }
            }),
            200
        )


    @auth_required()
    def put(self, property_id):

        owner = Owner.query.filter_by(
            user_id=current_user.id
        ).first()

        if not owner:
            return make_response(
                jsonify({
                    'message': 'Owner profile not found.'
                }),
                404
            )

        property = Property.query.filter_by(
            id=property_id,
            owner_id=owner.id
        ).first()

        if not property:
            return make_response(
                jsonify({
                    'message': 'Property not found.'
                }),
                404
            )

        data = request.get_json()

        if not data:
            return make_response(
                jsonify({
                    'message': 'Property data is required.'
                }),
                400
            )

        required_fields = [
            'name',
            'address',
            'city',
            'district',
            'state',
            'pincode'
        ]

        for field in required_fields:

            value = data.get(field)

            if value is None or str(value).strip() == '':
                return make_response(
                    jsonify({
                        'message': f'{field} is required.'
                    }),
                    400
                )

        try:

            property.name = data.get('name').strip()
            property.description = data.get('description')
            property.address = data.get('address').strip()
            property.city = data.get('city').strip()
            property.district = data.get('district').strip()
            property.state = data.get('state').strip()
            property.pincode = data.get('pincode').strip()
            property.latitude = data.get('latitude')
            property.longitude = data.get('longitude')

            db.session.commit()

            return make_response(
                jsonify({
                    'message': 'Property updated successfully.',
                    'property': {
                        'id': property.id,
                        'name': property.name,
                        'description': property.description,
                        'address': property.address,
                        'city': property.city,
                        'district': property.district,
                        'state': property.state,
                        'pincode': property.pincode,
                        'latitude': property.latitude,
                        'longitude': property.longitude,
                        'verification_status': property.verification_status
                    }
                }),
                200
            )

        except Exception as e:

            db.session.rollback()

            return make_response(
                jsonify({
                    'message': 'Failed to update property.',
                    'error': str(e)
                }),
                500
            )


    @auth_required()
    def delete(self, property_id):

        owner = Owner.query.filter_by(
            user_id=current_user.id
        ).first()

        if not owner:
            return make_response(
                jsonify({
                    'message': 'Owner profile not found.'
                }),
                404
            )

        property = Property.query.filter_by(
            id=property_id,
            owner_id=owner.id
        ).first()

        if not property:
            return make_response(
                jsonify({
                    'message': 'Property not found.'
                }),
                404
            )

        try:

            db.session.delete(property)
            db.session.commit()

            return make_response(
                jsonify({
                    'message': 'Property deleted successfully.'
                }),
                200
            )

        except Exception as e:

            db.session.rollback()

            return make_response(
                jsonify({
                    'message': 'Failed to delete property.',
                    'error': str(e)
                }),
                500
            )

class OwnerProfileApi(Resource):

    @auth_required()
    def get(self):

        owner = Owner.query.filter_by(
            user_id=current_user.id
        ).first()

        if not owner:
            return make_response(
                jsonify({
                    'message': 'Owner profile not found.'
                }),
                404
            )

        return make_response(
            jsonify({
                'message': 'Owner profile fetched successfully.',
                'owner': {
                    'id': owner.id,
                    'user_id': owner.user_id,
                    'name': owner.name,
                    'email': owner.user.email if owner.user else None,
                    'mobile': owner.mobile,
                    'id_type': owner.id_type,
                    'id_number': owner.id_number,
                    'property_address': owner.property_address,
                    'per_state': owner.per_state,
                    'per_district': owner.per_district,
                    'per_pincode': owner.per_pincode,
                    'profile_photo': owner.profile_photo,
                    'created_at': owner.created_at.isoformat()
                    if owner.created_at else None,
                    'updated_at': owner.updated_at.isoformat()
                    if owner.updated_at else None
                }
            }),
            200
        )

class OwnerBookingsApi(Resource):

    @auth_required()
    def get(self):

        owner = Owner.query.filter_by(
            user_id=current_user.id
        ).first()

        if not owner:
            return make_response(
                jsonify({
                    'message': 'Owner profile not found.'
                }),
                404
            )

        properties = Property.query.filter_by(
            owner_id=owner.id
        ).all()

        property_ids = [property.id for property in properties]

        if not property_ids:
            return make_response(
                jsonify({
                    'message': 'Bookings fetched successfully.',
                    'bookings': []
                }),
                200
            )

        bookings = Booking.query.filter(
            Booking.property_id.in_(property_ids)
        ).order_by(
            Booking.created_at.desc()
        ).all()

        booking_data = []

        for booking in bookings:

            student_name = None
            student_email = None
            student_mobile = None

            if booking.customer:
                student_name = booking.customer.name
                student_mobile = booking.customer.mobile

                if booking.customer.user:
                    student_email = booking.customer.user.email

            booking_data.append({
                'id': booking.id,
                'property_id': booking.property_id,
                'property_name': booking.property.name
                    if booking.property else None,

                'room_id': booking.room_id,
                'room_number': booking.room.room_number
                    if booking.room else None,

                'student_name': student_name,
                'student_email': student_email,
                'student_mobile': student_mobile,

                'check_in': booking.check_in.isoformat()
                    if booking.check_in else None,

                'check_out': booking.check_out.isoformat()
                    if booking.check_out else None,

                'number_of_guests': booking.number_of_guests,

                'total_amount': float(booking.total_amount)
                    if booking.total_amount is not None else 0,

                'status': booking.status,

                'created_at': booking.created_at.isoformat()
                    if booking.created_at else None
            })

        return make_response(
            jsonify({
                'message': 'Bookings fetched successfully.',
                'bookings': booking_data
            }),
            200
        )


class AmenitiesApi(Resource):

    @auth_required()
    def get(self):
        amenities = Amenity.query.order_by(Amenity.name.asc()).all()

        return make_response(jsonify({
            'message': 'Amenities fetched successfully.',
            'amenities': [
                {'id': item.id, 'name': item.name}
                for item in amenities
            ]
        }), 200)

    @auth_required()
    def post(self):
        if not current_user.has_role('owner'):
            return make_response(
                jsonify({'message': 'Owner access required.'}), 403
            )

        data = request.get_json(silent=True) or {}
        name = data.get('name', '')

        if not isinstance(name, str) or not name.strip():
            return make_response(
                jsonify({'message': 'Amenity name is required.'}), 400
            )

        name = name.strip()
        existing = Amenity.query.filter(
            db.func.lower(Amenity.name) == name.lower()
        ).first()

        if existing:
            return make_response(jsonify({
                'message': 'Amenity already exists.',
                'amenity': {
                    'id': existing.id,
                    'name': existing.name
                }
            }), 200)

        try:
            amenity = Amenity(name=name)
            db.session.add(amenity)
            db.session.commit()

            return make_response(jsonify({
                'message': 'Amenity added successfully.',
                'amenity': {
                    'id': amenity.id,
                    'name': amenity.name
                }
            }), 201)

        except Exception as e:
            db.session.rollback()
            print('AMENITY ERROR:', e)
            return make_response(
                jsonify({'message': 'Failed to add amenity.'}), 500
            )


class OwnerPropertyAmenitiesApi(Resource):

    @auth_required()
    def put(self, property_id):
        # Amenities now belong to individual rooms, not properties.
        return make_response(
            jsonify({
                'message': 'Amenities must be assigned to rooms.'
            }),
            410
        )


class OwnerPropertyRoomApi(Resource):

    @auth_required()
    def post(self, property_id):

        owner = Owner.query.filter_by(user_id=current_user.id).first()

        if not owner:
            return make_response(
                jsonify({'message': 'Owner profile not found.'}),404)

        property = Property.query.filter_by(id=property_id,owner_id=owner.id).first()

        if not property:
            return make_response(
                jsonify({'message': 'Property not found.'}),404)

        data = request.get_json()

        if not data:
            return make_response(
                jsonify({'message': 'Room data is required.'}),400)

        required_fields = [
            'room_number',
            'room_type',
            'capacity',
            'price_per_night'
        ]

        for field in required_fields:
            if data.get(field) is None or str(data.get(field)).strip() == '':
                return make_response(
                    jsonify({
                        'message': f'{field} is required.'
                    }),
                    400
                )

        amenity_ids, amenity_error = validate_amenity_ids(
            data.get('amenities', [])
        )
        if amenity_error:
            return make_response(jsonify({'message': amenity_error}), 400)

        try:
            room = Room(
                property_id=property.id,
                room_number=str(data.get('room_number')).strip(),
                room_type=str(data.get('room_type')).strip(),
                capacity=int(data.get('capacity')),
                price_per_night=float(data.get('price_per_night')),
                available=data.get('available', True),
                amenities=amenity_ids
            )

            db.session.add(room)
            db.session.commit()

            return make_response(
                jsonify({
                    'message': 'Room added successfully.',
                    'room': {
                        'id': room.id,
                        'property_id': room.property_id,
                        'room_number': room.room_number,
                        'room_type': room.room_type,
                        'capacity': room.capacity,
                        'price_per_night': room.price_per_night,
                        'available': room.available,
                        'amenities': [
                            {'id': item.id, 'name': item.name}
                            for item in Amenity.query.filter(
                                Amenity.id.in_(room.amenities or [])
                            ).all()
                        ] if room.amenities else []
                    }
                }),
                201
            )

        except (ValueError, TypeError):
            db.session.rollback()

            return make_response(
                jsonify({
                    'message': 'Invalid room data.'
                }),
                400
            )

        except Exception as e:
            db.session.rollback()

            return make_response(
                jsonify({
                    'message': 'Failed to add room.',
                    'error': str(e)
                }),
                500
            )

    @auth_required()
    def put(self, property_id, room_id):

        owner = Owner.query.filter_by(
            user_id=current_user.id
        ).first()

        if not owner:
            return make_response(
                jsonify({
                    'message': 'Owner profile not found.'
                }),
                404
            )

        property = Property.query.filter_by(
            id=property_id,
            owner_id=owner.id
        ).first()

        if not property:
            return make_response(
                jsonify({
                    'message': 'Property not found.'
                }),
                404
            )

        room = Room.query.filter_by(
            id=room_id,
            property_id=property.id
        ).first()

        if not room:
            return make_response(
                jsonify({
                    'message': 'Room not found.'
                }),
                404
            )

        data = request.get_json()

        if not data:
            return make_response(
                jsonify({
                    'message': 'Room data is required.'
                }),
                400
            )

        required_fields = [
            'room_number',
            'room_type',
            'capacity',
            'price_per_night'
        ]

        for field in required_fields:
            if data.get(field) is None or str(data.get(field)).strip() == '':
                return make_response(
                    jsonify({
                        'message': f'{field} is required.'
                    }),
                    400
                )

        try:
            room.room_number = str(
                data.get('room_number')
            ).strip()

            room.room_type = str(
                data.get('room_type')
            ).strip()

            room.capacity = int(
                data.get('capacity')
            )

            room.price_per_night = float(
                data.get('price_per_night')
            )

            room.available = data.get(
                'available',
                True
            )

            if 'amenities' in data:
                amenity_ids, amenity_error = validate_amenity_ids(
                    data.get('amenities')
                )
                if amenity_error:
                    db.session.rollback()
                    return make_response(
                        jsonify({'message': amenity_error}), 400
                    )
                room.amenities = amenity_ids

            db.session.commit()

            return make_response(
                jsonify({
                    'message': 'Room updated successfully.',
                    'room': {
                        'id': room.id,
                        'property_id': room.property_id,
                        'room_number': room.room_number,
                        'room_type': room.room_type,
                        'capacity': room.capacity,
                        'price_per_night': room.price_per_night,
                        'available': room.available,
                        'amenities': [
                            {'id': item.id, 'name': item.name}
                            for item in Amenity.query.filter(
                                Amenity.id.in_(room.amenities or [])
                            ).all()
                        ] if room.amenities else []
                    }
                }),
                200
            )

        except (ValueError, TypeError):
            db.session.rollback()

            return make_response(
                jsonify({
                    'message': 'Invalid room data.'
                }),
                400
            )

        except Exception as e:
            db.session.rollback()

            return make_response(
                jsonify({
                    'message': 'Failed to update room.',
                    'error': str(e)
                }),
                500
            )

    @auth_required()
    def delete(self, property_id, room_id):

        owner = Owner.query.filter_by(
            user_id=current_user.id
        ).first()

        if not owner:
            return make_response(
                jsonify({
                    'message': 'Owner profile not found.'
                }),
                404
            )

        property = Property.query.filter_by(
            id=property_id,
            owner_id=owner.id
        ).first()

        if not property:
            return make_response(
                jsonify({
                    'message': 'Property not found.'
                }),
                404
            )

        room = Room.query.filter_by(
            id=room_id,
            property_id=property.id
        ).first()

        if not room:
            return make_response(
                jsonify({
                    'message': 'Room not found.'
                }),
                404
            )

        try:
            db.session.delete(room)
            db.session.commit()

            return make_response(
                jsonify({
                    'message': 'Room deleted successfully.'
                }),
                200
            )

        except Exception as e:
            db.session.rollback()

            return make_response(
                jsonify({
                    'message': 'Failed to delete room.',
                    'error': str(e)
                }),
                500
            )