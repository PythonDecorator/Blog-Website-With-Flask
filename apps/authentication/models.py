from flask_login import UserMixin
from sqlalchemy.orm import relationship
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from apps import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String)

    oauth_github = db.Column(db.String(100), nullable=True)

    # get post from blog_posts table
    post = relationship('BlogPost', back_populates='post_author')

    # get the comment from comments table
    comment = relationship('Comment', back_populates='comment_author')

    # get following
    following = db.relationship('Following', backref='following_author', lazy='dynamic')

    def to_dict(self) -> dict:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default="datetime.utcnow")  # will be added by default
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)

    # we need user_id that posted
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # get author that posted and send the post to users
    post_author = relationship('User', back_populates='post')

    # get comment from comments table and send author post
    comment = relationship('Comment', back_populates='author_post')


class Comment(db.Model):
    __tablename__ = "comments"
    # main table attributes
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)

    # request: we need user_id that commented
    comment_author_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # get user and send comment to user
    comment_author = relationship("User", back_populates="comment")

    # request: we need author_post commented on
    author_post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))

    # get author_post and send comment to post_author
    author_post = relationship("BlogPost", back_populates="comment")


class UserProfile(db.Model):
    __tablename__ = "profile"
    id = db.Column(db.Integer, primary_key=True)
    profession = db.Column(db.String(64), nullable=True)
    profile_img = db.Column(db.String, nullable=True)
    bio = db.Column(db.Text, nullable=True)


class ContactUs(db.Model):
    __tablename__ = "contact_us"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default="datetime.utcnow")  # will be added by default
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    message = db.Column(db.String(250), nullable=False)


class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"), nullable=False)
    user = db.relationship(User)


class Following(db.Model):
    __tablename__ = "following"
    id = db.Column(db.Integer, primary_key=True)

    # we need following_author
    following_author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)



