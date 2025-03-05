# FHIR server setting

```bash
smart:
  app_id: "testing-app-id"
  redirect_uri: "http://127.0.0.1:5000/oauth/smart/callback"
  api_base: 'http://hapi.fhir.org/baseDstu3/'
```

```bash
smart:
  app_id: "testing-app-id"
  redirect_uri: "http://127.0.0.1:5000/oauth/smart/callback"
  api_base: 'http://hapi.fhir.org/baseDstu3/'

```


1. Verify the Patient ID
Ensure that the patient ID 18076 exists on the FHIR server. You can do this by manually navigating to the URL in your browser:

```
http://hapi.fhir.org/baseDstu3/Patient/18076
```

If the patient does not exist, you will see a 404 error. If the patient exists, you should see the patient's JSON representation.

2. Search for Patients
```python
search = Patient.where(struct={})
patients = search.perform_resources(smart.server)
for patient in patients:
    print(patient.id)
```

3. Create a Test Patient

```python
test_patient = {
    "resourceType": "Patient",
    "name": [{"use": "official", "family": "Doe", "given": ["John"]}],
    "gender": "male",
    "birthDate": "1990-01-01"
}

response = connector.post_to_target('Patient', test_patient)
print(response.status_code)
print(response.json())
```