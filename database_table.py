import os, sqlite3
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'hotel_manager.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

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

class Orders(db.Model):
    __tablename__ = 'Orders'
    orderNo = db.Column(db.SmallInteger, primary_key = True)
    roomNo = db.Column(db.SmallInteger)
    customer_ssn = db.Column(db.String(30))
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
    reusable = db.Column(db.SmallInteger)
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
    VIN = db.Column(db.String(17))
    SCHED = db.Column(db.String(10), primary_key = True)
    destination = db.Column(db.String(20))
    departTime = db.Column(db.SmallInteger)
    carType = db.Column(db.String(10))
    capacity = db.Column(db.SmallInteger)
    price = db.Column(db.Float)
    takenBy = db.Column(db.String(30))

class Rent_Car(db.Model):
    __tablename__ = 'Rent_Car'
    orderNo = db.Column(db.String(10), primary_key = True)
    VIN = db.Column(db.String(17))
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

@app.route('/signin', methods = ['GET', 'POST'])
def signin():
    PowerList=["3","1","2","3","1"]
    CodeList=["manager","customer","employee","admin","guest"]
    NameList=["manager","customer","employee","admin","guest"]
    if request.method == 'POST':
        Password=request.form['Password']
        Name=request.form['Name']
        for n in NameList:
            if n == Name:
                index = NameList.index(Name)
                if CodeList[index] == Password:
                    auth = PowerList[index]
                    if  auth == "1":
                        return render_template('customer.html')
                    elif  auth == "2":
                        return render_template('employee.html')
                    elif  auth == "3":
                        return render_template('manager.html')
                    else: 
                        return render_template('signin.html',errorInfo="1")


        return render_template('signin.html',errorInfo="1")
    else:
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
        SCHED = request.form['SCHED']
        if SCHED == 'all':
            conn = sqlite3.connect(sqlite_file)
            cursor = conn.cursor()
            cursor.execute('select * from Buses')
            data = cursor.fetchall()
            conn.close()
            return render_template('busesRead.html', items = data)
        else:
            try:
                buses = Buses.query.filter_by(SCHED = SCHED).first()
            except:
                return None
            if buses is None:
                info = 2
                return render_template('busesRead.html', information = info)
            else:
                conn = sqlite3.connect(sqlite_file)
                cursor = conn.cursor()
                sql_query = "select * from Buses where SCHED = " + "'" + SCHED + "'"
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
        orderNo = request.form['orderNo']
        if orderNo == 'all':
            conn = sqlite3.connect(sqlite_file)
            cursor = conn.cursor()
            cursor.execute('select * from Rent_Car')
            data = cursor.fetchall()
            conn.close()
            return render_template('rentCarRead.html', items = data)
        else:
            try:
                rentCar = Rent_Car.query.filter_by(orderNo = orderNo).first()
            except:
                return None
            if rentCar is None:
                info = 2
                return render_template('rentCarRead.html', information = info)
            else:
                conn = sqlite3.connect(sqlite_file)
                cursor = conn.cursor()
                sql_query = "select * from Rent_Car where orderNo = " + "'" + orderNo + "'"
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

@app.route('/ordersCreate', methods = ['GET', 'POST'])
def ordersCreate():
    if request.method == 'GET':
        return render_template('ordersCreate.html')
    else:
        orderNo = request.form['orderNo']
        roomNo = request.form['roomNo']
        customer_ssn = request.form['customer_ssn']
        checkInDate = request.form['checkInDate']
        checkOutDate = request.form['checkOutDate']
        price = request.form['price']
        pointChange = request.form['pointChange']
        cashierNo = request.form['cashierNo']
        orders = Orders(orderNo = orderNo, roomNo = roomNo, customer_ssn = customer_ssn, checkInDate = checkInDate, checkOutDate = checkOutDate, price = price, pointChange = pointChange, cashierNo = cashierNo)
        try:
            db.session.add(orders)
            db.session.commit()
            info = 1
            return render_template('ordersCreate.html', information = info)
        except:
            info = 2
            return render_template('ordersCreate.html', information = info)

