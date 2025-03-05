from fhirclient import client
from fhirclient.models.fhirsearch import FHIRSearch
import yaml
import json
from fhirclient.models.patient import Patient


class ClientConnector_test():
    """An object to host two FHIR clients to perform data exchange.
    """

    def __init__(self, *args, **kwargs):
        self.source_client = None
        self.target_client = None
        self.client_dict = dict()

        with open('server_config.yml') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        self.server_config = config

    def connect(self, service, connection_type):
        settings = self.server_config.get(service)

        if connection_type == 'source':
            self.source_client = client.FHIRClient(settings=settings)
            self.client_dict[service] = self.source_client
        elif connection_type == 'target':
            self.target_client = client.FHIRClient(settings=settings)
            self.client_dict[service] = self.target_client

    def reset(self):
        self.__init__()

    def post_to_target(self, resource_type, resource_json):

        url = '/'.join([self.target_client.server.base_uri, resource_type])
        headers = {
            'Accept': 'application/fhir+json',
            'Accept-Charset': 'UTF-8',
            'Content-Type': 'application/fhir+json'
        }
        if not self.target_client.server.auth is not None and self.target_client.server.auth.can_sign_headers():
            headers = self.target_client.server.auth.signed_headers(headers)

        # perform the request but intercept 401 responses, raising our own Exception
        res = self.target_client.server.session.post(
            url, headers=headers, data=json.dumps(resource_json))
        return res


connector = ClientConnector_test()
connector.connect(service="smart", connection_type="source")
smart = connector.source_client

#patient = Patient.read("18076", smart.server)

search = Patient.where(struct={})
bundle = search.perform(smart.server)  # Perform the search and get the Bundle

if bundle.entry:
    for entry in bundle.entry:
        patient = entry.resource
        if patient.text and hasattr(patient.text, 'div'):
            print(f"Patient ID: {patient.id}, Name: {patient.name[0].given[0]} {patient.name[0].family}")
        else:
            print(f"Patient ID: {patient.id} has missing or invalid 'text.div' field")
else:
    print("No patients found in the bundle.")

#patients = search.perform_resources(smart.server)
#for patient in patients:
#    print(patient.id)
#    break


settings = {
    'app_id': 'testing-app-id',
    'api_base': 'http://hapi.fhir.org/baseDstu3/',
    'strict': False  # Disable strict validation
}

smart2 = client.FHIRClient(settings=settings)
search2 = Patient.where(struct={})
bundle2 = search.perform(smart2.server)  # Perform the search and get the Bundle

if bundle2.entry:
    for entry in bundle.entry:
        patient = entry.resource
        if patient.text and hasattr(patient.text, 'div'):
            print(f"Patient ID: {patient.id}, Name: {patient.name[0].given[0]} {patient.name[0].family}")
        else:
            print(f"Patient ID: {patient.id} has missing or invalid 'text.div' field")
else:
    print("No patients found in the bundle.")