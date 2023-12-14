from flask import Blueprint, request
from ..models import Item, db
from flask_login import login_required, current_user
from datetime import date
from .auth_routes import validation_errors_to_error_messages

items_routes = Blueprint('items', __name__)

@items_routes.route('/<int:id>', methods=['POST'])
@login_required
def create_item(id):

    new_form = Item(
        user_id = current_user.id,
        vehicle_id = id,
        created_at = date.today()
    )

    db.session.add(new_form)
    db.session.commit()
    return new_form.to_dict()

@items_routes.route('/delete/<int:id>', methods=['DELETE'])
@login_required
def delete_cartitem(id):
    item_to_delete = Item.query.get(id)

    if (item_to_delete):

        db.session.delete(item_to_delete)
        db.session.commit()
        return {"message": "Cart Item Deleted!"}
    else:
        return {'errors': "No cart item to delete"}


@items_routes.route('/')
def get_all_items():
    items = Item.query.all()

    return [item.to_dict() for item in items]
