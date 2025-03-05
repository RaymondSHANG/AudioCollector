import json
from fhirclient import client

# Initialize the FHIR client
settings = {
    'app_id': 'testing-app-id',
    'api_base': 'http://hapi.fhir.org/baseDstu3/'
}
smart = client.FHIRClient(settings=settings)

# Perform a raw search request
search_url = f"{smart.server.base_uri}Patient"
response = smart.server.session.get(search_url, headers={
    'Accept': 'application/fhir+json',
    'Accept-Charset': 'UTF-8'
})

# Check if the request was successful
if response.status_code == 200:
    bundle = response.json()  # Parse the JSON response
    if 'entry' in bundle:
        for entry in bundle['entry']:
            patient = entry['resource']
            print(json.dumps(patient, indent=2))
            # Check if the 'text' field exists and contains 'div'
            if 'text' in patient and 'div' in patient['text']:
                print(f"Patient ID: {patient['id']}, Name: {patient['name'][0]}") # Not all patients have family name in the record:{patient['name'][0]['family']}
            else:
                print(f"Patient ID: {patient['id']} has missing or invalid 'text.div' field")
    else:
        print("No patients found in the bundle.")
else:
    print(f"Failed to fetch patients. Status code: {response.status_code}")