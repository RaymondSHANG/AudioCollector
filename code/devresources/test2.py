from fhirclient import client
## Repeat
from fhirclient.models.fhirsearch import FHIRSearchParam as fparam
#import fhirclient.models.bundle.Bundle as fBundle
from fhirclient.models.bundle import Bundle
from fhirclient.models.encounter import Encounter
from fhirclient.models import patient as p
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



search2 = Encounter.where(struct={'patient': '1299018'})

parts = []
parts.append(fparam('patient','1299018').as_parameter())
#resource_type.resource_type: Encounter
#Encounter
construct_res='{}?{}'.format('Encounter', '&'.join(parts))
search2.resource_type.resource_type

res2 = smart.server.request_json(construct_res)
bundle2 = Bundle(res2) ## Error
#bundle.origin_server = smart.server
struct1 = {'identifier': 'http://hl7.org/fhir/sid/us-ssn|999-45-3776'}

search1 = p.Patient.where(struct=struct1)
parts1 = []
parts1.append(fparam('identifier','http://hl7.org/fhir/sid/us-ssn|999-45-3776').as_parameter())

construct_res1='{}?{}'.format(search1.resource_type.resource_type, '&'.join(parts1))
res1 = smart.server.request_json(construct_res1)
bundle1 = Bundle(res1) ## OK, no errors

from fhirclient.models.fhirabstractbase import FHIRAbstractBase
from fhirclient.models.fhirabstractbase import FHIRValidationError
FHIRAbstractBase(jsondict=res1, strict=True)
FHIRAbstractBase(jsondict=res2, strict=True)