from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from extensions import db  # Import db from extensions, not from app

# User models
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

# Equipment model
class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    serial_number = db.Column(db.String(100), unique=True)
    purchase_date = db.Column(db.Date)
    purchase_cost = db.Column(db.Float)
    status = db.Column(db.String(20), default='Available')  # Available, In Use, Maintenance, Retired
    location = db.Column(db.String(100))
    maintenance_records = db.relationship('MaintenanceRecord', backref='equipment', lazy='dynamic')
    
    def __repr__(self):
        return f'<Equipment {self.name}>'

# Maintenance records
class MaintenanceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))
    maintenance_date = db.Column(db.Date, default=datetime.utcnow)
    description = db.Column(db.Text)
    cost = db.Column(db.Float)
    performed_by = db.Column(db.String(100))
    next_maintenance_date = db.Column(db.Date)
    
    def __repr__(self):
        return f'<Maintenance Record {self.id}>'

# Laboratory model
class Laboratory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    capacity = db.Column(db.Integer)
    description = db.Column(db.Text)
    schedules = db.relationship('Schedule', backref='laboratory', lazy='dynamic')
    
    def __repr__(self):
        return f'<Laboratory {self.name}>'

# Schedule model
class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    laboratory_id = db.Column(db.Integer, db.ForeignKey('laboratory.id'))
    title = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='Scheduled')  # Scheduled, Completed, Cancelled
    user = db.relationship('User', backref='schedules')
    
    def __repr__(self):
        return f'<Schedule {self.title}>'

# Inventory Item model
class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))  # Chemical, Equipment, Consumable, etc.
    quantity = db.Column(db.Float)
    unit = db.Column(db.String(20))  # g, ml, pieces, etc.
    location = db.Column(db.String(100))
    minimum_quantity = db.Column(db.Float)
    is_hazardous = db.Column(db.Boolean, default=False)
    hazard_information = db.Column(db.Text)
    purchase_date = db.Column(db.Date)
    expiry_date = db.Column(db.Date)
    supplier = db.Column(db.String(100))
    
    def __repr__(self):
        return f'<Inventory Item {self.name}>'

# Safety Protocol model
class SafetyProtocol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # Chemical, Equipment, General, etc.
    document_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Safety Protocol {self.title}>'

# Experiment Data model
class ExperimentData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    data = db.Column(db.Text)  # JSON data or file path
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    schedule = db.relationship('Schedule', backref='experiment_data')
    user = db.relationship('User', backref='experiment_data')
    
    def __repr__(self):
        return f'<Experiment Data {self.title}>'