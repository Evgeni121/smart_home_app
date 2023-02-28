from app import application as app
from smart_home import server_api

app = app.SmartHome(server_api)
app.run()
