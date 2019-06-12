from config import app
from controller_functions import index, register, bright_ideas

app.add_url_rule("/", view_func=index)
app.add_url_rule("/register", view_func=register, methods=['POST'])
app.add_url_rule("/bright_ideas", view_func=bright_ideas)