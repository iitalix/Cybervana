from flask import Blueprint, request
from ..models import Vehicle, Review, User, db
from random import choice, sample
from datetime import date
from flask_login import login_required, current_user
from ..forms import VehicleForm, UpdateVehicleForm, ReviewForm
from .aws_helpers import upload_file_to_s3, get_unique_filename, remove_file_from_s3
from .auth_routes import validation_errors_to_error_messages

vehicles_routes = Blueprint('vehicles', __name__)

# retrieves vehicles for All Vehicles Page
@vehicles_routes.route('/all')
def all():
    """GET all vehicles for the purposes of shopping"""

    all_vehicles = Vehicle.query.all()

    return [vehicle.to_dict() for vehicle in all_vehicles]


# retrieves Vehicles owned by logged in user
@vehicles_routes.route('/current')
@login_required
def current():
    """GET all vehicles owned by current user"""

    all_user_vehicles = Vehicle.query.filter_by(owner_id=current_user.id).all()

    return [vehicle.to_dict() for vehicle in all_user_vehicles]

# retrieves and posts new Vehicle
@vehicles_routes.route('/new', methods=['GET', 'POST'])
@login_required
def new_vehicle():
    form = VehicleForm()

    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        image = form.data["image"]
        image.filename = get_unique_filename(image.filename)
        upload = upload_file_to_s3(image)
        url = upload['url']

        vehicle = Vehicle(
            owner_id = current_user.id,
            make = form.data['make'],
            model = form.data['model'],
            price = form.data['price'],
            photo_url = url,
            description = form.data['description'],
            created_at = date.today()
        )

        db.session.add(vehicle)
        db.session.commit()

        return {"resPost": vehicle.to_dict()}

    return {'errors': validation_errors_to_error_messages(form.errors)}, 400


# updates vehicle through form
@vehicles_routes.route("/update/<int:id>", methods=["PUT"])
@login_required
def update_vehicle(id):
    vehicle_to_update = Vehicle.query.get(id)
    form = UpdateVehicleForm()

    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():

        vehicle_make=form.data['make']
        vehicle_model=form.data['model']
        vehicle_price=form.data['price']
        vehicle_description=form.data['description']

        vehicle_to_update.make=vehicle_make
        vehicle_to_update.model=vehicle_model
        vehicle_to_update.price=vehicle_price
        vehicle_to_update.description=vehicle_description

        db.session.commit()

        return {"updated": "updated"}

    return {'errors': validation_errors_to_error_messages(form.errors)}, 400

# deletes vehicle by ID
@vehicles_routes.route('/delete/<int:id>', methods=['DELETE'])
@login_required
def delete_vehicles(id):
    vehicle_to_delete = Vehicle.query.get(id)
    if id < 31:
        db.session.delete(vehicle_to_delete)
        db.session.commit()
        return 'Success, your vehicle was deleted.'

    elif id > 30:

        file_delete = remove_file_from_s3(vehicle_to_delete.photo_url)

        db.session.delete(vehicle_to_delete)
        db.session.commit()
        return 'Success, your vehicle was deleted.'
    else:
        return {"Error": "Vehicle Delete Error, please try again"}


# retrieves vehicle details by ID
@vehicles_routes.route('/<int:id>')
@login_required
def get_vehicle_details(id):
    vehicle = Vehicle.query.get(id)

    return vehicle.to_dict()



@vehicles_routes.route('/<int:id>/reviews/', methods=["vehicle"])
@login_required
def create_comment(id):
    form = ReviewForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        data = form.data
        create_review = Review(
            user_id=current_user.id,
            vehicle_id=id,
            comment=data['review'],
            created_at=date.today()
        )

        db.session.add(create_review)
        db.session.commit()

        return create_comment.to_dict()

    return {'errors': validation_errors_to_error_messages(form.errors)}, 400


@vehicles_routes.route('/<int:id>/reviews', methods=["PUT"])
@login_required
def update_comment():
    form = ReviewForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():

        data = form.data
        create_review = Review(
            user_id=current_user.id,
            vehicle_id=id,
            comment=data['review'],
            created_at=date.today()
        )

        db.session.add(create_review)
        db.session.commit()

        return create_review.to_dict()

    return {'errors': validation_errors_to_error_messages(form.errors)}, 400


@vehicles_routes.route('/<int:id>/')
def vehicle_by_id():
    """Get vehicle by vehicle ID to show on vehicle Details Page (when user clicks on a photo vehicle)"""
    vehicle_to_get = Vehicle.query.get(id)

    return vehicle_to_get.to_dict()
