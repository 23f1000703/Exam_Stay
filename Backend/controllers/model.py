from controllers.database import db
from flask_security import UserMixin, RoleMixin
from datetime import datetime
from sqlalchemy import JSON


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(100),unique=True,nullable=False)

    password = db.Column(db.String(255),nullable=False)

    active = db.Column(db.Boolean,default=False)

    fs_uniquifier = db.Column(db.String(255),nullable=False,unique=True)

    fs_token_uniquifier = db.Column(db.String(255),nullable=False,unique=True)

    roles = db.relationship("Role",secondary="user_role",back_populates="users")

    customer = db.relationship("Customer",back_populates="user",uselist=False)

    owner = db.relationship("Owner",back_populates="user",uselist=False)

    verifications = db.relationship("Verification",foreign_keys="Verification.user_id",back_populates="user",cascade="all, delete-orphan")

    notifications = db.relationship("Notification",back_populates="user",cascade="all, delete-orphan")


class Role(db.Model, RoleMixin):
    __tablename__ = "role"

    id = db.Column(db.Integer,primary_key=True)

    name = db.Column(db.String(100),nullable=False,unique=True)

    description = db.Column(db.String(255))

    users = db.relationship("User",secondary="user_role",back_populates="roles")


class UserRole(db.Model):
    __tablename__ = "user_role"

    id = db.Column(db.Integer,primary_key=True)

    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)

    role_id = db.Column(db.Integer,db.ForeignKey("role.id"),nullable=False)

    __table_args__ = (db.UniqueConstraint("user_id","role_id",name="unique_user_role"),)


class Customer(db.Model):
    __tablename__ = "customer"

    id = db.Column(db.Integer,primary_key=True)

    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False,unique=True)

    name = db.Column(db.String(250),nullable=False)

    dob = db.Column(db.DateTime,nullable=False)

    gender = db.Column(db.String(50),nullable=False)

    mobile = db.Column(db.String(20),nullable=False)

    alternate_mobile = db.Column(db.String(20))

    id_type = db.Column(db.String(100),nullable=False)

    id_number = db.Column(db.String(100),nullable=False)

    cor_address = db.Column(db.String(400),nullable=False)

    cor_state = db.Column(db.String(100),nullable=False)

    cor_district = db.Column(db.String(100),nullable=False)

    cor_pincode = db.Column(db.String(10),nullable=False)

    per_address = db.Column(db.String(400))

    per_state = db.Column(db.String(100),nullable=False)

    per_district = db.Column(db.String(100),nullable=False)

    per_pincode = db.Column(db.String(10),nullable=False)

    student_id = db.Column(db.String(100),unique=True)

    college_name = db.Column(db.String(250))

    course = db.Column(db.String(150))

    profile_photo = db.Column(db.String(500))

    created_at = db.Column(db.DateTime,default=datetime.utcnow)

    updated_at = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    user = db.relationship("User",back_populates="customer")

    exam_trips = db.relationship("ExamTrip",back_populates="customer",cascade="all, delete-orphan")

    bookings = db.relationship("Booking",back_populates="customer")

    reviews = db.relationship("Review",back_populates="customer")


class Owner(db.Model):
    __tablename__ = "owner"

    id = db.Column(db.Integer,primary_key=True)

    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False,unique=True)

    name = db.Column(db.String(150),nullable=False)

    mobile = db.Column(db.String(20),nullable=False)

    id_type = db.Column(db.String(100),nullable=False)

    id_number = db.Column(db.String(100),nullable=False)

    property_address = db.Column(db.String(500),nullable=False)

    per_state = db.Column(db.String(100),nullable=False)

    per_district = db.Column(db.String(100),nullable=False)

    per_pincode = db.Column(db.String(10),nullable=False)

    profile_photo = db.Column(db.String(500))

    created_at = db.Column(db.DateTime,default=datetime.utcnow)

    updated_at = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    user = db.relationship("User",back_populates="owner")

    properties = db.relationship("Property",back_populates="owner",cascade="all, delete-orphan")

    bank_account = db.relationship("BankAccount",back_populates="owner",uselist=False,cascade="all, delete-orphan")


