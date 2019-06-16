from config import app
from controller_functions import index, register, bright_ideas, login, logout, post_idea, user_view, like, delete, idea_view

app.add_url_rule("/", view_func=index)
app.add_url_rule("/register", view_func=register, methods=['POST'])
app.add_url_rule("/login", view_func=login, methods=['POST'])
app.add_url_rule("/logout", view_func=logout)
app.add_url_rule("/bright_ideas", view_func=bright_ideas)
app.add_url_rule("/post_idea", view_func=post_idea, methods=['POST'])
app.add_url_rule("/users/<id>", view_func=user_view)
app.add_url_rule("/like/<id>", view_func=like)
app.add_url_rule("/delete/<id>", view_func=delete)
app.add_url_rule("/bright_ideas/<id>", view_func=idea_view)