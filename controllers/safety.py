from flask import Blueprint, render_template
from flask_login import login_required

safety_bp = Blueprint('safety', __name__, url_prefix='/safety')

@safety_bp.route('/')
@login_required
def index():
    return render_template('safety/index.html')