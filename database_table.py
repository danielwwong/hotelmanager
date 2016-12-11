import os, sqlite3
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'hotel_manager.sqlite')

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
    cardNo = db.Column(db.SmallInteger)
    memberNo = db.Column(db.SmallInteger)

class Order(db.Model):
    __tablename__ = 'Orders'
    orderNo = db.Column(db.SmallInteger, primary_key = True)
    roomNo = db.Column(db.SmallInteger)
    customer = db.Column(db.String(30))
    checkInDate = db.Column(db.SmallInteger)
    checkOutDate = db.Column(db.SmallInteger)
    price = db.Column(db.Float)
    pointChange = db.Column(db.SmallInteger)
    cashierNo = db.Column(db.SmallInteger)

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
    ssn = db.Column(db.SmallInteger)
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
    staffNo = db.Column(db.SmallInteger)
    roomNo = db.Column(db.SmallInteger)
    linens = db.Column(db.String(10))
    lQty = db.Column(db.SmallInteger)
    lType = db.Column(db.String(10))
    reusable = db.Column(db.Boolean)
    cost = db.Column(db.Float)
    date = db.Column(db.SmallInteger)

class Public_Equipment_Repair(db.Model):
    __tablename__ = 'Public_Equipment_Repair'
    record = db.Column(db.String(10), primary_key = True)
    staffNo = db.Column(db.SmallInteger)
    equipName = db.Column(db.String(10))
    equipID = db.Column(db.SmallInteger)
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

@app.route('/')
def hello():
    return render_template('hello.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/booking', methods = ['GET', 'POST'])
def booking():
    if request.method == 'GET':
        return render_template('booking.html')
    else:
        info = 1
        return render_template('booking.html', information = info)

@app.route('/bus')
def bus():
    sqlite_file = os.path.join(basedir, 'hotel_manager.sqlite')
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    cursor.execute('select * from Buses')
    data = cursor.fetchall()
    conn.close()
    return render_template('bus.html', items = data)

@app.route('/manager')
def manager():
    return render_template('manager.html')

@app.route('/carrental')
def carrental():
    return render_template('carrental.html')

@app.route('/carbooking')
def carbooking():
    return render_template('carbooking.html')

@app.route('/membership')
def membership():
    sqlite_file = os.path.join(basedir, 'hotel_manager.sqlite')
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    cursor.execute('select * from Deal')
    data = cursor.fetchall()
    conn.close()
    return render_template('membership.html', items = data)

@app.route('/orderspageofemployee', methods = ['GET', 'POST'])
def orderspageofemployee():
    if request.method == 'GET':
        return render_template('orderspageofemployee.html')
    else:
        sqlite_file = os.path.join(basedir, 'hotel_manager.sqlite')
        orderNo = request.form['orderNo']
        if orderNo == 'all':
            conn = sqlite3.connect(sqlite_file)
            cursor = conn.cursor()
            cursor.execute('select * from Orders')
            data = cursor.fetchall()
            conn.close()
            return render_template('orderspageofemployee.html', items = data)
        else:
            try:
                orders = Orders.query.filter_by(orderNo = orderNo).first()
            except:
                return None
            if orders is None:
                info = 2
                return render_template('orderspageofemployee.html', information = info)
            else:
                conn = sqlite3.connect(sqlite_file)
                cursor = conn.cursor()
                sql_query = "select * from Orders where orderNo = " + "'" + orderNo + "'"
                cursor.execute(sql_query)
                data = cursor.fetchall()
                conn.close()
                return render_template('orderspageofemployee.html', items = data)

@app.route('/roomspageofemployee', methods = ['GET', 'POST'])
def roomspageofemployee():
    if request.method == 'GET':
        return render_template('roomspageofemployee.html')
    else:
        sqlite_file = os.path.join(basedir, 'hotel_manager.sqlite')
        roomNo = request.form['roomNo']
        if roomNo == 'all':
            conn = sqlite3.connect(sqlite_file)
            cursor = conn.cursor()
            cursor.execute('select * from Rooms')
            data = cursor.fetchall()
            conn.close()
            return render_template('roomspageofemployee.html', items = data)
        else:
            try:
                rooms = Rooms.query.filter_by(roomNo = roomNo).first()
            except:
                return None
            if rooms is None:
                info = 2
                return render_template('roomspageofemployee.html', information = info)
            else:
                conn = sqlite3.connect(sqlite_file)
                cursor = conn.cursor()
                sql_query = "select * from Rooms where roomNo = " + "'" + roomNo + "'"
                cursor.execute(sql_query)
                data = cursor.fetchall()
                conn.close()
                return render_template('roomspageofemployee.html', items = data)