class Verification(db.Model):
    __tablename__ = "verification"

    id = db.Column(db.Integer,primary_key=True)

    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)

    verification_type = db.Column(db.String(100),nullable=False)

    status = db.Column(db.String(50),default="pending",nullable=False)

    document_url = db.Column(db.String(500))

    remarks = db.Column(db.String(500))

    verified_at = db.Column(db.DateTime)

    verified_by = db.Column(db.Integer,db.ForeignKey("user.id"))

    created_at = db.Column(db.DateTime,default=datetime.utcnow)

    user = db.relationship("User",foreign_keys=[user_id],back_populates="verifications")


class Property(db.Model):
    __tablename__ = "property"

    id = db.Column(db.Integer,primary_key=True)

    owner_id = db.Column(db.Integer,db.ForeignKey("owner.id"),nullable=False)

    name = db.Column(db.String(250),nullable=False)

    description = db.Column(db.Text)

    address = db.Column(db.String(500),nullable=False)

    city = db.Column(db.String(100),nullable=False)

    district = db.Column(db.String(100),nullable=False)

    state = db.Column(db.String(100),nullable=False)

    pincode = db.Column(db.String(10),nullable=False)

    latitude = db.Column(db.Float)

    longitude = db.Column(db.Float)

    verification_status = db.Column(db.String(50),default="pending",nullable=False)

    created_at = db.Column(db.DateTime,default=datetime.utcnow)

    updated_at = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    owner = db.relationship("Owner",back_populates="properties")

    rooms = db.relationship("Room",back_populates="property",cascade="all, delete-orphan")

    images = db.relationship("PropertyImage",back_populates="property",cascade="all, delete-orphan")

    bookings = db.relationship("Booking",back_populates="property")

    reviews = db.relationship("Review",back_populates="property")

    complaints = db.relationship("Complaint",back_populates="property")


class Room(db.Model):
    __tablename__ = "room"

    id = db.Column(db.Integer,primary_key=True)

    property_id = db.Column(db.Integer,db.ForeignKey("property.id"),nullable=False)

    room_number = db.Column(db.String(50))

    room_type = db.Column(db.String(100),nullable=False)

    capacity = db.Column(db.Integer,nullable=False)

    price_per_night = db.Column(db.Float,nullable=False)

    available = db.Column(db.Boolean,default=True)

    amenities = db.Column(JSON, default=list, nullable=False)

    property = db.relationship("Property",back_populates="rooms")

    bookings = db.relationship("Booking",back_populates="room")


class Amenity(db.Model):
    __tablename__ = "amenity"

    id = db.Column(db.Integer,primary_key=True)

    name = db.Column(db.String(100),nullable=False,unique=True)




class PropertyImage(db.Model):
    __tablename__ = "property_image"

    id = db.Column(db.Integer,primary_key=True)

    property_id = db.Column(db.Integer,db.ForeignKey("property.id"),nullable=False)

    image_url = db.Column(db.String(500),nullable=False)

    is_primary = db.Column(db.Boolean,default=False)

    property = db.relationship("Property",back_populates="images")



class ExamTrip(db.Model):
    __tablename__ = "exam_trip"

    id = db.Column(db.Integer,primary_key=True)

    customer_id = db.Column(db.Integer,db.ForeignKey("customer.id"),nullable=False)

    exam_name = db.Column(db.String(250),nullable=False)

    exam_city = db.Column(db.String(100),nullable=False)

    exam_centre = db.Column(db.String(300),nullable=False)

    exam_date = db.Column(db.DateTime,nullable=False)

    check_in = db.Column(db.DateTime,nullable=False)

    check_out = db.Column(db.DateTime,nullable=False)

    budget = db.Column(db.Float)

    created_at = db.Column(db.DateTime,default=datetime.utcnow)

    customer = db.relationship("Customer",back_populates="exam_trips")


