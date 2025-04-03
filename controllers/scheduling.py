from flask import Blueprint, render_template
from flask_login import login_required

scheduling_bp = Blueprint('scheduling', __name__, url_prefix='/scheduling')

@scheduling_bp.route('/')
@login_required
def index():
    return render_template('scheduling/index.html')

@scheduling_bp.route('/calendar')
@login_required
def calendar():
    return render_template('scheduling/calendar.html')