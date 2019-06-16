from config import app
from controller_functions import index, register, bright_ideas, login, logout, post_idea

app.add_url_rule("/", view_func=index)
app.add_url_rule("/register", view_func=register, methods=['POST'])
app.add_url_rule("/login", view_func=login, methods=['POST'])
app.add_url_rule("/logout", view_func=logout)
app.add_url_rule("/bright_ideas", view_func=bright_ideas)
app.add_url_rule("/post_idea", view_func=post_idea, methods=['POST'])