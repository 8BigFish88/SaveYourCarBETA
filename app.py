from app import create_app

app = create_app()

from app import db
from app.users.models import User
from app.cars.models import Car, CarData, CarDataValue


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Car': Car, 'CarData': CarData, 'CarDataValue' : CarDataValue}

if __name__ == '__main__':
    app.run(debug=True)

