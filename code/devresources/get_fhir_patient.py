from fhirclient.models import patient as p
from fhirclient import client
from fhirclient.models.fhirsearch import FHIRSearch
from fhirclient.models.encounter import Encounter
from fhirclient.models import encounter as enc

settings = {
    'app_id': 'my_web_app',
    # 'https://fhir-open-api-dstu2.smarthealthit.org'
    'api_base':  'http://hapi.fhir.org/baseR4'
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

#print(f"smart.ready:{smart.ready}")
#print(f"smart.prepare(): {smart.prepare()}")
#print(f"smart.ready:{smart.ready}")

# smart.ready
# smart.prepare()
smart.authorize_url

struct = {'identifier': 'JP123456789'}

# patient = p.Patient.read('1349276', smart.server)
search = p.Patient.where(struct=struct)
# patient = search.perform(smart.server).entry[0].resource
# patient = search.perform_resources(smart.server)[0]
search = p.Patient.where(struct={'family': 'Cushing'})

if len(search.perform_resources(smart.server)) > 0:
    for patient in search.perform_resources(smart.server):
        #patient = search.perform_resources(smart.server)[0]
        #print(patient)
        print(smart.human_name(patient.name[0]))
        print(patient.id)
        if patient.birthDate:
            print(patient.birthDate.isostring)

        print(f"resource_type:{search.resource_type.resource_type}")
        print("\n\n\n##########################\n Test Encounter")
        struct_search = {'patient': patient.id, '_count': '100'}
        print(f"Patient: {struct_search}")
    search2 = Encounter.where(struct={'patient': patient.id, '_count': '100'})

    #Error below!
    search2.perform(smart.server)
    bundle = search2.perform(smart.server)
    print(bundle.as_json())
else:
    print("No patient found matching the given criteria.")



encounter = search.perform_resources(smart.server)
print(len(encounter))

"""perform gives back bundle, perform_resources gives back a list of resources"""
search3 = Encounter.where(struct={'patient': patient.id})
#'patient': '1299018'
encounters = search3.perform_resources(smart.server)
# print(encounters.as_json())

for e in encounters:
    print(e.type[0].text)