@app.route('/roomsCreate', methods = ['GET', 'POST'])
def roomsCreate():
    if request.method == 'GET':
        return render_template('roomsCreate.html')
    else:
        roomNo = request.form['roomNo']
        inRoomBill = request.form['inRoomBill']
        capacity = request.form['capacity']
        bedsNo = request.form['bedsNo']
        type = request.form['type']
        status = request.form['status']
        rooms = Rooms(roomNo = roomNo, inRoomBill = inRoomBill, capacity = capacity, bedsNo = bedsNo, type = type, status = status)
        try:
            db.session.add(rooms)
            db.session.commit()
            info = 1
            return render_template('roomsCreate.html', information = info)
        except:
            info = 2
            return render_template('roomsCreate.html', information = info)

@app.route('/maintainsCreate', methods = ['GET', 'POST'])
def maintainsCreate():
    if request.method == 'GET':
        return render_template('maintainsCreate.html')
    else:
        record = request.form['record']
        staffNo = request.form['staffNo']
        roomNo = request.form['roomNo']
        linens = request.form['linens']
        lQty = request.form['lQty']
        lType = request.form['lType']
        reusable = request.form['reusable']
        cost = request.form['cost']
        date = request.form['date']
        maintains = Maintains(record = record, staffNo = staffNo, roomNo = roomNo, linens = linens, lQty = lQty, lType = lType, reusable = reusable, cost = cost, date = date)
        try:
            db.session.add(maintains)
            db.session.commit()
            info = 1
            return render_template('maintainsCreate.html', information = info)
        except:
            info = 2
            return render_template('maintainsCreate.html', information = info)

@app.route('/equipCreate', methods = ['GET', 'POST'])
def equipCreate():
    if request.method == 'GET':
        return render_template('equipCreate.html')
    else:
        record = request.form['record']
        staffNo = request.form['staffNo']
        equipName = request.form['equipName']
        equipID = request.form['equipID']
        cost = request.form['cost']
        date = request.form['date']
        equip = Public_Equipment_Repair(record = record, staffNo = staffNo, equipName = equipName, equipID = equipID, cost = cost, date = date)
        try:
            db.session.add(equip)
            db.session.commit()
            info = 1
            return render_template('equipCreate.html', information = info)
        except:
            info = 2
            return render_template('equipCreate.html', information = info)

@app.route('/membershipCreate', methods = ['GET', 'POST'])
def membershipCreate():
    if request.method == 'GET':
        return render_template('membershipCreate.html')
    else:
        memberNo = request.form['memberNo']
        name = request.form['name']
        points = request.form['points']
        level = request.form['level']
        beginDate = request.form['beginDate']
        endDate = request.form['endDate']
        membership = Membership(memberNo = memberNo, name = name, points = points, level = level, beginDate = beginDate, endDate = endDate)
        try:
            db.session.add(membership)
            db.session.commit()
            info = 1
            return render_template('membershipCreate.html', information = info)
        except:
            info = 2
            return render_template('membershipCreate.html', information = info)

@app.route('/staffCreate', methods = ['GET', 'POST'])
def staffCreate():
    if request.method == 'GET':
        return render_template('staffCreate.html')
    else:
        ssn = request.form['ssn']
        staffNo = request.form['staffNo']
        position = request.form['position']
        workYear = request.form['workYear']
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        gender = request.form['gender']
        salary = request.form['salary']
        staff = Staff(ssn = ssn, staffNo = staffNo, position = position,workYear = workYear, name = name, address = address, phone = phone, gender = gender, salary = salary)
        try:
            db.session.add(staff)
            db.session.commit()
            info = 1
            return render_template('staffCreate.html', information = info)
        except:
            info = 2
            return render_template('staffCreate.html', information = info)

