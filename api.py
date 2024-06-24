from flask import Blueprint, request
from flask_restful import fields, marshal_with

from models import Employee, Position, Department
from init_db import db

apiBp = Blueprint('apiBp', __name__)

# Define resource fields
employee_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'address': fields.String,
    'position_id': fields.Integer,
    'department_id': fields.Integer,
    'state_id': fields.Integer,
    'image': fields.String,
}

position_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'details': fields.String
}

department_fields = {
    'id': fields.Integer,
    'name': fields.String
}


@apiBp.route('/employees', methods=['GET'])
@apiBp.route('/employees/<int:employee_id>')
@marshal_with(employee_fields)
def get_employee(employee_id=None):
    employee = Employee.query.get_or_404(employee_id) if employee_id else Employee.query.all()
    return employee


@apiBp.route('/employees', methods=['POST'])
@marshal_with(employee_fields)
def add_employee():
    args = request.form
    image_file = args['image'] if 'image' in args else 'default.jpg'
    print(args['name'])
    new_employee = Employee(
        name=args['name'],
        address=args['address'],
        position_id=args['position_id'],
        department_id=args['department_id'],
        state_id=args['state_id'],
        image_file=image_file
    )
    db.session.add(new_employee)
    db.session.commit()
    return new_employee, 201


@apiBp.route('/employees/<int:employee_id>', methods=['PUT'])
@marshal_with(employee_fields)
def put(employee_id):
    args = request.form
    employee = Employee.query.get_or_404(employee_id)
    employee.name = args['name'] if 'name' in args else employee.name
    employee.address = args['address'] if 'address' in args else employee.address
    employee.position_id = args['position_id'] if 'position_id' in args else employee.position_id
    employee.department_id = args['department_id'] if 'department_id' in args else employee.department_id
    employee.state_id = args['state_id'] if 'state_id' in args else employee.state_id
    employee.image_file = args['image'] if 'image' in args else employee.image_file
    db.session.commit()
    return employee


@apiBp.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    if employee.managing_department:
        return 'Cannot delete employee who is a department manager', 422
    db.session.delete(employee)
    db.session.commit()
    return '', 204


@apiBp.route('/positions', methods=['GET'])
@apiBp.route('/positions/<int:position_id>', methods=['GET'])
@marshal_with(position_fields)
def get_position(position_id=None):
    if position_id:
        position = Position.query.get_or_404(position_id)
        return position
    else:
        positions = Position.query.all()
        return positions


@apiBp.route('/positions', methods=['POST'])
@marshal_with(position_fields)
def add_position():
    args = request.form
    position = Position(name=args['name'], details=args['details'])
    db.session.add(position)
    db.session.commit()
    return position, 201

@apiBp.route('/positions/<int:position_id>', methods=['PUT'])
@marshal_with(position_fields)
def edit_position(position_id):
    args = request.form
    position = Position.query.get_or_404(position_id)
    position.name = args['name'] if 'name' in args else position.name
    position.details = args['details'] if 'details' in args else position.details
    db.session.commit()
    return position


@apiBp.route('/positions/<int:position_id>', methods=['DELETE'])
def delete_position(position_id):
    position = Position.query.get_or_404(position_id)
    if position.employees:
        return 'Cannot delete a position with employees assigned.', 422
    db.session.delete(position)
    db.session.commit()
    return '', 204

@apiBp.route('/departments', methods=['GET'])
@apiBp.route('/departments/<int:department_id>', methods=['GET'])
@marshal_with(department_fields)
def get_department(department_id=None):
    if department_id:
        department = Department.query.get_or_404(department_id)
        return department
    else:
        department = Department.query.all()
        return department


@apiBp.route('/departments', methods=['POST'])
@marshal_with(department_fields)
def add_department():
    args = request.form
    department = Department(name=args['name'])
    db.session.add(department)
    db.session.commit()
    return department, 201

@apiBp.route('/departments/<int:department_id>', methods=['PUT'])
@marshal_with(department_fields)
def edit_department(department_id):
    args = request.form
    department = Department.query.get_or_404(department_id)
    department.name = args['name']
    db.session.commit()
    return department


@apiBp.route('/departments/<int:department_id>', methods=['DELETE'])
def delete_department(department_id):
    department = Department.query.get_or_404(department_id)
    if department.employees:
        return 'Cannot delete a department with employees assigned.', 422
    db.session.delete(department)
    db.session.commit()
    return '', 204
