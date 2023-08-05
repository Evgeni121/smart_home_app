from app import application as app
from smart_home import server_api
from smart_home import driver

app = app.SmartHome(server_api, driver)
app.run()