@app.route('/busesCreate', methods = ['GET', 'POST'])
def busesCreate():
    if request.method == 'GET':
        return render_template('busesCreate.html')
    else:
        VIN = request.form['VIN']
        SCHED = request.form['SCHED']
        destination = request.form['destination']
        departTime = request.form['departTime']
        carType = request.form['carType']
        capacity = request.form['capacity']
        price = request.form['price']
        takenBy = request.form['takenBy']
        buses = Buses(VIN = VIN, SCHED = SCHED, destination = destination, departTime = departTime, carType = carType, capacity = capacity, price = price, takenBy = takenBy)
        try:
            db.session.add(buses)
            db.session.commit()
            info = 1
            return render_template('busesCreate.html', information = info)
        except:
            info = 2
            return render_template('busesCreate.html', information = info)

@app.route('/rentCarCreate', methods = ['GET', 'POST'])
def rentCarCreate():
    if request.method == 'GET':
        return render_template('rentCarCreate.html')
    else:
        orderNo = request.form['orderNo'];
        VIN = request.form['VIN']
        company = request.form['company']
        carType = request.form['carType']
        capacity = request.form['capacity']
        priceTotal = request.form['priceTotal']
        rentDate = request.form['rentDate']
        returnDate = request.form['returnDate']
        rentPlace = request.form['rentPlace']
        returnPlace = request.form['returnPlace']
        rentBy = request.form['rentBy']
        rentCar = Rent_Car(orderNo = orderNo, VIN = VIN, company = company, carType = carType, capacity = capacity, priceTotal = priceTotal, rentDate = rentDate, returnDate = returnDate, rentPlace = rentPlace, returnPlace = returnPlace, rentBy = rentBy)
        try:
            db.session.add(rentCar)
            db.session.commit()
            info = 1
            return render_template('rentCarCreate.html', information = info)
        except:
            info = 2
            return render_template('rentCarCreate.html', information = info)

@app.route('/dealCreate', methods = ['GET', 'POST'])
def dealCreate():
    if request.method == 'GET':
        return render_template('dealCreate.html')
    else:
        activity = request.form['activity']
        joinLevel = request.form['joinLevel']
        capacity = request.form['capacity']
        beginDate = request.form['beginDate']
        endDate = request.form['endDate']
        dealNo = request.form['dealNo']
        deal = Deal(activity = activity, joinLevel = joinLevel, capacity = capacity, beginDate = beginDate, endDate = endDate, dealNo = dealNo)
        try:
            db.session.add(deal)
            db.session.commit()
            info = 1
            return render_template('dealCreate.html', information = info)
        except:
            info = 2
            return render_template('dealCreate.html', information = info)

@app.route('/ordersDelete', methods = ['GET', 'POST'])
def ordersDelete():
    if request.method == 'GET':
        return render_template('ordersDelete.html')
    else:
        orderNo = request.form['orderNo']
        try:
            orders = Orders.query.filter_by(orderNo = orderNo).first()
        except:
            return None
        if orders is None:
            info = 2
            return render_template('ordersDelete.html', information = info)
        else:
            Orders.query.filter_by(orderNo = orderNo).delete()
            db.session.commit()
            info = 1
            return render_template('ordersDelete.html', information = info)

@app.route('/roomsDelete', methods = ['GET', 'POST'])
def roomsDelete():
    if request.method == 'GET':
        return render_template('roomsDelete.html')
    else:
        roomNo = request.form['roomNo']
        try:
            rooms = Rooms.query.filter_by(roomNo = roomNo).first()
        except:
            return None
        if rooms is None:
            info = 2
            return render_template('roomsDelete.html', information = info)
        else:
            Rooms.query.filter_by(roomNo = roomNo).delete()
            db.session.commit()
            info = 1
            return render_template('roomsDelete.html', information = info)

@app.route('/maintainsDelete', methods = ['GET', 'POST'])
def maintainsDelete():
    if request.method == 'GET':
        return render_template('maintainsDelete.html')
    else:
        record = request.form['record']
        try:
            maintains = Maintains.query.filter_by(record = record).first()
        except:
            return None
        if maintains is None:
            info = 2
            return render_template('maintainsDelete.html', information = info)
        else:
            maintains.query.filter_by(record = record).delete()
            db.session.commit()
            info = 1
            return render_template('maintainsDelete.html', information = info)

