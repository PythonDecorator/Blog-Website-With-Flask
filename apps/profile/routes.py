from apps.profile import blueprint
from flask import render_template
from flask_login import current_user, login_required
from apps.authentication.models import User, BlogPost
from apps import db


@blueprint.route('/my-profile')
@login_required
def profile():
    user_posts = db.session.query(BlogPost).filter_by(id=int(current_user.id))
    all_users = db.session.query(User).all()
    return render_template('home/profile.html',
                           name=current_user.name,
                           logged_in=True,
                           current_user=current_user,
                           users_db=all_users,
                           user_posts=user_posts)
