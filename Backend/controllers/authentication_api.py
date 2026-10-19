from flask_restful import Resource
from flask import request,jsonify,make_response
from flask_security import utils,auth_token_required

from controllers.user_database import user_datastore
from controllers.model import Customer,Owner
from controllers.database import db
from datetime import datetime

class LoginApi(Resource):
    def post(self):
        login_credentials = request.get_json()

        if not login_credentials:
            result = {
                'message': 'Login credential are required.'    
            }
            return make_response(jsonify(result), 400)

        email = login_credentials.get('email',None)
        password = login_credentials.get('password',None)

        if not email or not password:
            result = {
                'message':'Email and Password required.'                
            }
            return make_response(jsonify(result),400)
        user = user_datastore.find_user(email=email)

        if not user:
            result = {
                'message':'User not found.'
            }
            return make_response(jsonify(result),404)

        if not utils.verify_password(password, user.password):
            result = {
                'message':'Invalid Password.'
            }
            return make_response(jsonify(result),401)

        auth_token = user.get_auth_token()

        utils.login_user(user)

        response = {
            'message':'Login successful',
            'user_details':{
                'user_id':user.id,
                'email':user.email,
                'roles':[role.name for role in user.roles],
                'auth_token': auth_token
            }
        }
        return make_response(jsonify(response), 200)

class LogoutApi(Resource):
    def post(self):
        utils.logout_user()

        response = {
            'message':'logout successfully'
        }
        return make_response(jsonify(response),200)

    
class StudentRegisterApi(Resource):
    def post(self):
        creds = request.get_json()

        if not creds:
            result = {
                'message': 'Please fill the required blanks'
            }
            return make_response(jsonify(result), 400)

        email = creds.get('email')
        password = creds.get('password')
        role_name = creds.get('role')

        name = creds.get('name')
        dob = creds.get('dob')
        gender = creds.get('gender')
        mobile = creds.get('mobile')
        alternate_mobile = creds.get('alternate_mobile')

        id_type = creds.get('id_type')
        id_number = creds.get('id_number')

        cor_address = creds.get('cor_address')
        cor_state = creds.get('cor_state')
        cor_district = creds.get('cor_district')
        cor_pincode = creds.get('cor_pincode')

        per_address = creds.get('per_address')
        per_state = creds.get('per_state')
        per_district = creds.get('per_district')
        per_pincode = creds.get('per_pincode')

        student_id = creds.get('student_id')
        college_name = creds.get('college_name')
        course = creds.get('course')

        if not email or not password:
            result = {
                'message': 'Email and password required'
            }
            return make_response(jsonify(result), 400)

        if role_name != 'customer':
            result = {
                'message': 'Invalid role for student registration'
            }
            return make_response(jsonify(result), 400)

        

        if user_datastore.find_user(email=email):
            result = {
                'message': 'User already Exist'
            }
            return make_response(jsonify(result), 409)

        try:
            dob = datetime.strptime(dob, '%Y-%m-%d')
        except (ValueError, TypeError):
            result = {
                'message': 'Invalid date of birth'
            }
            return make_response(jsonify(result), 400)

        if dob > datetime.now():
            result = {
                'message': 'Date of birth cannot be in the future'
            }
            return make_response(jsonify(result), 400)

        required_fields = {
            'name': name,
            'dob': dob,
            'gender': gender,
            'mobile': mobile,
            'id_type': id_type,
            'id_number': id_number,
            'cor_address': cor_address,
            'cor_state': cor_state,
            'cor_district': cor_district,
            'cor_pincode': cor_pincode,
            'per_state': per_state,
            'per_district': per_district,
            'per_pincode': per_pincode
        }

        for field, value in required_fields.items():
            if not value:
                result = {
                    'message': f'{field} is required'
                }
                return make_response(jsonify(result), 400)

        role = user_datastore.find_role(role_name)

        if not role:
            result = {
                'message': 'Customer role does not exist'
            }
            return make_response(jsonify(result), 400)

        user = user_datastore.create_user(
            email=email,
            password=password,
            roles=[role]
        )

        db.session.add(user)
        db.session.flush()

        customer = Customer(
            user_id=user.id,
            name=name,
            dob=dob,
            gender=gender,
            mobile=mobile,
            alternate_mobile=alternate_mobile,
            id_type=id_type,
            id_number=id_number,
            cor_address=cor_address,
            cor_state=cor_state,
            cor_district=cor_district,
            cor_pincode=cor_pincode,
            per_address=per_address,
            per_state=per_state,
            per_district=per_district,
            per_pincode=per_pincode,
            student_id=student_id,
            college_name=college_name,
            course=course
        )

        db.session.add(customer)
        db.session.commit()

        response = {
            'message': 'Student registration successful',
            'user_details': {
                'id': user.id,
                'email': email,
                'role': [r.name for r in user.roles]
            },
            'student_details': {
                'id': customer.id,
                'name': customer.name,
                'mobile': customer.mobile,
                'student_id': customer.student_id,
                'college_name': customer.college_name,
                'course': customer.course
            }
        }

        return make_response(jsonify(response), 201)

class OwnerRegisterApi(Resource):
    def post(self):
        creds = request.get_json()

        if not creds:
            result = {
                'message': 'Please fill the required blanks'
            }
            return make_response(jsonify(result), 400)

        email = creds.get('email')
        password = creds.get('password')
        role_name = creds.get('role')

        name = creds.get('name')
        mobile = creds.get('mobile')

        id_type = creds.get('id_type')
        id_number = creds.get('id_number')

        property_address = creds.get('property_address')
        per_state = creds.get('per_state')
        per_district = creds.get('per_district')
        per_pincode = creds.get('per_pincode')

        if not email or not password:
            result = {
                'message': 'Email and password required'
            }
            return make_response(jsonify(result), 400)

        if role_name != 'owner':
            result = {
                'message': 'Invalid role for owner registration'
            }
            return make_response(jsonify(result), 400)

        if user_datastore.find_user(email=email):
            result = {
                'message': 'User already Exist'
            }
            return make_response(jsonify(result), 409)

        required_fields = {
            'name': name,
            'mobile': mobile,
            'id_type': id_type,
            'id_number': id_number,
            'property_address': property_address,
            'per_state': per_state,
            'per_district': per_district,
            'per_pincode': per_pincode
        }

        for field, value in required_fields.items():
            if not value:
                result = {
                    'message': f'{field} is required'
                }
                return make_response(jsonify(result), 400)

        role = user_datastore.find_role(role_name)

        if not role:
            result = {
                'message': 'Owner role does not exist'
            }
            return make_response(jsonify(result), 400)

        user = user_datastore.create_user(
            email=email,
            password=password,
            roles=[role]
        )

        db.session.add(user)
        db.session.flush()

        owner = Owner(
            user_id=user.id,
            name=name,
            mobile=mobile,
            id_type=id_type,
            id_number=id_number,
            property_address=property_address,
            per_state=per_state,
            per_district=per_district,
            per_pincode=per_pincode
        )

        db.session.add(owner)
        db.session.commit()

        response = {
            'message': 'Owner registration successful',
            'user_details': {
                'id': user.id,
                'email': email,
                'role': [r.name for r in user.roles]
            },
            'owner_details': {
                'id': owner.id,
                'name': owner.name,
                'mobile': owner.mobile,
                'id_type': owner.id_type,
                'property_address': owner.property_address,
                'per_state': owner.per_state,
                'per_district': owner.per_district,
                'per_pincode': owner.per_pincode
            }
        }

        return make_response(jsonify(response), 201)
