from flask_sqlalchemy import SQLAlchemy
from flask import Flask,render_template,request,redirect,abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy()

db.init_app(app)
@app.before_first_request
def create_table():
    db.create_all()


#Create Data
class EmployeeModel(db.Model):
    __tablename = 'Table'
    id = db.Column(db.Integer,primary_key=True)
    employee_id = db.Column(db.Integer(),unique = True)
    name = db.Column(db.String())
    age = db.Column(db.Integer())
    position = db.Column(db.String(80))

    def __init__(self,employee_id,name,age,position):
        self.employee_id = employee_id
        self.name = name
        self.age = age
        self.position = position

    def __repr__(self):
        return f"{self.name}:{self.employee_id}"

# Created Data Done
@app.route('/data/create' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')
 
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        name = request.form['name']
        age = request.form['age']
        position = request.form['position']
        employee = EmployeeModel(employee_id=employee_id, name=name, age=age, position = position)
        db.session.add(employee)
        db.session.commit()
        EmployeeModel.query.all()
        return render_template('data.html',employee=employee)
 
# Retrieve All Data
@app.route('/')
@app.route('/data')
def RetrieveList():
    employees = EmployeeModel.query.all()
    return render_template('datalist.html',employees = employees)
 
# Retrieve single Data
@app.route('/data/<int:id>')
def RetrieveEmployee(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if employee:
        return render_template('data.html', employee = employee)
    return f"Employee with id ={id} Doenst exist"
 
 
@app.route('/update/<int:id>',methods = ['GET','POST'])
def update(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()
            name = request.form['name']
            age = request.form['age']
            position = request.form['position']
            employee = EmployeeModel(employee_id=id, name=name, age=age, position = position)
            db.session.add(employee)
            db.session.commit()
            return redirect(f'/data/{id}')
        return redirect('/')
 
    return render_template('update.html', employee = employee)
 
 
@app.route('/delete/<int:id>')
def delete(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    db.session.delete(employee)
    db.session.commit()
    return redirect("/data")
if __name__ == '__main__':
    app.run(debug=True)