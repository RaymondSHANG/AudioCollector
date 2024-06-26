from flask import render_template, Blueprint, session, flash, redirect, url_for
from flask_login import current_user, login_required
from fhirclient.models.patient import Patient
from contextlib import suppress
from application.fhir.connect import connector
from application.fhir.search import ResourceFinder
from application.profile.forms import EditProfileForm
#from application.oauth.utils import oauth_required
from application.fhir.connect import smart

profile_bp = Blueprint(
    'profile_bp',
    __name__,
    url_prefix='/profile'
)


@profile_bp.route('/', methods=['GET'])
@login_required
def profile():
    # If not login go to login
    #if current_user.au
    #smart = connector.source_client
    #PatientFinder = ResourceFinder.build('Patient', smart.server)
    #PatientFinder = Patient.where(struct={'family': 'Smith'})
    patient = Patient.read(current_user.patient_id, smart.server)
    
    profile={}
    with suppress(TypeError):
        profile['title'] = patient.as_json().get('name', [{}])[0].get('family')# patient.name[0].prefix[0]
        contact_current = patient.as_json().get['telecom']
        if len(contact_current) >0:
            profile['contact'] = "{}: {} ({})".format(
                contact_current[0].system,
                contact_current[0].value,
                patient.telecom[0].use
            )
        else:
            profile['contact'] = "{}: {} ({})".format(
                "",
                "",
                ""
            )
        addess_current = patient.as_json().get['address']
        if len(addess_current) > 0:

            profile['address'] = ", ".join([
                addess_current[0].city,
                addess_current[0].state,
                addess_current[0].postalCode,
                addess_current[0].country
            ])
            profile['city'] = addess_current[0].city
            profile['state'] = addess_current[0].state
            profile['postalcode'] = addess_current[0].postalCode
            profile['country'] = addess_current[0].country
        else:
            profile['address'] = ", ".join([
                "",
                "",
                "",
                ""
            ])
            profile['city'] = ""
            profile['state'] = ""
            profile['postalcode'] = ""
            profile['country'] = ""
        if patient.communication:
            profile['language'] = patient.communication[0].language.text
        else:
            profile['language'] = "English"

        session['profile'] = profile

    return render_template('profile.html', profile=profile, patient=patient,smart=smart)

@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    try:
        session['profile']
    except KeyError:
        return redirect(url_for('profile_bp.profile'))

    form = EditProfileForm()

    #smart = connector.source_client
    PatientFinder = ResourceFinder.build('Patient', smart.server)
    patient = PatientFinder.find_by_id(
        current_user.patient_id,
        first=True
    )

    if form.validate_on_submit():
        city = form.city.data
        state = form.state.data
        postalcode = form.postalcode.data
        country = form.country.data

        patient.address[0].city = city
        patient.address[0].state = state
        patient.address[0].postalCode = postalcode
        patient.address[0].country = country

        updated_patient_dict = patient.update()

        if updated_patient_dict:
            flash("Your profile has been updated successfully!")
            return redirect(url_for('profile_bp.profile'))

    return render_template('edit.html', form=form, profile=session['profile'])
