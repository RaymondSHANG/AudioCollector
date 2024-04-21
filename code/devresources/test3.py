from fhirclient.models import patient as p
from fhirclient import client
from fhirclient.models.fhirsearch import FHIRSearch
from fhirclient.models.encounter import Encounter
from fhirclient.models import encounter as enc
from fhirclient.models.medicationrequest import MedicationRequest
from fhirclient.models import domainresource, bundle, fhirsearch
from fhirclient.models.fhirsearch import FHIRSearchParam as fparam

#MedicationRequest
settings = {
    'app_id': 'my_web_app',
    # 'https://fhir-open-api-dstu2.smarthealthit.org'
    'api_base':  'http://hapi.fhir.org/baseDstu3/'
}
smart = client.FHIRClient(settings=settings)


"""perform gives back bundle, perform_resources gives back a list of resources"""
search3 = Encounter.where(struct={'patient': '41177'})
#'patient': '1299018'
encounters = search3.perform_resources(smart.server)
# print(encounters.as_json())

for e in encounters:
    print(e.type[0].text)
