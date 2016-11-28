import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'hotel_manager.sqlite')
#app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

manager = Manager(app)
db = SQLAlchemy(app)

class Customers(db.Model):
    __tablename__ = 'Customers'
    ssn = db.Column(db.String(30), primary_key = True)
    name = db.Column(db.String(30))
    address = db.Column(db.String(300))
    gender = db.Column(db.String(1))
    phone = db.Column(db.SmallInteger)
    dob = db.Column(db.SmallInteger)
    cardNo = db.Column(db.SmallInteger, unique = True)
    memberNo = db.Column(db.SmallInteger, unique = True)

class Order(db.Model):
    __tablename__ = 'Order'
    orderNo = db.Column(db.SmallInteger, primary_key = True)
    roomNo = db.Column(db.SmallInteger, unique = True)
    customer = db.Column(db.String(30))
    checkInDate = db.Column(db.SmallInteger)
    checkOutDate = db.Column(db.SmallInteger)
    price = db.Column(db.Float)
    pointCharge = db.Column(db.SmallInteger)
    cashierNo = db.Column(db.SmallInteger, unique = True)

class Rooms(db.Model):
    __tablename__ = 'Rooms'
    roomNo = db.Column(db.SmallInteger, primary_key = True)
    inRoomBill = db.Column(db.Float)
    capacity = db.Column(db.SmallInteger)
    bedsNo = db.Column(db.SmallInteger)
    type = db.Column(db.String(10))
    status = db.Column(db.String(30))

class Staff(db.Model):
    __tablename__ = 'Staff'
    ssn = db.Column(db.SmallInteger, unique = True)
    staffNo = db.Column(db.SmallInteger, primary_key = True)
    position = db.Column(db.String(30))
    workYear = db.Column(db.SmallInteger)
    name = db.Column(db.String(30))
    address = db.Column(db.String(300), nullable = True)
    phone = db.Column(db.SmallInteger, nullable = True)
    gender = db.Column(db.String(1))
    salary = db.Column(db.Float)

class Maintains(db.Model):
    __tablename__ = 'Maintains'
    record = db.Column(db.String(10), primary_key = True)
    staffNo = db.Column(db.SmallInteger, unique = True)
    roomNo = db.Column(db.SmallInteger, unique = True)
    linens = db.Column(db.String(10))
    lQty = db.Column(db.SmallInteger)
    lType = db.Column(db.String(10))
    reusable = db.Column(db.Boolean)
    cost = db.Column(db.Float)
    date = db.Column(db.SmallInteger)

class Public_Equipment_Repair(db.Model):
    __tablename__ = 'Public_Equipment_Repair'
    record = db.Column(db.String(10), primary_key = True)
    staffNo = db.Column(db.SmallInteger, unique = True)
    equipName = db.Column(db.String(10))
    equipID = db.Column(db.SmallInteger, unique = True)
    cost = db.Column(db.Float)
    date = db.Column(db.SmallInteger)

class Buses(db.Model):
    __tablename__ = 'Buses'
    VIN = db.Column(db.String(17), primary_key = True)
    lines = db.Column(db.String(10))
    destination = db.Column(db.String(20))
    departTime = db.Column(db.SmallInteger)
    carType = db.Column(db.String(10))
    capacity = db.Column(db.SmallInteger)
    price = db.Column(db.Float)
    takenBy = db.Column(db.String(30))

class Rent_Car(db.Model):
    __tablename__ = 'Rent_Car'
    VIN = db.Column(db.String(17), primary_key = True)
    company = db.Column(db.String(20))
    carType = db.Column(db.String(10))
    capacity = db.Column(db.SmallInteger)
    priceTotal = db.Column(db.Float)
    rentDate = db.Column(db.SmallInteger)
    returnDate = db.Column(db.SmallInteger)
    rentPlace = db.Column(db.String(20))
    returnPlace = db.Column(db.String(20))
    rentBy = db.Column(db.String(30))

class Membership(db.Model):
    __tablename__ = 'Membership'
    memberNo = db.Column(db.SmallInteger, primary_key = True)
    name = db.Column(db.String(30))
    points = db.Column(db.SmallInteger)
    level = db.Column(db.String(10))
    beginDate = db.Column(db.SmallInteger)
    endDate = db.Column(db.SmallInteger)

class Deal(db.Model):
    __tablename__ = 'Deal'
    activity = db.Column(db.String(30))
    joinLevel = db.Column(db.String(10))
    capacity = db.Column(db.SmallInteger)
    beginDate = db.Column(db.SmallInteger)
    endDate = db.Column(db.SmallInteger)
    dealNo = db.Column(db.SmallInteger, primary_key = True)

@app.route('/create', methods = ['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
    else:
        ssn = request.form['ssn']
        name = request.form['name']
        address = request.form['address']
        gender = request.form['gender']
        phone = request.form['phone']
        dob = request.form['dob']
        cardNo = request.form['cardNo']
        memberNo = request.form['memberNo']
        customers = Customers(ssn = ssn, name = name, address = address, gender = gender, phone = phone, dob = dob, cardNo = cardNo, memberNo = memberNo)
        db.session.add(customers)
        db.session.commit()
        return redirect('/create')

if __name__ == '__main__':
    #manager.debug = True
    app.run(host = '0.0.0.0', port = 8000)
    manager.run()