@app.route('/equipDelete', methods = ['GET', 'POST'])
def equipDelete():
    if request.method == 'GET':
        return render_template('equipDelete.html')
    else:
        record = request.form['record']
        try:
            equip = Public_Equipment_Repair.query.filter_by(record = record).first()
        except:
            return None
        if equip is None:
            info = 2
            return render_template('equipDelete.html', information = info)
        else:
            equip.query.filter_by(record = record).delete()
            db.session.commit()
            info = 1
            return render_template('equipDelete.html', information = info)

@app.route('/membershipDelete', methods = ['GET', 'POST'])
def membershipDelete():
    if request.method == 'GET':
        return render_template('membershipDelete.html')
    else:
        memberNo = request.form['memberNo']
        try:
            membership = Membership.query.filter_by(memberNo = memberNo).first()
        except:
            return None
        if membership is None:
            info = 2
            return render_template('membershipDelete.html', information = info)
        else:
            membership.query.filter_by(memberNo = memberNo).delete()
            db.session.commit()
            info = 1
            return render_template('membershipDelete.html', information = info)

@app.route('/staffDelete', methods = ['GET', 'POST'])
def staffDelete():
    if request.method == 'GET':
        return render_template('staffDelete.html')
    else:
        staffNo = request.form['staffNo']
        try:
            staff = Staff.query.filter_by(staffNo = staffNo).first()
        except:
            return None
        if staff is None:
            info = 2
            return render_template('staffDelete.html', information = info)
        else:
            staff.query.filter_by(staffNo = staffNo).delete()
            db.session.commit()
            info = 1
            return render_template('staffDelete.html', information = info)

@app.route('/busesDelete', methods = ['GET', 'POST'])
def busesDelete():
    if request.method == 'GET':
        return render_template('busesDelete.html')
    else:
        SCHED = request.form['SCHED']
        try:
            buses = Buses.query.filter_by(SCHED = SCHED).first()
        except:
            return None
        if buses is None:
            info = 2
            return render_template('busesDelete.html', information = info)
        else:
            buses.query.filter_by(SCHED = SCHED).delete()
            db.session.commit()
            info = 1
            return render_template('busesDelete.html', information = info)

@app.route('/rentCarDelete', methods = ['GET', 'POST'])
def rentCarDelete():
    if request.method == 'GET':
        return render_template('rentCarDelete.html')
    else:
        orderNo = request.form['orderNo']
        try:
            rentCar = Rent_Car.query.filter_by(orderNo = orderNo).first()
        except:
            return None
        if rentCar is None:
            info = 2
            return render_template('rentCarDelete.html', information = info)
        else:
            rentCar.query.filter_by(orderNo = orderNo).delete()
            db.session.commit()
            info = 1
            return render_template('rentCarDelete.html', information = info)

@app.route('/dealDelete', methods = ['GET', 'POST'])
def dealDelete():
    if request.method == 'GET':
        return render_template('dealDelete.html')
    else:
        dealNo = request.form['dealNo']
        try:
            deal = Deal.query.filter_by(dealNo = dealNo).first()
        except:
            return None
        if deal is None:
            info = 2
            return render_template('dealDelete.html', information = info)
        else:
            deal.query.filter_by(dealNo = dealNo).delete()
            db.session.commit()
            info = 1
            return render_template('dealDelete.html', information = info)

@app.route('/ordersUpdate', methods = ['GET', 'POST'])
def ordersUpdate():
    if request.method == 'GET':
        return render_template('ordersUpdate.html')
    else:
        orderNo = request.form['orderNo']
        roomNo = request.form['roomNo']
        customer_ssn = request.form['customer_ssn']
        checkInDate = request.form['checkInDate']
        checkOutDate = request.form['checkOutDate']
        price = request.form['price']
        pointChange = request.form['pointChange']
        cashierNo = request.form['cashierNo']
        try:
            orders = Orders.query.filter_by(orderNo = orderNo).first()
        except:
            return None
        if orders is None:
            info = 2
            return render_template('ordersUpdate.html', information = info)
        else:
            orders.orderNo = orderNo
            orders.roomNo = roomNo
            orders.customer_ssn = customer_ssn
            orders.checkInDate = checkInDate
            orders.checkOutDate = checkOutDate
            orders.price = price
            orders.pointChange = pointChange
            orders.cashierNo = cashierNo
            db.session.commit()
            info = 1
            return render_template('ordersUpdate.html', information = info)

