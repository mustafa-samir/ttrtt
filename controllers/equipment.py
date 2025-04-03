from datetime import datetime  # Add this import at the top
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models.models import Equipment

equipment_bp = Blueprint('equipment', __name__, url_prefix='/equipment')

@equipment_bp.route('/')
@login_required
def index():
    equipment_items = Equipment.query.order_by(Equipment.name).all()
    
    if not equipment_items:  # Add empty state handling
        flash('No equipment found. Add your first item using the button above.', 'info')
    
    return render_template('equipment/index.html', 
                         equipment_items=equipment_items,
                         now=datetime.utcnow())  # Add current time context

# Add template filename validation
@equipment_bp.route('/view/<int:id>')
@login_required
def view(id):
    equipment = Equipment.query.get_or_404(id)
    return render_template('equipment/view.html', equipment=equipment)