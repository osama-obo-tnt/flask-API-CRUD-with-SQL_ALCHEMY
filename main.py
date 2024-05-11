from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///flask.db'
app.json.sort_keys = False
db = SQLAlchemy(app)

class DB(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    name  = db.Column(db.String, nullable = False)
    age = db.Column(db.Integer, nullable = False)



@app.route("/post", methods = ["POST"])
def add_user():
    name = request.json["name"]
    age = request.json["age"]
    if not name or not age :
        return "Error : Name or age missing"
    else:
        try:
            user = DB(name=name, age=age)
            db.session.add(user)
            db.session.commit()
            return f"{name} added successfully"
        except Exception as e:
            return f"Error : {e}"
    return "function executed successfully"

@app.route("/read")
def show_users():
    users = DB.query.all()
    data = [{"name":i.name,"age":i.age} for i in users]
    return jsonify(data)

@app.route("/read/<int:user_id>")
def show_user(user_id):
    if not user_id:
        return "Missing user_id"
    else:
        user = DB.query.filter_by(user_id=user_id).first()
        data = {"name":user.name, "age":user.age}
        return data
    

@app.route("/update/<int:user_id>", methods = ["PUT"])
def update(user_id):
    user = DB.query.filter_by(user_id=user_id).first()
    if user:
        data = request.json
        if "name" in data:
            user.name = data["name"]
        if "age" in data:
            user.age = data["age"]
        db.session.commit()
        return "User updated successfully"
    else:
        return "There is some error "

@app.route("/delete/<int:user_id>", methods = ["DELETE"])
def del_user(user_id):
    user = DB.query.filter_by(user_id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return f"{user.name} deleted successfully"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug = True)