@app.route('/maintainspageofemployee', methods = ['GET', 'POST'])
def maintainspageofemployee():
    if request.method == 'GET':
        return render_template('maintainspageofemployee.html')
    else:
        sqlite_file = os.path.join(basedir, 'hotel_manager.sqlite')
        record = request.form['record']
        if record == 'all':
            conn = sqlite3.connect(sqlite_file)
            cursor = conn.cursor()
            cursor.execute('select * from Maintains')
            data = cursor.fetchall()
            conn.close()
            return render_template('maintainspageofemployee.html', items = data)
        else:
            try:
                maintains = Maintains.query.filter_by(record = record).first()
            except:
                return None
            if maintains is None:
                info = 2
                return render_template('maintainspageofemployee.html', information = info)
            else:
                conn = sqlite3.connect(sqlite_file)
                cursor = conn.cursor()
                sql_query = "select * from Maintains where record = " + "'" + record + "'"
                cursor.execute(sql_query)
                data = cursor.fetchall()
                conn.close()
                return render_template('maintainspageofemployee.html', items = data)

@app.route('/equippageofemployee', methods = ['GET', 'POST'])
def equippageofemployee():
    if request.method == 'GET':
        return render_template('equippageofemployee.html')
    else:
        sqlite_file = os.path.join(basedir, 'hotel_manager.sqlite')
        record = request.form['record']
        if record == 'all':
            conn = sqlite3.connect(sqlite_file)
            cursor = conn.cursor()
            cursor.execute('select * from Public_Equipment_Repair')
            data = cursor.fetchall()
            conn.close()
            return render_template('equippageofemployee.html', items = data)
        else:
            try:
                equip = Public_Equipment_Repair.query.filter_by(record = record).first()
            except:
                return None
            if equip is None:
                info = 2
                return render_template('equippageofemployee.html', information = info)
            else:
                conn = sqlite3.connect(sqlite_file)
                cursor = conn.cursor()
                sql_query = "select * from Public_Equipment_Repair where record = " + "'" + record + "'"
                cursor.execute(sql_query)
                data = cursor.fetchall()
                conn.close()
                return render_template('equippageofemployee.html', items = data)

@app.route('/membershiptable', methods = ['GET', 'POST'])
def membershiptable():
    if request.method == 'GET':
        return render_template('membershiptable.html')
    else:
        sqlite_file = os.path.join(basedir, 'hotel_manager.sqlite')
        memberNo = request.form['memberNo']
        if memberNo == 'all':
            conn = sqlite3.connect(sqlite_file)
            cursor = conn.cursor()
            cursor.execute('select * from Membership')
            data = cursor.fetchall()
            conn.close()
            return render_template('membershiptable.html', items = data)
        else:
            try:
                membership = Membership.query.filter_by(memberNo = memberNo).first()
            except:
                return None
            if membership is None:
                info = 2
                return render_template('membershiptable.html', information = info)
            else:
                conn = sqlite3.connect(sqlite_file)
                cursor = conn.cursor()
                sql_query = "select * from Membership where memberNo = " + "'" + memberNo + "'"
                cursor.execute(sql_query)
                data = cursor.fetchall()
                conn.close()
                return render_template('membershiptable.html', items = data)

@app.route('/staffRead', methods = ['GET', 'POST'])
def staffRead():
    if request.method == 'GET':
        return render_template('staffRead.html')
    else:
        sqlite_file = os.path.join(basedir, 'hotel_manager.sqlite')
        staffNo = request.form['staffNo']
        if staffNo == 'all':
            conn = sqlite3.connect(sqlite_file)
            cursor = conn.cursor()
            cursor.execute('select * from Staff')
            data = cursor.fetchall()
            conn.close()
            return render_template('staffRead.html', items = data)
        else:
            try:
                staff = Staff.query.filter_by(staffNo = staffNo).first()
            except:
                return None
            if staff is None:
                info = 2
                return render_template('staffRead.html', information = info)
            else:
                conn = sqlite3.connect(sqlite_file)
                cursor = conn.cursor()
                sql_query = "select * from Staff where staffNo = " + "'" + staffNo + "'"
                cursor.execute(sql_query)
                data = cursor.fetchall()
                conn.close()
                return render_template('staffRead.html', items = data)

@app.route('/busesRead', methods = ['GET', 'POST'])
def busesRead():
    if request.method == 'GET':
        return render_template('busesRead.html')
    else:
        sqlite_file = os.path.join(basedir, 'hotel_manager.sqlite')
        licenseNo = request.form['license']
        if licenseNo == 'all':
            conn = sqlite3.connect(sqlite_file)
            cursor = conn.cursor()
            cursor.execute('select * from Buses')
            data = cursor.fetchall()
            conn.close()
            return render_template('busesRead.html', items = data)
        else:
            try:
                buses = Buses.query.filter_by(licenseNo = licenseNo).first()
            except:
                return None
            if buses is None:
                info = 2
                return render_template('busesRead.html', information = info)
            else:
                conn = sqlite3.connect(sqlite_file)
                cursor = conn.cursor()
                sql_query = "select * from Buses where licenseNo = " + "'" + licenseNo + "'"
                cursor.execute(sql_query)
                data = cursor.fetchall()
                conn.close()
                return render_template('busesRead.html', items = data)

