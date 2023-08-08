from apps.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_required
from apps.authentication.models import BlogPost, ContactUs, Comment
from apps.authentication.forms import CommentForm, ContactUsForm, CreateBlogPostForm, PostEditForm
from functools import wraps
from flask import abort
from apps import db
from datetime import datetime


# Admin only decorator
def admin_only(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        # Otherwise continue with the route function
        return func(*args, **kwargs)

    return decorated_function


@blueprint.route('/')
def index():
    blog_post = db.session.query(BlogPost).all()
    return render_template('home/index.html', logged_in=current_user.is_authenticated,
                           current_user=current_user, all_post=blog_post)


@blueprint.route("/read-post/<int:post_id>", methods=["GET", "POST"])
@login_required
def read_post(post_id):
    comment_form = CommentForm()
    post_to_read = db.session.query(BlogPost).filter_by(id=int(post_id)).first()

    if request.method == "POST" and comment_form.validate_on_submit():

        # write comment to db
        new_comment = Comment(comment=request.form["comment"],
                              comment_author=current_user,
                              author_post=post_to_read
                              )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("home_blueprint.read_post", post_id=post_id))

    return render_template("home/read_post.html", logged_in=current_user.is_authenticated, post=post_to_read,
                           name=current_user.name, form=comment_form)


@blueprint.route("/add", methods=["GET", "POST"])
@login_required
def add():
    create_blog_post_form = CreateBlogPostForm()
    if request.method == "POST" and create_blog_post_form.validate_on_submit():
        new_post = BlogPost(
            title=request.form["title"],
            subtitle=request.form["subtitle"],
            post_author=current_user,
            img_url=request.form["img_url"],
            body=request.form["body"],
            date=datetime.now().date()
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("home_blueprint.index"))

    return render_template("home/add.html", form=create_blog_post_form, logged_in=current_user.is_authenticated,
                           current_user=current_user)


@blueprint.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    post_edit_form = PostEditForm()
    if request.method == "POST":
        post_id = request.args.get('post_id')
        post_to_update = db.session.query(BlogPost).get(int(post_id))
        post_to_update.subtitle = request.form["subtitle"]
        post_to_update.body = request.form["new_body"]
        db.session.commit()
        return redirect(url_for('home_blueprint.index'))
    post_id = request.args.get('post_id')
    post_selected = db.session.query(BlogPost).get(int(post_id))
    return render_template("home/edit.html", post=post_selected, form=post_edit_form,
                           logged_in=current_user.is_authenticated, current_user=current_user)


@blueprint.route("/delete/<int:post_id>")
@login_required
def delete(post_id):
    post_to_delete = BlogPost.query.get(int(post_id))
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('home_blueprint.index'))


@blueprint.route("/contact-us", methods=['GET', 'POST'])
def contact_us():
    contact_us_form = ContactUsForm()
    if request.method == "POST":
        name = contact_us_form.name.data
        email = contact_us_form.email.data
        message = contact_us_form.message.data
        message_to_us = ContactUs(
            name=name,
            email=email,
            message=message,
            date=datetime.now().date()
        )
        db.session.add(message_to_us)
        db.session.commit()

        return redirect(url_for('home_blueprint.index'))
