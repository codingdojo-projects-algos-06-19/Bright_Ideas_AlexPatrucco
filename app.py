from config import app, db
from models import Users, Ideas

import routes

if __name__ == "__main__":
    app.run(debug=True)