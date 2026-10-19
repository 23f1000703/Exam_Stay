from flask_restful import Resource
from flask import request,jsonify,make_response
from flask_security import utils,auth_token_required
from flask_security import auth_required, current_user

from controllers.user_database import user_datastore
from controllers.model import Customer, Owner, Property, Booking ,User, Complaint, Amenity
from controllers.database import db

class AdminDashboard(Resource):
    def get(self):

        total_students = Customer.query.count()
        total_owners = Owner.query.count()
        total_properties = Property.query.count()
        total_bookings = Booking.query.count()
        pending_owner_verification = Property.query.filter_by(
            verification_status='pending'
        ).count()
        print("Total Students:", total_students)
        print("Total Owners:", total_owners)
        print("Total Properties:", total_properties)
        print("Total Bookings:", total_bookings)
        print("Pending Owner Verification:", pending_owner_verification)

        return jsonify({
            "total_students": total_students,
            "total_owners": total_owners,
            "total_properties": total_properties,
            "total_bookings": total_bookings,
            "pending_owner_verification": pending_owner_verification
        })


class AdminStudentsApi(Resource):

    @auth_required()
    def get(self):

        if not current_user.has_role('admin'):
            return make_response(
                jsonify({
                    'message': 'Admin access required.'
                }),
                403
            )

        search = request.args.get(
            'search',
            ''
        ).strip().lower()

        customers = Customer.query.order_by(
            Customer.id.desc()
        ).all()

        students = []

        for customer in customers:

            name = customer.name or ''
            email = (
                customer.user.email
                if customer.user
                else ''
            )
            mobile = customer.mobile or ''
            college = customer.college_name or ''
            student_id = customer.student_id or ''

            if search:

                search_text = ' '.join([
                    name,
                    email,
                    mobile,
                    college,
                    student_id
                ]).lower()

                if search not in search_text:
                    continue

            students.append({
                'id': customer.id,
                'user_id': customer.user_id,
                'name': customer.name,
                'email': email,
                'mobile': customer.mobile,
                'college_name': customer.college_name,
                'course': customer.course,
                'student_id': customer.student_id,
                'profile_photo': customer.profile_photo,
                'created_at': (
                    customer.created_at.isoformat()
                    if customer.created_at
                    else None
                )
            })

            if len(students) == 20:
                break

        return make_response(
            jsonify({
                'message': 'Students fetched successfully.',
                'students': students
            }),
            200
        )

