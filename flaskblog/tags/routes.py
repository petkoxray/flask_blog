from flask import current_app, Blueprint, render_template, request
from flaskblog.models import Post, Tag

tags = Blueprint('tags', __name__)


@tags.route('/tag/<string:tag_name>')
def tag_posts(tag_name):
    page = request.args.get('page', 1, type=int)
    posts = Post.query.join(Tag, Post.tags).filter(Tag.name == tag_name) \
        .order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=current_app['POSTS_PER_PAGE'])

    return render_template('tags/tag_posts.html', posts=posts, tag_name=tag_name)
