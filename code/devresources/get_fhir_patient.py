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
#smart.authorize_url

#struct = {'identifier': 'JP123456789'}

# patient = p.Patient.read('1349276', smart.server)
#search = p.Patient.where(struct=struct)
# patient = search.perform(smart.server).entry[0].resource
# patient = search.perform_resources(smart.server)[0]
search = p.Patient.where(struct={'family': 'Smith'})

if len(search.perform_resources(smart.server)) > 0:
    for patient in search.perform_resources(smart.server):
        #patient = search.perform_resources(smart.server)[0]
        #print(patient)
        print(smart.human_name(patient.name[0]))
        print(patient.id)
        if patient.birthDate:
            print(patient.birthDate.isostring)

        print(f"resource_type:{search.resource_type.resource_type}")
        checkpoint = 0
        if patient.address:
            print(patient.id)
            #print(f"Patient with address:{patient.as_json()}")
            checkpoint += 1
            #Check medication history
            search_med = MedicationRequest.where(struct={'patient': patient.id, '_count': '100'})
            #medlist = search_med.perform_resources(smart.server)

            parts = []
            parts.append(fparam('patient',patient.id).as_parameter())
            #resource_type.resource_type: Encounter
            #Encounter
            construct_res='{}?{}'.format(search_med.resource_type.resource_type, '&'.join(parts))
            #search2.resource_type.resource_type

            res2 = smart.server.request_json(construct_res)


            if res2:
                if res2.get('entry') and len(res2.get('entry'))>1:
                    print("medlist:\n")
                    print(res2)
                    checkpoint += 1
            if checkpoint >=2:
                break
    print("\n\n\n##########################\n Test Encounter")
    struct_search = {'patient': patient.id, '_count': '10'}
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
search3 = Encounter.where(struct={'patient': '41177'})
#'patient': '1299018'
encounters = search3.perform_resources(smart.server)
# print(encounters.as_json())

for e in encounters:
    print(e.type[0].text)


#PatientFinder = p.Patient.where(struct={'family': 'Smith'})

#patient = PatientFinder.find_by_id(
#    "113017",
#    first=True
#)
patient = p.Patient.read('18076', smart.server)
print(patient.as_json())

print(patient.telecom[0].system)