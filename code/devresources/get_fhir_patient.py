from fhirclient.models import patient as p
from fhirclient import client
from fhirclient.models.fhirsearch import FHIRSearch
from fhirclient.models.encounter import Encounter

settings = {
    'app_id': 'my_web_app',
    # 'https://fhir-open-api-dstu2.smarthealthit.org'
    'api_base':  'http://hapi.fhir.org/baseDstu3/'
}
# http://hapi.fhir.org/baseR4
# http://hapi.fhir.org/baseDstu3/
# https://bulk-data.smarthealthit.org/eyJlcnIiOiIiLCJwYWdlIjoxMDAwMCwiZHVyIjoxMCwidGx0IjoxNSwibSI6MSwic3R1Ijo0LCJkZWwiOjB9/fhir
# 'http://tomcat.nuchange.ca/fhir/'
# 'https://healthcare.googleapis.com/v1/projects/gcp-testing-308520/locations/us-east4/datasets/testset/fhirStores/fhirstore/fhir'
# 'https://r3.smarthealthit.org/'
# 'https://launch.smarthealthit.org/v/r4/sim/WzIsIiIsIiIsIkFVVE8iLDAsMSwwLCIiLCIiLCIiLCIiLCIiLCIiLCIiLDAsMV0/fhir'
# https://launch.smarthealthit.org/v/r4/sim/WzIsIiIsIiIsIkFVVE8iLDAsMCwwLCIiLCIiLCIiLCIiLCIiLCIiLCIiLDAsMV0/fhir
# https://launch.smarthealthit.org/v/r4/sim/WzIsIiIsIiIsIkFVVE8iLDAsMCwwLCIiLCIiLCIiLCIiLCIiLCIiLCIiLDAsMV0/fhir
smart = client.FHIRClient(settings=settings)

# print(f"smart.ready:{smart.ready}")
# print(f"smart.prepare(): {smart.prepare()}")
# print(f"smart.ready:{smart.ready}")

# smart.ready
# smart.prepare()
# smart.authorize_url

struct = {'identifier': 'http://hl7.org/fhir/sid/us-ssn|999-45-3776'}
# patient = p.Patient.read('1349276', smart.server)
search = p.Patient.where(struct=struct)
# patient = search.perform(smart.server).entry[0].resource
# patient = search.perform_resources(smart.server)[0]

if len(search.perform_resources(smart.server)) > 0:
    patient = search.perform_resources(smart.server)[0]
    print(patient)

    print(patient.birthDate.isostring)

    print(patient.id)

    print(smart.human_name(patient.name[0]))
    print(search.resource_type.resource_type)
else:
    print("No patient found matching the given criteria.")

print("\n\n\n##########################\n Test Encounter")
search = Encounter.where(struct={'patient': patient.id, '_count': '100'})
search.perform(smart.server)

encounter = search.perform_resources(smart.server)
print(len(encounter))

"""perform gives back bundle, perform_resources gives back a list of resources"""
search = Encounter.where(struct={'patient': patient.id})
encounters = search.perform_resources(smart.server)
# print(encounters.as_json())

for e in encounters:
    print(e.type[0].text)
