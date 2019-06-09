from config import app
from controller_functions import index

app.add_url_rule("/", view_func=index)