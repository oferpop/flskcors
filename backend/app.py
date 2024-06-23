from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutorial.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(50))
    model = db.Column(db.String(50))
    brand = db.Column(db.String(50))

    def __repr__(self):
        return f"<Car {self.id}: {self.color}, {self.model}, {self.brand}>"

@app.route("/")
def hello_world():
    return jsonify({"message": "Hello, World!"})

@app.route("/new_car", methods=["POST"])
def add_car():
    if request.headers.get("Content-Type") == "application/json":
        data = request.get_json()
        if data and "color" in data and "model" in data and "brand" in data:
            new_car = Car(color=data["color"], model=data["model"], brand=data["brand"])
            db.session.add(new_car)
            db.session.commit()
            return jsonify({"message": "New car added"})
        else:
            return jsonify({"error": "Invalid data"}), 400
    else:
        return jsonify({"error": "Unsupported Media Type"}), 415

@app.route("/get_cars", methods=["GET"])
def get_all_cars():
    cars = Car.query.all()
    cars_list = [{"id": car.id, "color": car.color, "model": car.model, "brand": car.brand} for car in cars]
    return jsonify(cars_list)

@app.route("/update_car/<int:car_id>", methods=["PUT"])
def update_car(car_id):
    if request.headers.get("Content-Type") == "application/json":
        data = request.get_json()
        if not data:
            return jsonify({"error": "No fields provided for update"}), 400
        
        car = Car.query.get(car_id)
        if not car:
            return jsonify({"error": "Car not found"}), 404

        if "color" in data:
            car.color = data["color"]
        if "model" in data:
            car.model = data["model"]
        if "brand" in data:
            car.brand = data["brand"]
        
        db.session.commit()
        return jsonify({"message": f"Car with ID {car_id} updated successfully"})
    else:
        return jsonify({"error": "Unsupported Media Type"}), 415

@app.route("/delete_car/<int:car_id>", methods=["DELETE"])
def delete_car(car_id):
    car = Car.query.get(car_id)
    if not car:
        return jsonify({"error": "Car not found"}), 404

    db.session.delete(car)
    db.session.commit()
    return jsonify({"message": "Car deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)
