from fhirclient import client


hostname_prefix = 'cibmtr-smart-dev'
auth_server = 'https://{0}-auth.b12x.org'.format(hostname_prefix)
aud = 'https://{0}-stu3.b12x.org/smartstu3/data'.format(hostname_prefix)
sandman_url = 'https://{0}-sandman.b12x.org/'.format(hostname_prefix)

settings = {
    'app_id': 'my_web_app',
    'api_base': aud,
    'redirect_uri': sandman_url,
}
'''

        - `app_id`*: Your app/client-id, e.g. 'my_web_app'
        - `app_secret`*: Your app/client-secret
        - `api_base`*: The FHIR service to connect to, e.g. 'https://fhir-api-dstu2.smarthealthit.org'
        - `redirect_uri`: The callback/redirect URL for your app, e.g. 'http://localhost:8000/fhir-app/' when testing locally
        - `patient_id`: The patient id against which to operate, if already known
        - `scope`: Space-separated list of scopes to request, if other than default
        - `launch_token`: The launch token
'''

smart = client.FHIRClient(settings=settings)
