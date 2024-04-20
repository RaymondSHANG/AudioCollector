# FHIR Patient Portal
This is a FHIR client web app built with Flask, a plug-and-play web app set to connect to [SMART App Launcher](https://launch.smarthealthit.org/) or other FHIR servers when configged correctly. A new patient could register and record his/her audio files to the server.

This app is built on top of fhir-flask-client-web-app, originally published in github(https://github.com/kelhwh/fhir-flask-client-web-app).
In Kelhwh's work, the app could do the FHIR data sharing work. In my work, I focused on audio file collection. I first updated and debug all codes so that it runs well in the latest versions. Then, I add addNews, audioRecording modules and integrate them to the app.

Login credentials for SMART App Launcher are prefilled.

## Initiation
```
python app.py
```

Go to http://127.0.0.1:5000/ and register a user with prefilled values and then login.

## References
1. fhirclient, https://pypi.org/project/fhirclient/
2. SMART on FHIR, https://github.com/smart-on-fhir
3. SMART on FHIR python client demo
, https://github.com/pete88b/smart-on-fhir-client-py-demo
4. fhir-flask-client-web-app,https://github.com/kelhwh/fhir-flask-client-web-app
5. SMART Launcher,https://launch.smarthealthit.org/
6. App Launch: Scopes and Launch Context,https://www.hl7.org/fhir/smart-app-launch/scopes-and-launch-context.html
7. Flask’s documentation, https://flask.palletsprojects.com/en/3.0.x/

