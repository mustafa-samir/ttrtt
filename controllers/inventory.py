from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from extensions import db  # Keep only this import for db
from models.models import InventoryItem
# Remove this line: from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SelectField, BooleanField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional
from datetime import datetime, timedelta  # Added timedelta import

from flask import Blueprint

inventory_bp = Blueprint(
    'inventory',
    __name__,
    template_folder='../templates/inventory'  # Adjust this path according to your actual structure
)

# Forms
class InventoryItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('Chemical', 'Chemical'),
        ('Equipment', 'Equipment'),
        ('Consumable', 'Consumable'),
        ('Glassware', 'Glassware'),
        ('Other', 'Other')
    ])
    quantity = FloatField('Quantity', validators=[DataRequired()])
    unit = StringField('Unit', validators=[DataRequired()])
    location = StringField('Location')
    minimum_quantity = FloatField('Minimum Quantity')
    is_hazardous = BooleanField('Is Hazardous')
    hazard_information = TextAreaField('Hazard Information')
    purchase_date = DateField('Purchase Date', format='%Y-%m-%d', validators=[Optional()])
    expiry_date = DateField('Expiry Date', format='%Y-%m-%d', validators=[Optional()])
    supplier = StringField('Supplier')
    submit = SubmitField('Submit')

# Routes
@inventory_bp.route('/')
@login_required
def index():
    inventory_items = InventoryItem.query.all()
    return render_template('inventory/index.html', inventory_items=inventory_items)

@inventory_bp.route('/low-stock')
@login_required
def low_stock():
    # Modified query to handle null minimum_quantity cases
    low_stock_items = InventoryItem.query.filter(
        InventoryItem.minimum_quantity.isnot(None),
        InventoryItem.quantity <= InventoryItem.minimum_quantity
    ).order_by(InventoryItem.quantity.asc()).all()
    
    if not low_stock_items:
        flash('No low stock items found', 'info')
    
    return render_template('inventory/low_stock.html', low_stock_items=low_stock_items)

@inventory_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = InventoryItemForm()
    if form.validate_on_submit():
        item = InventoryItem(
            name=form.name.data,
            category=form.category.data,
            quantity=form.quantity.data,
            unit=form.unit.data,
            location=form.location.data,
            minimum_quantity=form.minimum_quantity.data,
            is_hazardous=form.is_hazardous.data,
            hazard_information=form.hazard_information.data,
            purchase_date=form.purchase_date.data,
            expiry_date=form.expiry_date.data,
            supplier=form.supplier.data
        )
        db.session.add(item)
        db.session.commit()
        flash('Inventory item added successfully!')
        return redirect(url_for('inventory.index'))
    return render_template('inventory/form.html', title='Add Inventory Item', form=form)

@inventory_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    item = InventoryItem.query.get_or_404(id)
    form = InventoryItemForm(obj=item)
    if form.validate_on_submit():
        item.name = form.name.data
        item.category = form.category.data
        item.quantity = form.quantity.data
        item.unit = form.unit.data
        item.location = form.location.data
        item.minimum_quantity = form.minimum_quantity.data
        item.is_hazardous = form.is_hazardous.data
        item.hazard_information = form.hazard_information.data
        item.purchase_date = form.purchase_date.data
        item.expiry_date = form.expiry_date.data
        item.supplier = form.supplier.data
        db.session.commit()
        flash('Inventory item updated successfully!')
        return redirect(url_for('inventory.index'))
    return render_template('inventory/form.html', title='Edit Inventory Item', form=form)

@inventory_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    item = InventoryItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Inventory item deleted successfully!')
    return redirect(url_for('inventory.index'))

@inventory_bp.route('/view/<int:id>')
@login_required
def view(id):
    item = InventoryItem.query.get_or_404(id)
    return render_template('inventory/view.html', title=item.name, item=item)

@inventory_bp.route('/hazardous')
@login_required
def hazardous():
    items = InventoryItem.query.filter_by(is_hazardous=True).all()
    return render_template('inventory/hazardous.html', title='Hazardous Items', items=items)

# In expiring route, fix timedelta usage
@inventory_bp.route('/expiring')
@login_required
def expiring():
    today = datetime.utcnow().date()
    thirty_days_later = today + timedelta(days=30)  # Removed datetime prefix
    items = InventoryItem.query.filter(
        InventoryItem.expiry_date.isnot(None),
        InventoryItem.expiry_date <= thirty_days_later,
        InventoryItem.expiry_date >= today
    ).order_by(InventoryItem.expiry_date).all()
    return render_template('inventory/expiring.html', title='Expiring Items', items=items)

@inventory_bp.route('/adjust/<int:id>', methods=['GET', 'POST'])
@login_required
def adjust(id):
    item = InventoryItem.query.get_or_404(id)
    if request.method == 'POST':
        adjustment = float(request.form.get('adjustment', 0))
        item.quantity += adjustment
        db.session.commit()
        flash(f'Inventory adjusted by {adjustment} {item.unit}')
        return redirect(url_for('inventory.view', id=id))
    return render_template('inventory/adjust.html', title=f'Adjust {item.name}', item=item)