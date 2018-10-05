from sqlalchemy.orm import joinedload


def register_jinja_ext(app):
    from flaskblog.models import Comment
    from flaskblog import db
    with app.app_context():
        app.jinja_env.globals.update({
            'latest_comments': db.session.query(Comment)
                .options(joinedload('post'))
                .order_by(Comment.date_posted.desc()) \
                .limit(5).
                all()
        })
