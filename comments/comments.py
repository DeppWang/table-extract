from comments.auth import login_required
from comments.db import get_db
from flask import request, render_template, Blueprint, redirect, url_for, g

bp = Blueprint("comments", __name__)


@bp.route("/", methods=["GET"])
def index():
    is_json = request.values.get('is_json', 0)
    db = get_db()
    data = db.execute('''SELECT * FROM comments ORDER BY created_time DESC''').fetchall()
    new_data = [{'id': item[0], 'content': item[1], 'parent': item[2], 'username': item[3], 'created_time': item[4]} for
                item in data]
    comments = generate_tree(new_data, 0)
    if is_json:
        return {'data': comments}
    return render_template("comments/index.html", comments=comments)


@bp.route("/", methods=["POST"])
@login_required
def post_index():
    content = request.form["content"]
    parent = request.form["parent"] or 0
    db = get_db()
    db.execute("INSERT INTO comments (content, parent, username) VALUES (?, ?, ?)",
               (content, parent, g.user['username']))
    db.commit()
    return redirect(url_for("index"))


def generate_tree(source, parent):
    """
    生成树状结构
    :param source:
    :param parent:
    :return:
    """
    tree = []
    for item in source:
        if item["parent"] == parent:
            item["child"] = generate_tree(source, item["id"])
            tree.append(item)
    return tree
