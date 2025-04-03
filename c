{% extends 'base.html' %}
{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Lab Equipment</h1>
        <a href="{{ url_for('equipment.add') }}" class="btn btn-primary">
            <i class="bi bi-plus-lg"></i> Add Equipment
        </a>
    </div>

    {% if equipment_items %}
    <div class="table-responsive">
        <table class="table table-hover align-middle">
            <thead class="table-light">
                <tr>
                    <th>Name</th>
                    <th>Serial Number</th>
                    <th>Location</th>
                    <th>Last Maintenance</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for item in equipment_items %}
                <tr>
                    <td>{{ item.name }}</td>
                    <td>{{ item.serial_number or 'N/A' }}</td>
                    <td>{{ item.location }}</td>
                    <td>
                        {% if item.last_maintenance_date %}
                            {{ item.last_maintenance_date.strftime('%Y-%m-%d') }}
                            <small class="text-muted">({{ ((now - item.last_maintenance_date).days) }} days ago)</small>
                        {% else %}
                            Never
                        {% endif %}
                    </td>
                    <td>
                        <a href="{{ url_for('equipment.view', id=item.id) }}" class="btn btn-sm btn-outline-secondary">
                            <i class="bi bi-eye"></i>
                        </a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% else %}
    <div class="alert alert-warning">
        No equipment items found in the database.
    </div>
    {% endif %}
</div>
{% endblock %}
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">