@app.route('/rentCarRead', methods = ['GET', 'POST'])
def rentCarRead():
    if request.method == 'GET':
        return render_template('rentCarRead.html')
    else:
        sqlite_file = os.path.join(basedir, 'hotel_manager.sqlite')
        VIN = request.form['VIN']
        if VIN == 'all':
            conn = sqlite3.connect(sqlite_file)
            cursor = conn.cursor()
            cursor.execute('select * from Rent_Car')
            data = cursor.fetchall()
            conn.close()
            return render_template('rentCarRead.html', items = data)
        else:
            try:
                rentCar = Rent_Car.query.filter_by(VIN = VIN).first()
            except:
                return None
            if rentCar is None:
                info = 2
                return render_template('rentCarRead.html', information = info)
            else:
                conn = sqlite3.connect(sqlite_file)
                cursor = conn.cursor()
                sql_query = "select * from Rent_Car where VIN = " + "'" + VIN + "'"
                cursor.execute(sql_query)
                data = cursor.fetchall()
                conn.close()
                return render_template('rentCarRead.html', items = data)

@app.route('/dealRead', methods = ['GET', 'POST'])
def dealRead():
    if request.method == 'GET':
        return render_template('dealRead.html')
    else:
        sqlite_file = os.path.join(basedir, 'hotel_manager.sqlite')
        dealNo = request.form['dealNo']
        if dealNo == 'all':
            conn = sqlite3.connect(sqlite_file)
            cursor = conn.cursor()
            cursor.execute('select * from Deal')
            data = cursor.fetchall()
            conn.close()
            return render_template('dealRead.html', items = data)
        else:
            try:
                deal = Deal.query.filter_by(dealNo = dealNo).first()
            except:
                return None
            if deal is None:
                info = 2
                return render_template('dealRead.html', information = info)
            else:
                conn = sqlite3.connect(sqlite_file)
                cursor = conn.cursor()
                sql_query = "select * from Deal where dealNo = " + "'" + dealNo + "'"
                cursor.execute(sql_query)
                data = cursor.fetchall()
                conn.close()
                return render_template('dealRead.html', items = data)

@app.route('/customer')
def customer():
    return render_template('customer.html')

@app.route('/roominformation')
def roominformation():
    return render_template('roominformation.html')

@app.route('/employee')
def employee():
    return render_template('employee.html')

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
        try:
            db.session.add(customers)
            db.session.commit()
            info = 1
            return render_template('create.html', information = info)
        except:
            info = 2
            return render_template('create.html', information = info)

@app.route('/delete', methods = ['GET', 'POST'])
def delete():
    if request.method == 'GET':
        return render_template('delete.html')
    else:
        ssn = request.form['ssn']
        try:
            customers = Customers.query.filter_by(ssn = ssn).first()
        except:
            return None
        if customers is None:
            info = 2
            return render_template('delete.html', information = info)
        else:
            Customers.query.filter_by(ssn = ssn).delete()
            db.session.commit()
            info = 1
            return render_template('delete.html', information = info)

@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'GET':
        return render_template('update.html')
    else:
        ssn = request.form['ssn']
        name = request.form['name']
        address = request.form['address']
        gender = request.form['gender']
        phone = request.form['phone']
        dob = request.form['dob']
        cardNo = request.form['cardNo']
        memberNo = request.form['memberNo']
        try:
            customers = Customers.query.filter_by(ssn = ssn).first()
        except:
            return None
        if customers is None:
            info = 2
            return render_template('update.html', information = info)
        else:
            customers.name = name
            customers.address = address
            customers.gender = gender
            customers.phone = phone
            customers.dob = dob
            customers.cardNo = cardNo
            customers.memberNo = memberNo
            db.session.commit()
            info = 1
            return render_template('update.html', information = info)

@app.route('/read', methods = ['GET', 'POST'])
def read():
    if request.method == 'GET':
        return render_template('read.html')
    else:
        sqlite_file = os.path.join(basedir, 'hotel_manager.sqlite')
        ssn = request.form['ssn']
        if ssn == 'all':
            conn = sqlite3.connect(sqlite_file)
            cursor = conn.cursor()
            cursor.execute('select * from Customers')
            data = cursor.fetchall()
            conn.close()
            return render_template('read.html', items = data)
        else:
            try:
                customers = Customers.query.filter_by(ssn = ssn).first()
            except:
                return None
            if customers is None:
                info = 2
                return render_template('read.html', information = info)
            else:
                conn = sqlite3.connect(sqlite_file)
                cursor = conn.cursor()
                sql_query = "select * from Customers where ssn = " + "'" + ssn + "'"
                cursor.execute(sql_query)
                data = cursor.fetchall()
                conn.close()
                return render_template('read.html', items = data)

@app.route('/query', methods = ['GET', 'POST'])
def query():
    if request.method == 'GET':
        return render_template('query.html')
    else:
        sqlite_file = os.path.join(basedir, 'hotel_manager.sqlite')
        query = request.form['query']
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()
        cursor.execute(query)
        column = cursor.description
        data = cursor.fetchall()
        conn.close()
        return render_template('query.html', names = column, items = data)

if __name__ == '__main__':
    #manager.debug = True
    app.run(host = '0.0.0.0', port = 8000)
    manager.run()
