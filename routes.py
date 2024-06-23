from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user

from forms import StateForm, PositionForm, DepartmentForm, EmployeeForm, SearchEmployeeForm
from models import Employee, Position, Department, State, User
from init_db import db

main = Blueprint('main', __name__)


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash("Invalid Username")
            return render_template('register.html')
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('register.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.index'))
    return render_template('login.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


# Create routes
@main.route('/create_employee', methods=['GET', 'POST'])
@login_required
def create_employee():
    form = EmployeeForm()
    form.position.choices = [(-1, 'No Position')] + [(e.id, e.name) for e in Position.query.all()]
    form.department.choices = [(-1, 'No Department')] + [(e.id, e.name) for e in Department.query.all()]
    form.state.choices = [(-1, 'No State')] + [(e.id, e.name) for e in State.query.all()]
    if form.validate_on_submit():
        if form.position.data == -1 or form.department.data == -1 or form.state.data == -1:
            flash('Employee must have position, department, and state')
            return redirect(url_for('main.index'))
        new_employee = Employee(name=form.name.data, address=form.address.data, position_id=form.position.data,
                                department_id=form.department.data, state_id=form.state.data)
        db.session.add(new_employee)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('create_employee.html', form=form)


@main.route('/create_position', methods=['GET', 'POST'])
@login_required
def create_position():
    form = PositionForm()
    if form.validate_on_submit():
        new_position = Position(name=form.name.data, details=form.details.data)
        db.session.add(new_position)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('create_position.html', form=form)


@main.route('/create_department', methods=['GET', 'POST'])
@login_required
def create_department():
    form = DepartmentForm()
    form.manager.choices = [(-1, 'No Manager')] + [(e.id, e.name) for e in Employee.query.all()]
    if form.validate_on_submit():
        new_department = Department(name=form.name.data,
                                    manager_id=form.manager.data) if form.manager.data != -1 else Department(name=form.name.data)
        db.session.add(new_department)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('create_department.html', form=form)


@main.route('/create_state', methods=['GET', 'POST'])
@login_required
def create_state():
    form = StateForm()
    if form.validate_on_submit():
        new_state = State(name=form.name.data)
        db.session.add(new_state)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('create_state.html', form=form)


# Read routes
@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = SearchEmployeeForm()
    form.position.choices = [(0, 'All Position')] + [(pos.id, pos.name) for pos in Position.query.all()]
    form.department.choices = [(0, 'All Department')] + [(dept.id, dept.name) for dept in Department.query.all()]
    form.state.choices = [(0, 'All State')] + [(st.id, st.name) for st in State.query.all()]

    query = Employee.query
    if form.position.data:
        query = query.filter(Employee.position_id == form.position.data)
    if form.department.data:
        query = query.filter(Employee.department_id == form.department.data)
    if form.state.data:
        query = query.filter(Employee.state_id == form.state.data)

    employees = query.all()
    positions = Position.query.all()
    departments = Department.query.all()
    states = State.query.all()
    return render_template('index.html', form=form, employees=employees, positions=positions, departments=departments,
                           states=states)


# Update routes
@main.route('/update_employee/<int:id>', methods=['GET', 'POST'])
@login_required
def update_employee(id):
    employee = Employee.query.get_or_404(id)
    form = EmployeeForm(obj=employee)
    form.position.choices = [(-1, 'No Position')] + [(e.id, e.name) for e in Position.query.all()]
    form.department.choices = [(-1, 'No Department')] + [(e.id, e.name) for e in Department.query.all()]
    form.state.choices = [(-1, 'No State')] + [(e.id, e.name) for e in State.query.all()]
    if form.validate_on_submit():
        if form.position.data == -1 or form.department.data == -1 or form.state.data == -1:
            flash('Employee must have position, department, and state')
            return redirect(url_for('main.index'))
        employee.name = form.name.data
        employee.address = form.address.data
        employee.position_id = form.position.data
        employee.department_id = form.department.data
        employee.state_id = form.state.data
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('update_employee.html', form=form, employee=employee)


@main.route('/update_position/<int:id>', methods=['GET', 'POST'])
@login_required
def update_position(id):
    position = Position.query.get_or_404(id)
    form = PositionForm(obj=position)
    if form.validate_on_submit():
        position.name = form.name.data
        position.details = form.details.data
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('update_position.html', form=form, position=position)


@main.route('/update_department/<int:id>', methods=['GET', 'POST'])
@login_required
def update_department(id):
    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    form.manager.choices = [(-1, 'No manager')] + [(e.id, e.name) for e in Employee.query.all()]
    if form.validate_on_submit():
        department.name = form.name.data
        department.manager_id = form.manager.data if form.manager.data != -1 else None
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('update_department.html', form=form, department=department)


@main.route('/update_state/<int:id>', methods=['GET', 'POST'])
@login_required
def update_state(id):
    state = State.query.get_or_404(id)
    form = StateForm(obj=state)
    if form.validate_on_submit():
        state.name = form.name.data
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('update_state.html', form=form, state=state)


# Delete routes
@main.route('/delete_employee/<int:id>', methods=['POST'])
@login_required
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    if employee.managing_department:
        flash('Cannot delete employee who is a department manager.')
        return redirect(url_for('main.index'))
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for('main.index'))


@main.route('/delete_position/<int:id>', methods=['POST'])
@login_required
def delete_position(id):
    position = Position.query.get_or_404(id)
    if position.employees:
        flash('Cannot delete position with employees assigned.')
        return redirect(url_for('main.index'))
    db.session.delete(position)
    db.session.commit()
    return redirect(url_for('main.index'))


@main.route('/delete_department/<int:id>', methods=['POST'])
@login_required
def delete_department(id):
    department = Department.query.get_or_404(id)
    if department.employees:
        flash('Cannot delete department with employees assigned.')
        return redirect(url_for('main.index'))
    db.session.delete(department)
    db.session.commit()
    return redirect(url_for('main.index'))


@main.route('/delete_state/<int:id>', methods=['POST'])
@login_required
def delete_state(id):
    state = State.query.get_or_404(id)
    if state.employees:
        flash('Cannot delete state with employees assigned.')
        return redirect(url_for('main.index'))
    db.session.delete(state)
    db.session.commit()
    return redirect(url_for('main.index'))
