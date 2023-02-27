from app import application as app
from smart_home import api

app = app.SmartHome(api)
app.run()
