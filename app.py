from apps import create_app

app = create_app()

from apps import db
from apps.appUser.models import User
from apps.appCar.models import Car, CarData, CarDataValue


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Car': Car, 'CarData': CarData, 'CarDataValue' : CarDataValue}

if __name__ == '__main__':
    app.run(debug=True)

