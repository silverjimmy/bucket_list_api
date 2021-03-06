from app.models import Bucket, Activity, User
from flask import Blueprint, make_response, jsonify, request, session
from app.utils import login_required


search = Blueprint('search', __name__, url_prefix='/api/v1')


@search.route('/search', methods=['GET'])
@login_required
def search_api():
    """
    This end point is used to search for buckets and activities in the bucket
    :return: json response
    """
    query = request.args.get('q')
    if not query:
        return make_response(jsonify(error='Please enter search parameters'), 400)

    email = session.get('user')
    user = User.query.filter_by(email=email).first()
    bucket_lists = Bucket.query.search(query).filter_by(user_id=user.id).all()
    activities = Activity.query.search(query).filter_by(user_id=user.id).all()
    bucket_obj = [bucket.serialize for bucket in bucket_lists]
    activity_obj = [activity.serialize for activity in activities]
    return make_response(jsonify(buckets=bucket_obj, activities=activity_obj))
