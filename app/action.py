from flask import redirect
from . import blp

@blp.route('/')
def index():
    return redirect("/admin/",code=301)
