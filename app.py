from flask import Flask, render_template, request, url_for, redirect

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_db.db'
db = SQLAlchemy(app)


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(50), nullable=False)
    district = db.Column(db.String(50), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    address = db.relationship(Address)

    def full_address(self):
        return f"{self.address.state}, {self.address.district}, {self.address.pincode}"


#Retreiving from the database
@app.route("/")
@app.route("/students")
def index():
    student_obj = Student.query.all()
    address_obj = Address.query.all()
    # print(url_for("add_student"))
    return render_template('index.html', students=student_obj, address=address_obj)


#creating 
@app.post("/add_student")
def add_student():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        address_id = request.form['address_id']
        
        student = Student(id=id, name=name, address_id=address_id)

        db.session.add(student)

        db.session.commit()
        
        return redirect(url_for("index"))
    

#deleting
@app.route("/delete_student/<id>", methods=['GET', 'POST'])
def delete_student(id):
    object = Student.query.get(id)
    db.session.delete(object)
    db.session.commit()

    return redirect(url_for("index"))


#updating
@app.route("/update/<id>", methods=['GET','POST'])
def update_student(id):
    if request.method == 'POST':
        student = Student.query.get(id)
        student.name = request.form['name']
        student.address_id = request.form['address_id']
        db.session.commit()
        return redirect(url_for("index"))
    
    address = Address.query.all()
    student = Student.query.get(id)
    return render_template('update.html', student=student, address=address)



@app.route("/address")
def address():
    address_obj = Address.query.all()   
    return render_template('address.html', address1=address_obj)






if __name__ == "__main__":
    app.run(debug=True)