class AdminStudentDetailApi(Resource):

    @auth_required()
    def get(self, student_id):

        if not current_user.has_role('admin'):
            return make_response(
                jsonify({'message': 'Admin access required.'}),
                403
            )

        customer = Customer.query.filter_by(id=student_id).first()

        if not customer:
            return make_response(
                jsonify({'message': 'Student not found.'}),
                404
            )

        bookings = Booking.query.filter_by(
            customer_id=customer.id
        ).order_by(
            Booking.created_at.desc()
        ).all()

        booking_list = []

        for booking in bookings:

            booking_list.append({
                'booking_id': booking.id,

                'property': {
                    'id': booking.property.id if booking.property else None,
                    'name': booking.property.name if booking.property else None,
                    'address': booking.property.address if booking.property else None,
                    'city': booking.property.city if booking.property else None,
                    'district': booking.property.district if booking.property else None,
                    'state': booking.property.state if booking.property else None,
                    'pincode': booking.property.pincode if booking.property else None
                },

                'room': {
                    'id': booking.room.id if booking.room else None,
                    'room_number': booking.room.room_number if booking.room else None,
                    'room_type': booking.room.room_type if booking.room else None,
                    'price_per_night': (
                        booking.room.price_per_night
                        if booking.room else None
                    )
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

                'booking_status': booking.status,

                'payment': {
                    'amount': (
                        booking.payment.amount
                        if booking.payment else None
                    ),
                    'method': (
                        booking.payment.payment_method
                        if booking.payment else None
                    ),
                    'transaction_id': (
                        booking.payment.transaction_id
                        if booking.payment else None
                    ),
                    'status': (
                        booking.payment.status
                        if booking.payment else None
                    ),
                    'paid_at': (
                        booking.payment.paid_at.isoformat()
                        if booking.payment and booking.payment.paid_at
                        else None
                    )
                },

                'booked_at': (
                    booking.created_at.isoformat()
                    if booking.created_at else None
                )
            })

        return make_response(
            jsonify({
                'message': 'Student details fetched successfully.',

                'student': {
                    'id': customer.id,
                    'name': customer.name,
                    'email': customer.user.email if customer.user else None,
                    'mobile': customer.mobile,
                    'college_name': customer.college_name,
                    'course': customer.course,
                    'student_id': customer.student_id,
                    'profile_photo': customer.profile_photo
                },

                'booking_summary': {
                    'total_bookings': len(bookings),
                    'confirmed': sum(
                        1 for b in bookings if b.status == 'confirmed'
                    ),
                    'pending': sum(
                        1 for b in bookings if b.status == 'pending'
                    ),
                    'cancelled': sum(
                        1 for b in bookings if b.status == 'cancelled'
                    ),
                    'completed': sum(
                        1 for b in bookings if b.status == 'completed'
                    )
                },

                'bookings': booking_list
            }),
            200
        )

class AdminPropertiesApi(Resource):

    @auth_required()
    def get(self):

        if not current_user.has_role('admin'):
            return make_response(
                jsonify({'message': 'Admin access required.'}),
                403
            )

        search = request.args.get('search', '').strip().lower()
        status = request.args.get('status', '').strip().lower()

        properties = Property.query.order_by(
            Property.created_at.desc()
        ).all()

        property_list = []

        for prop in properties:

            owner = prop.owner
            owner_name = owner.name if owner else ''
            owner_email = (
                owner.user.email
                if owner and owner.user else ''
            )

            search_text = ' '.join([
                prop.name or '',
                prop.address or '',
                prop.city or '',
                prop.district or '',
                prop.state or '',
                owner_name,
                owner_email
            ]).lower()

            if search and search not in search_text:
                continue

            if status and prop.verification_status.lower() != status:
                continue

            property_list.append({
                'id': prop.id,
                'name': prop.name,
                'address': prop.address,
                'city': prop.city,
                'district': prop.district,
                'state': prop.state,
                'pincode': prop.pincode,
                'verification_status': prop.verification_status,

                'owner': {
                    'id': owner.id if owner else None,
                    'name': owner.name if owner else None,
                    'email': owner_email or None,
                    'mobile': owner.mobile if owner else None
                },

                'room_count': len(prop.rooms),
                'image_count': len(prop.images),

                'created_at': (
                    prop.created_at.isoformat()
                    if prop.created_at else None
                )
            })
            print("Property:", prop.name, "Owner:", owner_name, "Email:", owner_email)

        return make_response(
            jsonify({
                'message': 'Properties fetched successfully.',
                'total_properties': len(property_list),
                'properties': property_list
            }),
            200
        )

class AdminPropertyDetailApi(Resource):

    @auth_required()
    def get(self, property_id):

        if not current_user.has_role('admin'):
            return make_response(
                jsonify({'message': 'Admin access required.'}),
                403
            )

        prop = Property.query.filter_by(
            id=property_id
        ).first()

        if not prop:
            return make_response(
                jsonify({'message': 'Property not found.'}),
                404
            )

        owner = prop.owner

        bookings = Booking.query.filter_by(
            property_id=prop.id
        ).order_by(
            Booking.created_at.desc()
        ).all()

        return make_response(
            jsonify({
                'message': 'Property details fetched successfully.',

                'property': {
                    'id': prop.id,
                    'name': prop.name,
                    'description': prop.description,
                    'address': prop.address,
                    'city': prop.city,
                    'district': prop.district,
                    'state': prop.state,
                    'pincode': prop.pincode,
                    'latitude': prop.latitude,
                    'longitude': prop.longitude,
                    'verification_status': prop.verification_status,

                    'created_at': (
                        prop.created_at.isoformat()
                        if prop.created_at else None
                    ),
                    'updated_at': (
                        prop.updated_at.isoformat()
                        if prop.updated_at else None
                    )
                },

                'owner': {
                    'id': owner.id if owner else None,
                    'user_id': owner.user_id if owner else None,
                    'name': owner.name if owner else None,
                    'email': (
                        owner.user.email
                        if owner and owner.user else None
                    ),
                    'mobile': owner.mobile if owner else None,
                    'property_address': (
                        owner.property_address if owner else None
                    )
                } if owner else None,

                'rooms': [
                        {
                            'id': room.id,
                            'room_number': room.room_number,
                            'room_type': room.room_type,
                            'capacity': room.capacity,
                            'price_per_night': room.price_per_night,
                            'available': room.available,

                            'amenities': [
                                {
                                    'id': amenity.id,
                                    'name': amenity.name
                                }
                                for amenity in Amenity.query.filter(
                                    Amenity.id.in_(room.amenities or [])
                                ).all()
                            ]
                        }
                        for room in prop.rooms
                    ],

                'images': [
                    {
                        'id': image.id,
                        'image_url': image.image_url,
                        'is_primary': image.is_primary
                    }
                    for image in prop.images
                ],


                'booking_summary': {
                    'total_bookings': len(bookings),
                    'pending': sum(
                        1 for b in bookings if b.status == 'pending'
                    ),
                    'confirmed': sum(
                        1 for b in bookings if b.status == 'confirmed'
                    ),
                    'cancelled': sum(
                        1 for b in bookings if b.status == 'cancelled'
                    ),
                    'completed': sum(
                        1 for b in bookings if b.status == 'completed'
                    )
                },

                'bookings': [
                    {
                        'id': booking.id,
                        'customer_id': booking.customer_id,
                        'student_name': (
                            booking.customer.name
                            if booking.customer else None
                        ),
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
                    }
                    for booking in bookings
                ]
            }),
            200
        )
    
    
    @auth_required()
    def put(self, property_id):

        if not current_user.has_role('admin'):
            return make_response(
                jsonify({'message': 'Admin access required.'}),
                403
            )

        prop = Property.query.filter_by(id=property_id).first()

        if not prop:
            return make_response(
                jsonify({'message': 'Property not found.'}),
                404
            )

        if (prop.verification_status or '').lower() != 'pending':
            return make_response(
                jsonify({
                    'message': 'Only pending properties can be verified.',
                    'verification_status': prop.verification_status
                }),
                400
            )

        try:
            prop.verification_status = 'verified'
            db.session.commit()

            return make_response(
                jsonify({
                    'message': 'Property verified successfully.',
                    'property': {
                        'id': prop.id,
                        'verification_status': prop.verification_status
                    }
                }),
                200
            )

        except Exception:
            db.session.rollback()
            return make_response(
                jsonify({'message': 'Failed to verify property.'}),
                500
            )



class AdminBookingsApi(Resource):

    @auth_required()
    def get(self):

        if not current_user.has_role('admin'):
            return make_response(
                jsonify({'message': 'Admin access required.'}),
                403
            )

        search = request.args.get('search', '').strip().lower()
        status_filter = request.args.get('status', '').strip().lower()

        all_bookings = Booking.query.order_by(
            Booking.created_at.desc()
        ).all()

        booking_list = []

        for booking in all_bookings:
            student = booking.customer
            prop = booking.property
            room = booking.room
            payment = booking.payment

            student_name = student.name if student else ''
            student_email = (
                student.user.email
                if student and student.user else ''
            )
            student_mobile = student.mobile if student else ''

            property_name = prop.name if prop else ''
            room_number = room.room_number if room else ''

            booking_status = (booking.status or '').lower()

            # Filter by booking status
            if status_filter and booking_status != status_filter:
                continue

            # Search by student name, property name,
            # email, booking ID, and room number
            search_text = ' '.join([
                str(booking.id),
                student_name or '',
                student_email or '',
                property_name or '',
                str(room_number or '')
            ]).lower()

            if search and search not in search_text:
                continue

            booking_list.append({
                'id': booking.id,

                # Student information
                'student': {
                    'id': student.id if student else None,
                    'name': student_name or 'N/A',
                    'email': student_email or None,
                    'mobile': student_mobile or None,
                    'college_name': (
                        student.college_name if student else None
                    ),
                    'course': student.course if student else None
                } if student else None,

                # Property information
                'property': {
                    'id': prop.id if prop else None,
                    'name': property_name or 'N/A',
                    'address': prop.address if prop else None,
                    'city': prop.city if prop else None,
                    'district': prop.district if prop else None,
                    'state': prop.state if prop else None,
                    'pincode': prop.pincode if prop else None
                } if prop else None,

                # Room information
                'room': {
                    'id': room.id if room else None,
                    'room_number': room.room_number,
                    'room_type': room.room_type,
                    'capacity': room.capacity,
                    'price_per_night': (
                        float(room.price_per_night)
                        if room.price_per_night is not None else None
                    )
                } if room else None,

                # Booking information
                'check_in': (
                    booking.check_in.isoformat()
                    if booking.check_in else None
                ),
                'check_out': (
                    booking.check_out.isoformat()
                    if booking.check_out else None
                ),
                'number_of_guests': booking.number_of_guests,
                'total_amount': (
                    float(booking.total_amount)
                    if booking.total_amount is not None else None
                ),
                'status': booking.status,

                # Payment information
                'payment': {
                    'amount': (
                        float(payment.amount)
                        if payment and payment.amount is not None
                        else None
                    ),
                    'payment_method': (
                        payment.payment_method if payment else None
                    ),
                    'transaction_id': (
                        payment.transaction_id if payment else None
                    ),
                    'status': (
                        payment.status if payment else 'unpaid'
                    ),
                    'paid_at': (
                        payment.paid_at.isoformat()
                        if payment and payment.paid_at else None
                    )
                } if payment else {
                    'amount': None,
                    'payment_method': None,
                    'transaction_id': None,
                    'status': 'unpaid',
                    'paid_at': None
                },

                'created_at': (
                    booking.created_at.isoformat()
                    if booking.created_at else None
                )
            })

        return make_response(
            jsonify({
                'message': 'Bookings fetched successfully.',
                'total_bookings': len(booking_list),
                'bookings': booking_list
            }),
            200
        )


class AdminPendingVerificationsApi(Resource):

    @auth_required()
    def get(self):

        if not current_user.has_role('admin'):
            return make_response(
                jsonify({'message': 'Admin access required.'}),
                403
            )

        search = request.args.get('search', '').strip().lower()

        # Sirf pending properties fetch karo
        query = Property.query.filter_by(
            verification_status='pending'
        ).order_by(Property.created_at.desc())

        pending_properties = query.all()
        property_list = []

        for prop in pending_properties:
            owner = prop.owner

            owner_name = owner.name if owner else ''
            owner_email = (
                owner.user.email
                if owner and owner.user else ''
            )

            search_text = ' '.join([
                prop.name or '',
                prop.address or '',
                prop.city or '',
                prop.district or '',
                prop.state or '',
                prop.pincode or '',
                owner_name,
                owner_email,
                owner.mobile or '' if owner else ''
            ]).lower()

            # Property ya owner ki details se search
            if search and search not in search_text:
                continue

            property_list.append({
                'id': prop.id,
                'name': prop.name,
                'description': prop.description,
                'address': prop.address,
                'city': prop.city,
                'district': prop.district,
                'state': prop.state,
                'pincode': prop.pincode,
                'verification_status': prop.verification_status,

                'owner': {
                    'id': owner.id if owner else None,
                    'name': owner_name or 'N/A',
                    'email': owner_email or 'N/A',
                    'mobile': owner.mobile if owner else None
                } if owner else None,

                'room_count': len(prop.rooms),
                'image_count': len(prop.images),

                'created_at': (
                    prop.created_at.isoformat()
                    if prop.created_at else None
                )
            })

        return make_response(
            jsonify({
                'message': 'Pending verifications fetched successfully.',
                'total_pending': len(property_list),
                'properties': property_list
            }),
            200
        )

class AdminComplaintsApi(Resource):

    @auth_required()
    def get(self):
        if not current_user.has_role('admin'):
            return make_response(
                jsonify({'message': 'Admin access required.'}), 403
            )

        complaint_type = request.args.get('type', 'customer').lower()

        if complaint_type not in ['owner', 'customer']:
            return make_response(
                jsonify({'message': 'Invalid complaint type.'}), 400
            )

        complaints = Complaint.query.order_by(
            Complaint.created_at.desc()
        ).all()

        results = []

        for complaint in complaints:
            user = User.query.get(complaint.user_id)

            if not user:
                continue

            if complaint_type == 'owner':
                if not user.has_role('owner'):
                    continue
                owner = Owner.query.filter_by(user_id=user.id).first()
                complainant_name = owner.name if owner else user.email
            else:
                if not user.has_role('customer'):
                    continue
                customer = Customer.query.filter_by(user_id=user.id).first()
                complainant_name = customer.name if customer else user.email

            results.append({
                'id': complaint.id,
                'complainant_name': complainant_name,
                'email': user.email,
                'subject': complaint.subject,
                'description': complaint.description,
                'status': complaint.status,
                'property_id': complaint.property_id,
                'booking_id': complaint.booking_id,
                'created_at': (
                    complaint.created_at.isoformat()
                    if complaint.created_at else None
                )
            })

        return make_response(jsonify({
            'message': 'Complaints fetched successfully.',
            'complaint_type': complaint_type,
            'total': len(results),
            'complaints': results
        }), 200)