@app.route('/roomsUpdate', methods = ['GET', 'POST'])
def roomsUpdate():
    if request.method == 'GET':
        return render_template('roomsUpdate.html')
    else:
        roomNo = request.form['roomNo']
        inRoomBill = request.form['inRoomBill']
        capacity = request.form['capacity']
        bedsNo = request.form['bedsNo']
        type = request.form['type']
        status = request.form['status']
        try:
            rooms = Rooms.query.filter_by(roomNo = roomNo).first()
        except:
            return None
        if rooms is None:
            info = 2
            return render_template('roomsUpdate.html', information = info)
        else:
            rooms.roomNo = roomNo
            rooms.inRoomBill = inRoomBill
            rooms.capacity = capacity
            rooms.bedsNo = bedsNo
            rooms.type = type
            rooms.status = status
            db.session.commit()
            info = 1
            return render_template('roomsUpdate.html', information = info)

@app.route('/maintainsUpdate', methods = ['GET', 'POST'])
def maintainsUpdate():
    if request.method == 'GET':
        return render_template('maintainsUpdate.html')
    else:
        record = request.form['record']
        staffNo = request.form['staffNo']
        roomNo = request.form['roomNo']
        linens = request.form['linens']
        lQty = request.form['lQty']
        lType = request.form['lType']
        reusable = request.form['reusable']
        cost = request.form['cost']
        date = request.form['date']
        try:
            maintains = Maintains.query.filter_by(record = record).first()
        except:
            return None
        if maintains is None:
            info = 2
            return render_template('maintainsUpdate.html', information = info)
        else:
            maintains.record = record
            maintains.staffNo = staffNo
            maintains.roomNo = roomNo
            maintains.linens = linens
            maintains.lQty = lQty
            maintains.lType = lType
            maintains.reusable = reusable
            maintains.cost = cost
            maintains.date = date
            db.session.commit()
            info = 1
            return render_template('maintainsUpdate.html', information = info)

@app.route('/equipUpdate', methods = ['GET', 'POST'])
def equipUpdate():
    if request.method == 'GET':
        return render_template('equipUpdate.html')
    else:
        record = request.form['record']
        staffNo = request.form['staffNo']
        equipName = request.form['equipName']
        equipID = request.form['equipID']
        cost = request.form['cost']
        date = request.form['date']
        try:
            equip = Public_Equipment_Repair.query.filter_by(record = record).first()
        except:
            return None
        if equip is None:
            info = 2
            return render_template('equipUpdate.html', information = info)
        else:
            equip.record = record
            equip.staffNo = staffNo
            equip.equipName = equipName
            equip.equipID = equipID
            equip.cost = cost
            equip.date = date
            db.session.commit()
            info = 1
            return render_template('equipUpdate.html', information = info)

@app.route('/membershipUpdate', methods = ['GET', 'POST'])
def membershipUpdate():
    if request.method == 'GET':
        return render_template('membershipUpdate.html')
    else:
        memberNo = request.form['memberNo']
        name = request.form['name']
        points = request.form['points']
        level = request.form['level']
        beginDate = request.form['beginDate']
        endDate = request.form['endDate']
        try:
            membership = Membership.query.filter_by(memberNo = memberNo).first()
        except:
            return None
        if membership is None:
            info = 2
            return render_template('membershipUpdate.html', information = info)
        else:
            membership.memberNo = memberNo
            membership.name = name
            membership.points = points
            membership.level = level
            membership.beginDate = beginDate
            membership.endDate = endDate
            db.session.commit()
            info = 1
            return render_template('membershipUpdate.html', information = info)

