from flask import Blueprint, jsonify

tags = Blueprint('tags', __name__)


@tags.route('/tag', methods=['POST'])
def new_tag():
    return jsonify({'status': 'ok'})
