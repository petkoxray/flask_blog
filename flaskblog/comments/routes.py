from flask import render_template, url_for, flash, redirect, Blueprint
from flaskblog import db
from flaskblog.comments.forms import CommentForm
from flaskblog.models import Post, Comment

comments = Blueprint('comments', __name__)


@comments.route("/post/<int:post_id>/comment", methods=['POST'])
def new_comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, author=form.author.data,
                          email=form.email.data, site_url=form.site_url.data,
                          post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))

    return render_template('posts/post.html', title=post.title, post=post, form=form)
