from flask import Blueprint, request
from ..models import Review, User, db
from flask_login import login_required, current_user
from ..forms import ReviewForm
from .auth_routes import validation_errors_to_error_messages
from datetime import date

reviews_routes = Blueprint('reviews', __name__)

#create a review
@reviews_routes.route('/new/vehicles/<int:id>', methods=['POST'])
@login_required
def post_new_review(id):
    form = ReviewForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        new_review = Review(
            user_id=current_user.id,
            vehicle_id=id,
            review=form.data['review'],
            stars=form.data['stars'],
            created_at=date.today()
        )
        db.session.add(new_review)
        db.session.commit()
        return new_review.to_dict()
    return {'errors': validation_errors_to_error_messages(form.errors)}, 400

@reviews_routes.route('/<int:id>/update/vehicles/', methods=['PUT'])
@login_required
def update_new_review(id):
    review_to_update = Review.query.get(id)

    form = ReviewForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        new_review=form.data['review']
        new_stars=form.data['stars']

        review_to_update.review = new_review
        review_to_update.stars=new_stars

        db.session.commit()
        return review_to_update.to_dict()
    return {'errors': validation_errors_to_error_messages(form.errors)}, 400


#get all reviews
@reviews_routes.route('/all')
@login_required
def get_all_reviews():
    all_reviews = Review.query.all()
    return [review.to_dict() for review in all_reviews]

#get one comment
@reviews_routes.route('/')


#delete a comment
@reviews_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_comment(id):
    comment_to_delete = Comment.query.get(id)
    db.session.delete(comment_to_delete)
    db.session.commit()
    return {"Message" : "Comment Deleted"}
