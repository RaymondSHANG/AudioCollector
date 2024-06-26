from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user
from application import db
from application.models import UserModel
from application.users.forms import LoginForm, RegistrationForm
from application.fhir.search import ResourceFinder
from application.fhir.connect import smart
from fhirclient.models.patient import Patient
from flask_login import current_user, login_required

users_bp = Blueprint('users_bp', __name__)


@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    flash(f"smart server:{smart}")
    #PatientFinder = ResourceFinder.build('Patient', smart.server)
    #patient = Patient.read(current_user.patient_id, smart.server)
    if form.validate_on_submit():
        # Check patient on FHIR server
        patient = Patient.read(form.identifier_value.data, smart.server)

        if not patient:
            flash(f'No patient record found, please check again. If you keep failing the verification, please contact your provider.')

        else:
            check_patient_duplicated = UserModel.query.filter_by(
                patient_id=patient.id).first()
            check_email_matched = UserModel.query.filter_by(
                email=form.email.data).first()
            check_dob_matched = patient.birthDate.date == form.date_of_birth.data
            check_family_matched = patient.name[0].family == form.family_name.data
            check_given_matched = patient.name[0].given[0] == form.given_name.data
            
            if check_patient_duplicated:
                flash(f'The patient has been registered already.')
            elif check_email_matched:
                flash(f'The email has been registered already.')
            elif not (check_dob_matched or check_family_matched or check_given_matched):
                flash(f'No patient record found, please check again. If you keep failing the verification, please contact your provider.')
            else:
                user = UserModel(
                    given_name=patient.name[0].given[0],
                    family_name=form.family_name.data,
                    date_of_birth=form.date_of_birth.data,
                    identifier_system=form.identifier_system.data,
                    identifier_value=form.identifier_value.data,
                    oauth_server = form.oauth_server.data,
                    patient_id=patient.id,
                    email=form.email.data,
                    password=form.password.data
                )

                db.session.add(user)
                db.session.commit()
                flash(f'Welcome {patient.name[0].given[0]}! Please login now.')
                return redirect(url_for('users_bp.login'))

    return render_template('register.html', form=form)


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = UserModel.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash(f'Welcome back, {user.given_name}!')
            return redirect(url_for('core_bp.main'))

        else:
            flash('Incorrect email or password, please try again.')
            return redirect(url_for('users_bp.login'))

    return render_template('login.html', form=form)


@users_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash("You've now logged out.")
    return redirect(url_for('core_bp.welcome'))
