import test_connection.ClientConnector_test as ClientConnector_test
connector = ClientConnector_test()
connector.connect(service="smart", connection_type="source")
smart = connector.source_client

test_patient = {
    "resourceType": "Patient",
    "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">John Doe (male), born 1990-01-01</div>"
    },
    "name": [{"use": "official", "family": "Doe", "given": ["John"]}],
    "gender": "male",
    "birthDate": "1990-01-01"
}

response = connector.post_to_target('Patient', test_patient)
print(response.status_code)
print(response.json())