class Booking(db.Model):
    __tablename__ = "booking"

    id = db.Column(db.Integer,primary_key=True)

    customer_id = db.Column(db.Integer,db.ForeignKey("customer.id"),nullable=False)

    property_id = db.Column(db.Integer,db.ForeignKey("property.id"),nullable=False)

    room_id = db.Column(db.Integer,db.ForeignKey("room.id"),nullable=False)

    check_in = db.Column(db.DateTime,nullable=False)

    check_out = db.Column(db.DateTime,nullable=False)

    number_of_guests = db.Column(db.Integer,default=1)

    total_amount = db.Column(db.Float,nullable=False)

    status = db.Column(db.String(50),default="pending",nullable=False)

    created_at = db.Column(db.DateTime,default=datetime.utcnow)

    customer = db.relationship("Customer",back_populates="bookings")

    property = db.relationship("Property",back_populates="bookings")

    room = db.relationship("Room",back_populates="bookings")

    payment = db.relationship("Payment",back_populates="booking",uselist=False,cascade="all, delete-orphan")

    review = db.relationship("Review",back_populates="booking",uselist=False)


class Payment(db.Model):
    __tablename__ = "payment"

    id = db.Column(db.Integer,primary_key=True)

    booking_id = db.Column(db.Integer,db.ForeignKey("booking.id"),nullable=False,unique=True)

    amount = db.Column(db.Float,nullable=False)

    payment_method = db.Column(db.String(50))

    transaction_id = db.Column(db.String(200),unique=True)

    status = db.Column(db.String(50),default="pending")

    paid_at = db.Column(db.DateTime)

    booking = db.relationship("Booking",back_populates="payment")


class Review(db.Model):
    __tablename__ = "review"

    id = db.Column(db.Integer,primary_key=True)

    customer_id = db.Column(db.Integer,db.ForeignKey("customer.id"),nullable=False)

    property_id = db.Column(db.Integer,db.ForeignKey("property.id"),nullable=False)

    booking_id = db.Column(db.Integer,db.ForeignKey("booking.id"),nullable=False,unique=True)

    rating = db.Column(db.Integer,nullable=False)

    comment = db.Column(db.Text)

    created_at = db.Column(db.DateTime,default=datetime.utcnow)

    customer = db.relationship("Customer",back_populates="reviews")

    property = db.relationship("Property",back_populates="reviews")

    booking = db.relationship("Booking",back_populates="review")


class BankAccount(db.Model):
    __tablename__ = "bank_account"

    id = db.Column(db.Integer,primary_key=True)

    owner_id = db.Column(db.Integer,db.ForeignKey("owner.id"),nullable=False,unique=True)

    account_holder_name = db.Column(db.String(150),nullable=False)

    account_number = db.Column(db.String(50),nullable=False)

    ifsc_code = db.Column(db.String(20),nullable=False)

    bank_name = db.Column(db.String(150),nullable=False)

    owner = db.relationship("Owner",back_populates="bank_account")


class Complaint(db.Model):
    __tablename__ = "complaint"

    id = db.Column(db.Integer,primary_key=True)

    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)

    property_id = db.Column(db.Integer,db.ForeignKey("property.id"))

    booking_id = db.Column(db.Integer,db.ForeignKey("booking.id"))

    subject = db.Column(db.String(250),nullable=False)

    description = db.Column(db.Text,nullable=False)

    status = db.Column(db.String(50),default="open")

    created_at = db.Column(db.DateTime,default=datetime.utcnow)

    resolved_at = db.Column(db.DateTime)

    property = db.relationship("Property",back_populates="complaints")


class Notification(db.Model):
    __tablename__ = "notification"

    id = db.Column(db.Integer,primary_key=True)

    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)

    title = db.Column(db.String(250),nullable=False)

    message = db.Column(db.Text,nullable=False)

    notification_type = db.Column(db.String(100))

    is_read = db.Column(db.Boolean,default=False)

    created_at = db.Column(db.DateTime,default=datetime.utcnow)

    user = db.relationship("User",back_populates="notifications")