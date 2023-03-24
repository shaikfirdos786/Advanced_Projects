import random
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
API_KEY = "TopSecretAPIKey"


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        # Method 1.
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary
        #
        # # Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        # return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def get_random_cafe():
    all_cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(all_cafes)
    return jsonify(Cafe=random_cafe.to_dict())


@app.route("/all")
def all_cafes():
    all_cafes = db.session.query(Cafe).all()
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


# @app.route("/search/<location>")
# def required_cafe(location):
#     cafes = db.session.query(Cafe).all()
#     for cafe in cafes:
#         new_cafe = cafe.to_dict()
#         if new_cafe['location'] == location:
#             return jsonify(Cafe = new_cafe)
#         else:
#             return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})

#    SECOND METHOD
@app.route("/search")
def get_cafe_at_location():
    query_location = request.args.get("loc")
    cafe = db.session.query(Cafe).filter_by(location=query_location).first()
    if cafe:
        return jsonify(Cafe=cafe.to_dict())
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})


@app.route('/add', methods=["POST"])
def add_cafe():
    api_key = request.args.get('api-key')
    if api_key == API_KEY:
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("loc"),
            has_sockets=bool(request.form.get("sockets")),
            has_toilet=bool(request.form.get("toilet")),
            has_wifi=bool(request.form.get("wifi")),
            can_take_calls=bool(request.form.get("calls")),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price"),
        )
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={"Success": "Successfully added the new cafe."})
    else:
        return jsonify(response={"error": "Sorry! that's not allowed. Make sure you have the correct api_key."}), 403


@app.route('/update-price/<cafe_id>', methods=["PATCH"])
def Update_coffee_price(cafe_id):
    api_key = request.args.get('api-key')
    if api_key == API_KEY:
        cafe = Cafe.query.get(cafe_id)
        if cafe:
            new_price = request.args.get('new_price')
            cafe.coffee_price = new_price
            db.session.commit()
            ## Just add the code after the jsonify method. 200 = Ok
            return jsonify(response={"Success": "Successfully updated the price."}), 200
        else:
            # 404 = Resource not found
            return jsonify(error={"Not Found": "Sorry! a cafe with that id was not found in the database."}), 404
    else:
        return jsonify(response={"error": "Sorry! that's not allowed. Make sure you have the correct api_key."}), 403


@app.route('/report-closed/<cafe_id>', methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get('api-key')
    if api_key == API_KEY:
        cafe = Cafe.query.get(cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Cafe deleted from the database."})
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        return jsonify(response={"error": "Sorry! that's not allowed. Make sure you have the correct api_key."}), 403

## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
