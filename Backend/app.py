from flask import Flask
from flask_security import Security
from flask_restful import Api
from flask_cors import CORS

from controllers.config import Config
from flask import send_from_directory
from controllers.user_database import user_datastore
from controllers.database import db

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    security = Security(app, user_datastore)

    api = Api(app, prefix ="/api")

    with app.app_context():
        db.create_all()

        admin_role = user_datastore.find_or_create_role(name ='admin',description='Admin')
        customer_role = user_datastore.find_or_create_role(name = 'customer',description = 'Customer')
        owner_role = user_datastore.find_or_create_role(name ='owner',description='Owner')

        

        if not user_datastore.find_user(email = 'admin@gmail.com'):
            user_datastore.create_user(
                email = 'admin@gmail.com',
                password = 'admin@12345',
                roles =[admin_role]
            )
            db.session.commit()

        from controllers.model import Amenity

        amenity_names = [
            "Wi-Fi",
            "Air Conditioning",
            "Parking",
            "Attached Bathroom",
            "Geyser",
            "Washing Machine",
            "Refrigerator",
            "TV",
            "Power Backup",
            "CCTV",
            "Security Guard",
            "Housekeeping",
            "Laundry",
            "Lift",
            "RO Water",
            "Water Cooler",
            "Food Included",
            "Kitchen",
            "Study Table",
            "Wardrobe",
            "Bed",
            "Mattress",
            "Fan",
            "Hot Water",
            "Common Area",
            "Balcony",
            "Gym",
            "Fire Safety",
            "Visitor Parking"
        ]

        added_count = 0

        for name in amenity_names:
            existing = Amenity.query.filter(
                db.func.lower(Amenity.name) == name.lower()
            ).first()

            if not existing:
                db.session.add(Amenity(name=name))
                added_count += 1

        db.session.commit()

        print(f"Default amenities added: {added_count}")
        print(f"Total amenities: {Amenity.query.count()}")

    return app,api



            
app, api =create_app()
CORS(app, origins = [
      "http://localhost:5173",
      "http://127.0.0.1:5173"
  ])

@app.route('/')
def index():
    return {
        'message': "this is my app"
    }
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(
        'uploads',
        filename
    )

from controllers.authentication_api import LoginApi,LogoutApi,StudentRegisterApi,OwnerRegisterApi
from controllers.admin import AdminBookingsApi, AdminComplaintsApi, AdminDashboard, AdminPendingVerificationsApi, AdminPropertiesApi, AdminPropertyDetailApi, AdminStudentDetailApi, AdminStudentsApi
from controllers.owner import AmenitiesApi, OwnerDashboardApi, OwnerPropertiesApi, OwnerPropertyAmenitiesApi,OwnerPropertyApi,OwnerPropertyImageApi,OwnerPropertyRoomApi,OwnerProfileApi,OwnerBookingsApi
from controllers.students import StudentBookingHistoryApi, StudentDashboardApi, StudentProfileApi, StudentPropertiesApi,StudentPropertyDetailApi,StudentBookingCreateApi

api.add_resource(LoginApi,'/login')
api.add_resource(LogoutApi,'/logout')
api.add_resource(StudentRegisterApi,'/studentregister')
api.add_resource(OwnerRegisterApi,'/ownerregister')

api.add_resource(AdminDashboard,'/admin/dashboard')
api.add_resource(AdminStudentsApi,'/admin/students')
api.add_resource(AdminStudentDetailApi,'/admin/students/<int:student_id>')
api.add_resource(AdminPropertiesApi,'/admin/properties')
api.add_resource(AdminPropertyDetailApi,'/admin/properties/<int:property_id>')
api.add_resource(AdminBookingsApi,'/admin/bookings')
api.add_resource( AdminPendingVerificationsApi,'/admin/verifications')
api.add_resource(AdminComplaintsApi,'/admin/complaints')


api.add_resource(OwnerDashboardApi,'/owner/dashboard')
api.add_resource(OwnerPropertiesApi,'/owner/properties')
api.add_resource(OwnerPropertyImageApi,'/owner/properties/<int:property_id>/images')
api.add_resource(OwnerPropertyApi,'/owner/properties/<int:property_id>')
api.add_resource(OwnerPropertyRoomApi,'/owner/properties/<int:property_id>/rooms',
    '/owner/properties/<int:property_id>/rooms/<int:room_id>')
api.add_resource(OwnerProfileApi,'/owner/profile')
api.add_resource(OwnerBookingsApi,'/owner/bookings')
api.add_resource(OwnerPropertyAmenitiesApi,'/owner/properties/<int:property_id>/amenities')
api.add_resource(AmenitiesApi, '/amenities')


api.add_resource(StudentDashboardApi,'/student/dashboard')
api.add_resource(StudentPropertiesApi,'/student/properties')
api.add_resource(StudentProfileApi,'/student/profile')
api.add_resource(StudentBookingHistoryApi,'/student/booking-history')
api.add_resource(StudentPropertyDetailApi,'/student/properties/<int:property_id>')
api.add_resource(StudentBookingCreateApi,'/student/bookings')



if __name__ == "__main__":
    app.run(debug=True)