@app.route('/staffUpdate', methods = ['GET', 'POST'])
def staffUpdate():
    if request.method == 'GET':
        return render_template('staffUpdate.html')
    else:
        ssn = request.form['ssn']
        staffNo = request.form['staffNo']
        position = request.form['position']
        workYear = request.form['workYear']
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        gender = request.form['gender']
        salary = request.form['salary']
        try:
            staff = Staff.query.filter_by(staffNo = staffNo).first()
        except:
            return None
        if staff is None:
            info = 2
            return render_template('staffUpdate.html', information = info)
        else:
            staff.ssn = ssn
            staff.staffNo = staffNo
            staff.position = position
            staff.workYear = workYear
            staff.name = name
            staff.address = address
            staff.phone = phone
            staff.gender = gender
            staff.salary = salary
            db.session.commit()
            info = 1
            return render_template('staffUpdate.html', information = info)

@app.route('/busesUpdate', methods = ['GET', 'POST'])
def busesUpdate():
    if request.method == 'GET':
        return render_template('busesUpdate.html')
    else:
        VIN = request.form['VIN']
        SCHED = request.form['SCHED']
        destination = request.form['destination']
        departTime = request.form['departTime']
        carType = request.form['carType']
        capacity = request.form['capacity']
        price = request.form['price']
        takenBy = request.form['takenBy']
        try:
            buses = Buses.query.filter_by(SCHED = SCHED).first()
        except:
            return None
        if buses is None:
            info = 2
            return render_template('busesUpdate.html', information = info)
        else:
            buses.VIN = VIN
            buses.SCHED = SCHED
            buses.destination = destination
            buses.departTime = departTime
            buses.carType = carType
            buses.capacity = capacity
            buses.price = price
            buses.takenBy = takenBy
            db.session.commit()
            info = 1
            return render_template('busesUpdate.html', information = info)

@app.route('/rentCarUpdate', methods = ['GET', 'POST'])
def rentCarUpdate():
    if request.method == 'GET':
        return render_template('rentCarUpdate.html')
    else:
        orderNo = request.form['orderNo']
        VIN = request.form['VIN']
        company = request.form['company']
        carType = request.form['carType']
        capacity = request.form['capacity']
        priceTotal = request.form['priceTotal']
        rentDate = request.form['rentDate']
        returnDate = request.form['returnDate']
        rentPlace = request.form['rentPlace']
        returnPlace = request.form['returnPlace']
        rentBy = request.form['rentBy']
        try:
            rentCar = Rent_Car.query.filter_by(orderNo = orderNo).first()
        except:
            return None
        if rentCar is None:
            info = 2
            return render_template('rentCarUpdate.html', information = info)
        else:
            rentCar.orderNo = orderNo
            rentCar.VIN = VIN
            rentCar.company = company
            rentCar.carType = carType
            rentCar.capacity = capacity
            rentCar.priceTotal = priceTotal
            rentCar.rentDate = rentDate
            rentCar.returnDate = returnDate
            rentCar.rentPlace = rentPlace
            rentCar.returnPlace = returnPlace
            rentCar.rentBy = rentBy
            db.session.commit()
            info = 1
            return render_template('rentCarUpdate.html', information = info)

@app.route('/dealUpdate', methods = ['GET', 'POST'])
def dealUpdate():
    if request.method == 'GET':
        return render_template('dealUpdate.html')
    else:
        activity = request.form['activity']
        joinLevel = request.form['joinLevel']
        capacity = request.form['capacity']
        beginDate = request.form['beginDate']
        endDate = request.form['endDate']
        dealNo = request.form['dealNo']
        try:
            deal = Deal.query.filter_by(dealNo = dealNo).first()
        except:
            return None
        if deal is None:
            info = 2
            return render_template('dealUpdate.html', information = info)
        else:
            deal.activity = activity
            deal.joinLevel = joinLevel
            deal.capacity = capacity
            deal.beginDate = beginDate
            deal.endDate = endDate
            deal.dealNo = dealNo
            db.session.commit()
            info = 1
            return render_template('dealUpdate.html', information = info)

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
    app.run(host = '0.0.0.0', port = 8000, debug = True)
    manager.run()
