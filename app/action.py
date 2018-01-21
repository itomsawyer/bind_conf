from flask import url_for, redirect, render_template, request, abort
from flask_security import current_user
from . import blp

@blp.route('/')
def index():
    if not current_user.is_active or not current_user.is_authenticated:
        return redirect(url_for('security.login', next="/admin/"))

    return redirect('/admin/')
