#Import Flask Library
import json
from re import A
from flask import Flask, render_template, request, session, url_for, redirect, jsonify
from matplotlib.style import use
from numpy import average
import pymysql.cursors
from sympy import Q, per, refine

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
def get_conn(HOST, USER, PASSWORD, DB, ROLE):
    conn = pymysql.connect(host=HOST,
                       user=USER,
                       password=PASSWORD,
                       db=None,
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    query = 'SET ROLE {}'.format(ROLE)
    print('query:', query)
    cursor.execute(query)
    cursor.close()
    conn.select_db(DB)
    return conn


#Define a route for search
@app.route('/')
def search():
    query = ''
    query = 'SELECT * FROM airline'
    print('query:', query)
    conn = get_conn('localhost', 'default_user', '', 'flight_ticket', 'default_role')
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    print(data)
    cursor.close()
    conn.close()
    return render_template('search.html', airlines=data)

#Define a route for search result
@app.route('/result', methods=['GET', 'POST'])
def result():
    departure_city = request.form.get('departure_city')
    arrival_city = request.form.get('arrival_city')
    departure_date = request.form.get('departure_date')
    arrival_date = request.form.get('arrival_date')
    query = ''
    if departure_city:
        if query == '':
            query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM (flight JOIN airport AS ad ON(flight.departure_airport=ad.airport_name)) JOIN airport AS aa ON(flight.arrival_airport=aa.airport_name) WHERE ad.airport_city=\'{}\''.format(departure_city)
        else:
            query += " AND ad.airport_city=\'{}\'".format(departure_city)
    if arrival_city:
        if query == '':
            query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM (flight JOIN airport AS ad ON(flight.departure_airport=ad.airport_name)) JOIN airport AS aa ON(flight.arrival_airport=aa.airport_name) WHERE aa.airport_city=\'{}\''.format(arrival_city)
        else:
            query += ' AND aa.airport_city=\'{}\''.format(arrival_city)
    if departure_date:
        if query == '':
            query = 'SELECT * FROM flight WHERE DATE_FORMAT(departure_time, \'%Y-%m-%e\')=DATE_FORMAT(\'{}\', \'%Y-%m-%e\')'.format(departure_date)
        else:
            query += ' AND DATE_FORMAT(departure_time, \'%Y-%m-%e\')=DATE_FORMAT(\'{}\', \'%Y-%m-%e\')'.format(departure_date)
    if arrival_date:
        if query == '':
            query = 'SELECT * FROM flight WHERE DATE_FORMAT(arrival_time, \'%Y-%m-%e\')=DATE_FORMAT(\'{}\', \'%Y-%m-%e\')'.format(arrival_date)
        else:
            query += ' AND DATE_FORMAT(arrival_time, \'%Y-%m-%e\')=DATE_FORMAT(\'{}\', \'%Y-%m-%e\')'.format(arrival_date)
    print('query:', query)
    conn = get_conn('localhost', 'default_user', '', 'flight_ticket', 'default_role')
    conn.autocommit = False
    cursor = conn.cursor()
    if query:
        query += ' AND status=\'Upcoming\''
        cursor.execute(query)
        data0 = cursor.fetchall()
    else:
        data0 = None
    print(data0)
    query = 'SELECT * FROM airline'
    print('query:', query)
    cursor.execute(query)
    data1 = cursor.fetchall()
    print(data1)
    cursor.close()
    conn.commit()
    conn.close()
    return render_template('search.html', search_result=data0, airlines=data1)

#Define a route for abstract search result
@app.route('/abstract_result', methods=['GET', 'POST'])
def abstract_result():
    searchText = request.form.get('searchText')
    query = ''
    if searchText:
        query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM (flight JOIN airport AS ad ON(flight.departure_airport=ad.airport_name)) JOIN airport AS aa ON(flight.arrival_airport=aa.airport_name) WHERE status=\'Upcoming\' AND (departure_airport LIKE \'%{}%\' OR arrival_airport LIKE \'%{}%\' OR ad.airport_city LIKE \'%{}%\' OR aa.airport_city LIKE \'%{}%\')'.format(searchText, searchText, searchText, searchText)
    print('query:', query)
    conn = get_conn('localhost', 'default_user', '', 'flight_ticket', 'default_role')
    conn.autocommit = False
    cursor = conn.cursor()
    if query:
        cursor.execute(query)
        data0 = cursor.fetchall()
    else:
        data0 = None
    print(data0)
    query = 'SELECT * FROM airline'
    print('query:', query)
    cursor.execute(query)
    data1 = cursor.fetchall()
    print(data1)
    cursor.close()
    conn.commit()
    conn.close()
    return render_template('search.html', search_result=data0, airlines=data1)

#Define a route for search result with flight number
@app.route('/number_result', methods=['GET', 'POST'])
def number_result():
    flight_number = request.form.get('flight_number')
    airline_name = request.form.get('airline_name')
    query = ''
    if flight_number:
        query = 'SELECT * FROM flight WHERE airline_name=\'{}\' AND flight_num={}'.format(airline_name,flight_number)
    print('query:', query)
    conn = get_conn('localhost', 'default_user', '', 'flight_ticket', 'default_role')
    conn.autocommit = False
    cursor = conn.cursor()
    if query:
        cursor.execute(query)
        data0 = cursor.fetchall()
    else:
        data0 = None
    print(data0)
    query = 'SELECT * FROM airline'
    print('query:', query)
    cursor.execute(query)
    data1 = cursor.fetchall()
    print(data1)
    cursor.close()
    conn.commit()
    conn.close()
    return render_template('search.html', search_result=data0, airlines=data1)

#Define a route for register
@app.route('/register')
def register():
    return render_template('register.html')

#Define a route for register branch
@app.route('/register/register_branch', methods=['GET', 'POST'])
def register_branch():
    type = request.form.get('type')
    if type == 'Customer':
        return render_template('register_customer.html')
    elif type == 'Booking Agent':
        query = ''
        query = 'SELECT * FROM airline'
        print('query:', query)
        conn = get_conn('localhost', 'default_user', '', 'flight_ticket', 'register_role')
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        cursor.close()
        conn.close()
        return render_template('register_agent.html', airlines=data)
    elif type == 'Airline Staff':
        query = ''
        query = 'SELECT * FROM airline'
        conn = get_conn('localhost', 'default_user', '', 'flight_ticket', 'register_role')
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        cursor.close()
        conn.close()
        return render_template('register_staff.html', airlines=data)
    else:
        print('Something unexpected has happened.')
        return render_template('register.html')

#Define a route for customor register
@app.route('/register/customer', methods=['GET', 'POST'])
def register_customer():
    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')
    building_number = request.form.get('building_number')
    street = request.form.get('street')
    city = request.form.get('city')
    state = request.form.get('state')
    phone_number = request.form.get('phone_number')
    passport_number = request.form.get('passport_number')
    passport_expiration = request.form.get('passport_expiration')
    passport_country = request.form.get('passport_country')
    date_of_birth = request.form.get('date_of_birth')
    conn = get_conn('localhost', 'default_user', '', 'flight_ticket', 'register_role')
    conn.autocommit = False
    query = ''
    query = 'SELECT email FROM customer WHERE email=\'{}\''.format(email)
    print('query:', query)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchone()
    print(data)
    if data:
        cursor.close()
        conn.commit()
        conn.close()
        error = 'The email is already used!'
        return render_template('register.html', error=error)
    else:
        query = 'SELECT md5(\'{}\')'.format(password)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        password = data['md5(\'{}\')'.format(password)]
        query = 'INSERT INTO customer VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', {}, \'{}\', \'{}\', \'{}\', \'{}\')'.format(email,name,password,building_number,street,city,state,phone_number,passport_number,passport_expiration,passport_country,date_of_birth)
        print('query:', query)
        cursor.execute(query)
        query = 'CREATE USER \'customer_{}\'@\'localhost\' IDENTIFIED BY \'{}\''.format(email,password)
        print('query:', query)
        cursor.execute(query)
        query = 'GRANT customer_role TO \'customer_{}\'@\'localhost\''.format(email)
        print('query:', query)
        cursor.execute(query)
        cursor.close()
        conn.commit()
        conn.close()
        session['username'] = 'customer_{}'.format(email)
        session['password'] = password
        conn = get_conn('localhost', 'customer_{}'.format(email), password, 'flight_ticket', 'customer_role')
        conn.autocommit = False
        cursor = conn.cursor()
        query = ''
        query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM ((customer JOIN purchases ON(customer.email=purchases.customer_email)) NATURAL JOIN ticket) NATURAL JOIN flight WHERE status=\'Upcoming\' AND email=\'{}\''.format(email)
        print('query:', query)
        cursor.execute(query)
        data0 = cursor.fetchall()
        print(data0)
        query = 'SELECT * FROM airline'
        print('query:', query)
        cursor.execute(query)
        data1 = cursor.fetchall()
        print(data1)
        cursor.close()
        conn.commit()
        conn.close()
        session.pop('customer_track_from', None)
        session.pop('customer_track_to', None)
        return render_template('customer_home.html', name=name, myflight=data0, airlines=data1)
    
# Define a route for spending data of customer
@app.route('/spending_data')
def spending_data():
    customer_track_from = session.get('customer_track_from')
    customer_track_to = session.get('customer_track_to')
    username = session.get('username')
    password = session.get('password')
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'customer_role')
        cursor = conn.cursor()
        query = ''
        if customer_track_from and customer_track_to:
            query = 'CALL customer_ranged_spending(\'{}\',\'{}\',\'{}\')'.format(username[9:],customer_track_from,customer_track_to)
            print('query:', query)
            cursor.execute(query)
            data = cursor.fetchall()
            for spending_per_month in data:
                spending_per_month['spending'] = float(spending_per_month['spending'])
            print(data)
        else:
            query = 'CALL customer_recent_spending(\'{}\')'.format(username[9:])
            print('query:', query)
            cursor.execute(query)
            data = cursor.fetchall()
            for spending_per_month in data:
                spending_per_month['spending'] = float(spending_per_month['spending'])
            print(data)
        cursor.close()
        conn.close()
    else:
        data = []
    return jsonify(data)

#Define a route for customer search result
@app.route('/customer/result', methods=['GET', 'POST'])
def customer_result():
    departure_city = request.form.get('departure_city')
    arrival_city = request.form.get('arrival_city')
    departure_date = request.form.get('departure_date')
    arrival_date = request.form.get('arrival_date')
    username = session.get('username')
    password = session.get('password')
    query = ''
    if departure_city:
        if query == '':
            query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM (flight JOIN airport AS ad ON(flight.departure_airport=ad.airport_name)) JOIN airport AS aa ON(flight.arrival_airport=aa.airport_name) WHERE ad.airport_city=\'{}\''.format(departure_city)
        else:
            query += " AND ad.airport_city=\'{}\'".format(departure_city)
    if arrival_city:
        if query == '':
            query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM (flight JOIN airport AS ad ON(flight.departure_airport=ad.airport_name)) JOIN airport AS aa ON(flight.arrival_airport=aa.airport_name) WHERE aa.airport_city=\'{}\''.format(arrival_city)
        else:
            query += ' AND aa.airport_city=\'{}\''.format(arrival_city)
    if departure_date:
        if query == '':
            query = 'SELECT * FROM flight WHERE DATE_FORMAT(departure_time, \'%Y-%m-%e\')=DATE_FORMAT(\'{}\', \'%Y-%m-%e\')'.format(departure_date)
        else:
            query += ' AND DATE_FORMAT(departure_time, \'%Y-%m-%e\')=DATE_FORMAT(\'{}\', \'%Y-%m-%e\')'.format(departure_date)
    if arrival_date:
        if query == '':
            query = 'SELECT * FROM flight WHERE DATE_FORMAT(arrival_time, \'%Y-%m-%e\')=DATE_FORMAT(\'{}\', \'%Y-%m-%e\')'.format(arrival_date)
        else:
            query += ' AND DATE_FORMAT(arrival_time, \'%Y-%m-%e\')=DATE_FORMAT(\'{}\', \'%Y-%m-%e\')'.format(arrival_date)
    print('query:', query)
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'customer_role')
    else:
        conn = get_conn('localhost', 'default_user', '', 'flight_ticket', 'default_role')
    conn.autocommit = False
    cursor = conn.cursor()
    if query:
        query += ' AND status=\'Upcoming\''
        cursor.execute(query)
        data0 = cursor.fetchall()
    else:
        data0 = None
    print(data0)
    query = 'SELECT * FROM airline'
    print('query:', query)
    cursor.execute(query)
    data1 = cursor.fetchall()
    print(data1)
    if username and password:
        query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM ((customer JOIN purchases ON(customer.email=purchases.customer_email)) NATURAL JOIN ticket) NATURAL JOIN flight WHERE status=\'Upcoming\' AND email=\'{}\''.format(username[9:])
        print('query:', query)
        cursor.execute(query)
        data2 = cursor.fetchall()
        print(data2)
        query = 'SELECT name FROM customer WHERE email=\'{}\''.format(username[9:])
        print('query:', query)
        cursor.execute(query)
        data3 = cursor.fetchone()['name']
        print(data3)
    cursor.close()
    conn.commit()
    conn.close()
    if username and password:
        session.pop('customer_track_from', None)
        session.pop('customer_track_to', None)
        return render_template('customer_home.html', search_result=data0, airlines=data1, myflight=data2, name=data3)
    else:
        session.clear()
        return render_template('search.html', search_result=data0, airlines=data1)

#Define a route for customer abstract search result
@app.route('/customer/abstract_result', methods=['GET', 'POST'])
def customer_abstract_result():
    searchText = request.form.get('searchText')
    username = session.get('username')
    password = session.get('password')
    query = ''
    if searchText:
        query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM (flight JOIN airport AS ad ON(flight.departure_airport=ad.airport_name)) JOIN airport AS aa ON(flight.arrival_airport=aa.airport_name) WHERE status=\'Upcoming\' AND (departure_airport LIKE \'%{}%\' OR arrival_airport LIKE \'%{}%\' OR ad.airport_city LIKE \'%{}%\' OR aa.airport_city LIKE \'%{}%\')'.format(searchText, searchText, searchText, searchText)
    print('query:', query)
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'customer_role')
    else:
        conn = get_conn('localhost', 'default_user', '', 'flight_ticket', 'default_role')
    conn.autocommit = False
    cursor = conn.cursor()
    if query:
        cursor.execute(query)
        data0 = cursor.fetchall()
    else:
        data0 = None
    print(data0)
    query = 'SELECT * FROM airline'
    print('query:', query)
    cursor.execute(query)
    data1 = cursor.fetchall()
    print(data1)
    if username and password:
        query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM ((customer JOIN purchases ON(customer.email=purchases.customer_email)) NATURAL JOIN ticket) NATURAL JOIN flight WHERE status=\'Upcoming\' AND email=\'{}\''.format(username[9:])
        print('query:', query)
        cursor.execute(query)
        data2 = cursor.fetchall()
        print(data2)
        query = 'SELECT name FROM customer WHERE email=\'{}\''.format(username[9:])
        print('query:', query)
        cursor.execute(query)
        data3 = cursor.fetchone()['name']
        print(data3)
    cursor.close()
    conn.commit()
    conn.close()
    if username and password:
        session.pop('customer_track_from', None)
        session.pop('customer_track_to', None)
        return render_template('customer_home.html', search_result=data0, airlines=data1, myflight=data2, name=data3)
    else:
        session.clear()
        return render_template('search.html', search_result=data0, airlines=data1)

#Define a route for customer search result with flight number
@app.route('/customer/number_result', methods=['GET', 'POST'])
def customer_number_result():
    flight_number = request.form.get('flight_number')
    airline_name = request.form.get('airline_name')
    username = session.get('username')
    password = session.get('password')
    query = ''
    if flight_number:
        query = 'SELECT * FROM flight WHERE airline_name=\'{}\' AND flight_num={}'.format(airline_name,flight_number)
    print('query:', query)
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'customer_role')
    else:
        conn = get_conn('localhost', 'default_user', '', 'flight_ticket', 'default_role')
    conn.autocommit = False
    cursor = conn.cursor()
    if query:
        cursor.execute(query)
        data0 = cursor.fetchall()
    else:
        data0 = None
    print(data0)
    query = 'SELECT * FROM airline'
    print('query:', query)
    cursor.execute(query)
    data1 = cursor.fetchall()
    print(data1)
    if username and password:
        query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM ((customer JOIN purchases ON(customer.email=purchases.customer_email)) NATURAL JOIN ticket) NATURAL JOIN flight WHERE status=\'Upcoming\' AND email=\'{}\''.format(username[9:])
        print('query:', query)
        cursor.execute(query)
        data2 = cursor.fetchall()
        print(data2)
        query = 'SELECT name FROM customer WHERE email=\'{}\''.format(username[9:])
        print('query:', query)
        cursor.execute(query)
        data3 = cursor.fetchone()['name']
        print(data3)
    cursor.close()
    conn.commit()
    conn.close()
    if username and password:
        session.pop('customer_track_from', None)
        session.pop('customer_track_to', None)
        return render_template('customer_home.html', search_result=data0, airlines=data1, myflight=data2, name=data3)
    else:
        session.clear()
        return render_template('search.html', search_result=data0, airlines=data1)

#Define a route for customer spending track
@app.route('/customer/track', methods=['GET', 'POST'])
def customer_track():
    customer_track_from = request.form.get('from')
    customer_track_to = request.form.get('to')
    username = session.get('username')
    password = session.get('password')
    if username and password:
        session['customer_track_from'] = customer_track_from
        session['customer_track_to'] = customer_track_to
        conn = get_conn('localhost', username, password, 'flight_ticket', 'customer_role')
        conn.autocommit = False
        cursor = conn.cursor()
        query = ''
        query = 'SELECT * FROM airline'
        print('query:', query)
        cursor.execute(query)
        data0 = cursor.fetchall()
        print(data0)
        query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM ((customer JOIN purchases ON(customer.email=purchases.customer_email)) NATURAL JOIN ticket) NATURAL JOIN flight WHERE status=\'Upcoming\' AND email=\'{}\''.format(username[9:])
        print('query:', query)
        cursor.execute(query)
        data1 = cursor.fetchall()
        print(data1)
        query = 'SELECT name FROM customer WHERE email=\'{}\''.format(username[9:])
        print('query:', query)
        cursor.execute(query)
        data2 = cursor.fetchone()['name']
        print(data2)
        cursor.close()
        conn.commit()
        conn.close()
        return render_template('customer_home.html', airlines=data0, myflight=data1, name=data2)
    else:
        session.clear()
        return redirect(url_for('search'))

#Define a route for customer purchase
@app.route('/customer/purchase', methods=['GET', 'POST'])
def customer_purchase():
    ticket_info = list(request.form.keys())[0].split(',')
    airline_name = ticket_info[0]
    flight_num = ticket_info[1]
    username = session.get('username')
    password = session.get('password')
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'customer_role')
        cursor = conn.cursor()
        query = ''
        query = 'CALL customer_purchase(\'{}\', \'{}\')'.format(airline_name,flight_num)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        cursor.close()
        conn.close()
        return render_template('choose_ticket.html', airline_name=airline_name, flight_num=flight_num, tickets=data)
    else:
        return redirect(url_for('search'))

#Define a route for customer purchase result
@app.route('/customer/purchase_result', methods=['GET', 'POST'])
def customer_purchase_result():
    ticket_id = list(request.form.keys())[0]
    username = session.get('username')
    password = session.get('password')
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'customer_role')
        conn.autocommit = False
        cursor = conn.cursor()
        query = ''
        query = 'SELECT date_format(now(), \'%Y-%m-%d\') AS today'
        print('query:', query)
        cursor.execute(query)
        today = cursor.fetchone().get('today')
        print(today)
        query = 'INSERT INTO purchases VALUES({}, \'{}\', NULL, \'{}\')'.format(ticket_id,username[9:],today)
        print('query:', query)
        cursor.execute(query)
        query = 'SELECT email, name FROM customer WHERE email=\'{}\''.format(username[9:])
        print('query:', query)
        cursor.execute(query)
        data0 = cursor.fetchone()
        print(data0)
        query = 'SELECT ticket_id, airline_name, flight_num FROM ticket WHERE ticket_id=\'{}\''.format(ticket_id)
        print('query:', query)
        cursor.execute(query)
        data1 = cursor.fetchone()
        print(data1)
        cursor.close()
        conn.commit()
        conn.close()
        return render_template('purchase_result.html', customer_info=data0, ticket_info=data1)
    else:
        return redirect(url_for('search'))

#Define a route for customer back to home
@app.route('/customer/back', methods=['GET', 'POST'])
def customer_back():
    username = session.get('username')
    password = session.get('password')
    conn = get_conn('localhost', username, password, 'flight_ticket', 'customer_role')
    conn.autocommit = False
    cursor = conn.cursor()
    query = ''
    query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM ((customer JOIN purchases ON(customer.email=purchases.customer_email)) NATURAL JOIN ticket) NATURAL JOIN flight WHERE status=\'Upcoming\' AND email=\'{}\''.format(username[9:])
    print('query:', query)
    cursor.execute(query)
    data0 = cursor.fetchall()
    print(data0)
    query = 'SELECT * FROM airline'
    print('query:', query)
    cursor.execute(query)
    data1 = cursor.fetchall()
    print(data1)
    query = 'SELECT name FROM customer WHERE email=\'{}\''.format(username[9:])
    print('query:', query)
    cursor.execute(query)
    name = cursor.fetchone().get('name')
    print(name)
    session.pop('customer_track_from', None)
    session.pop('customer_track_to', None)
    cursor.close()
    conn.commit()
    conn.close()
    return render_template('customer_home.html', name=name, myflight=data0, airlines=data1)

#Define a route for agent register
@app.route('/register/agent', methods=['GET', 'POST'])
def register_agent():
    email = request.form.get('email')
    password = request.form.get('password')
    booking_agent_id = request.form.get('booking_agent_id')
    conn = get_conn('localhost', 'default_user', '', 'flight_ticket', 'register_role')
    conn.autocommit = False
    query = ''
    query = 'SELECT email FROM booking_agent WHERE email=\'{}\''.format(email)
    print('query:', query)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchone()
    print(data)
    if data:
        cursor.close()
        conn.commit()
        conn.close()
        error = 'The email is already used!'
        return render_template('register.html', error=error)
    else:
        query = 'SELECT email FROM booking_agent WHERE booking_agent_id=\'{}\''.format(booking_agent_id)
        print('query:', query)
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        if data:
            cursor.close()
            conn.commit()
            conn.close()
            error = 'The id number is already used!'
            return render_template('register.html', error=error)
        query = 'SELECT md5(\'{}\')'.format(password)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        password = data['md5(\'{}\')'.format(password)]
        query = 'INSERT INTO booking_agent VALUES(\'{}\', \'{}\', {})'.format(email,password,booking_agent_id)
        print('query:', query)
        cursor.execute(query)
        query = 'CREATE USER \'agent_{}\'@\'localhost\' IDENTIFIED BY \'{}\''.format(email,password)
        print('query:', query)
        cursor.execute(query)
        query = 'GRANT agent_role TO \'agent_{}\'@\'localhost\''.format(email)
        print('query:', query)
        cursor.execute(query)
        cursor.close()
        conn.commit()
        conn.close()
        session['username'] = 'agent_{}'.format(email)
        session['password'] = password
        conn = get_conn('localhost', 'agent_{}'.format(email), password, 'flight_ticket', 'agent_role')
        conn.autocommit = False
        cursor = conn.cursor()
        query = ''
        query = 'SELECT * FROM airline'
        print('query:', query)
        cursor.execute(query)
        data0 = cursor.fetchall()
        print(data0)
        query = 'SELECT customer_email, airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM ((purchases NATURAL JOIN booking_agent) NATURAL JOIN ticket) NATURAL JOIN flight WHERE status=\'Upcoming\' AND email=\'{}\''.format(email)
        print('query:', query)
        cursor.execute(query)
        data1 = cursor.fetchall()
        print(data1)
        query = 'SELECT sum(price)*0.1 AS total_commission, avg(price)*0.1 AS avg_commission, COUNT(ticket_id) AS total_tickets FROM ((booking_agent NATURAL JOIN purchases) NATURAL JOIN ticket) NATURAL JOIN flight WHERE datediff(now(), purchase_date)<=30 AND email=\'{}\''.format(email)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        total_commission = float(data.get('total_commission')) if data.get('total_commission') else None
        average_commission = float(data.get('avg_commission')) if data.get('avg_commission') else None
        total_tickets = data.get('total_tickets')
        cursor.close()
        conn.commit()
        conn.close()
        return render_template('agent_home.html', airlines=data0, myflight=data1, total_commission=total_commission, average_commission=average_commission, total_tickets=total_tickets, name=email)

#Define a route for ranking ticket data of customer
@app.route('/customer_data_ticket')
def customer_data_ticket():
    username = session.get('username')
    password = session.get('password')
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'agent_role')
        cursor = conn.cursor()
        query = ''
        agent_commission_from = session.get('agent_commission_from')
        agent_commission_to = session.get('agent_commission_to')
        if agent_commission_from and agent_commission_to:
            query = 'CALL agent_customer_ticket_ranged(\'{}\', \'{}\', \'{}\')'.format(username[6:],agent_commission_from,agent_commission_to)
        else:
            query = 'CALL agent_customer_ticket(\'{}\')'.format(username[6:])
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchall()
        for tickets_per_person in data:
            tickets_per_person['number_of_tickets'] = float(tickets_per_person['number_of_tickets'])
        print(data)
        cursor.close()
        conn.close()
    else:
        data = []
    return jsonify(data)

#Define a route for ranking commission data of customer
@app.route('/customer_data_commission')
def customer_data_commission():
    username = session.get('username')
    password = session.get('password')
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'agent_role')
        cursor = conn.cursor()
        query = ''
        agent_commission_from = session.get('agent_commission_from')
        agent_commission_to = session.get('agent_commission_to')
        if agent_commission_from and agent_commission_to:
            query = 'CALL agent_customer_commission_ranged(\'{}\', \'{}\', \'{}\')'.format(username[6:],agent_commission_from,agent_commission_to)
        else:
            query = 'CALL agent_customer_commission(\'{}\')'.format(username[6:])
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchall()
        for tickets_per_person in data:
            tickets_per_person['spending'] = float(tickets_per_person['spending'])
        print(data)
        cursor.close()
        conn.close()
    else:
        data = []
    return jsonify(data)

#Define a route for agent search result
@app.route('/agent/result', methods=['GET', 'POST'])
def agent_result():
    departure_city = request.form.get('departure_city')
    arrival_city = request.form.get('arrival_city')
    departure_date = request.form.get('departure_date')
    arrival_date = request.form.get('arrival_date')
    username = session.get('username')
    password = session.get('password')
    query = ''
    if departure_city:
        if query == '':
            query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM (flight JOIN airport AS ad ON(flight.departure_airport=ad.airport_name)) JOIN airport AS aa ON(flight.arrival_airport=aa.airport_name) WHERE ad.airport_city=\'{}\''.format(departure_city)
        else:
            query += " AND ad.airport_city=\'{}\'".format(departure_city)
    if arrival_city:
        if query == '':
            query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM (flight JOIN airport AS ad ON(flight.departure_airport=ad.airport_name)) JOIN airport AS aa ON(flight.arrival_airport=aa.airport_name) WHERE aa.airport_city=\'{}\''.format(arrival_city)
        else:
            query += ' AND aa.airport_city=\'{}\''.format(arrival_city)
    if departure_date:
        if query == '':
            query = 'SELECT * FROM flight WHERE DATE_FORMAT(departure_time, \'%Y-%m-%e\')=DATE_FORMAT(\'{}\', \'%Y-%m-%e\')'.format(departure_date)
        else:
            query += ' AND DATE_FORMAT(departure_time, \'%Y-%m-%e\')=DATE_FORMAT(\'{}\', \'%Y-%m-%e\')'.format(departure_date)
    if arrival_date:
        if query == '':
            query = 'SELECT * FROM flight WHERE DATE_FORMAT(arrival_time, \'%Y-%m-%e\')=DATE_FORMAT(\'{}\', \'%Y-%m-%e\')'.format(arrival_date)
        else:
            query += ' AND DATE_FORMAT(arrival_time, \'%Y-%m-%e\')=DATE_FORMAT(\'{}\', \'%Y-%m-%e\')'.format(arrival_date)
    print('query:', query)
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'agent_role')
    else:
        conn = get_conn('localhost', 'default_user', '', 'flight_ticket', 'default_role')
    conn.autocommit = False
    cursor = conn.cursor()
    if query:
        query += ' AND status=\'Upcoming\''
        cursor.execute(query)
        data0 = cursor.fetchall()
    else:
        data0 = None
    print(data0)
    query = 'SELECT * FROM airline'
    print('query:', query)
    cursor.execute(query)
    data1 = cursor.fetchall()
    print(data1)
    if username and password:
        query = 'SELECT airline_name FROM booking_agent_work_for WHERE email=\'{}\''.format(username[6:])
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        data = [line['airline_name'] for line in data]
        for line in data0:
            if line['airline_name'] in data:
                line['purchase'] = 1
            else:
                line['purchase'] = 0
        email = username[6:]
        query = 'SELECT customer_email, airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM ((purchases NATURAL JOIN booking_agent) NATURAL JOIN ticket) NATURAL JOIN flight WHERE status=\'Upcoming\' AND email=\'{}\''.format(email)
        print('query:', query)
        cursor.execute(query)
        data2 = cursor.fetchall()
        print(data2)
        query = 'SELECT sum(price)*0.1 AS total_commission, avg(price)*0.1 AS avg_commission, COUNT(ticket_id) AS total_tickets FROM ((booking_agent NATURAL JOIN purchases) NATURAL JOIN ticket) NATURAL JOIN flight WHERE datediff(now(), purchase_date)<=30 AND email=\'{}\''.format(email)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        total_commission = float(data.get('total_commission')) if data.get('total_commission') else None
        average_commission = float(data.get('avg_commission')) if data.get('avg_commission') else None
        total_tickets = data.get('total_tickets')
    cursor.close()
    conn.commit()
    conn.close()
    if username and password:
        return render_template('agent_home.html', search_result=data0, airlines=data1, myflight=data2, total_commission=total_commission, average_commission=average_commission, total_tickets=total_tickets, name=email)
    else:
        session.clear()
        return render_template('search.html', search_result=data0, airlines=data1)

#Define a route for agent abstract search result
@app.route('/agent/abstract_result', methods=['GET', 'POST'])
def agent_abstract_result():
    searchText = request.form.get('searchText')
    username = session.get('username')
    password = session.get('password')
    query = ''
    if searchText:
        query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM (flight JOIN airport AS ad ON(flight.departure_airport=ad.airport_name)) JOIN airport AS aa ON(flight.arrival_airport=aa.airport_name) WHERE status=\'Upcoming\' AND (departure_airport LIKE \'%{}%\' OR arrival_airport LIKE \'%{}%\' OR ad.airport_city LIKE \'%{}%\' OR aa.airport_city LIKE \'%{}%\')'.format(searchText, searchText, searchText, searchText)
    print('query:', query)
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'agent_role')
    else:
        conn = get_conn('localhost', 'default_user', '', 'flight_ticket', 'default_role')
    conn.autocommit = False
    cursor = conn.cursor()
    if query:
        cursor.execute(query)
        data0 = cursor.fetchall()
    else:
        data0 = None
    print(data0)
    query = 'SELECT * FROM airline'
    print('query:', query)
    cursor.execute(query)
    data1 = cursor.fetchall()
    print(data1)
    if username and password:
        query = 'SELECT airline_name FROM booking_agent_work_for WHERE email=\'{}\''.format(username[6:])
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        data = [line['airline_name'] for line in data]
        for line in data0:
            if line['airline_name'] in data:
                line['purchase'] = 1
            else:
                line['purchase'] = 0
        email = username[6:]
        query = 'SELECT customer_email, airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM ((purchases NATURAL JOIN booking_agent) NATURAL JOIN ticket) NATURAL JOIN flight WHERE status=\'Upcoming\' AND email=\'{}\''.format(email)
        print('query:', query)
        cursor.execute(query)
        data2 = cursor.fetchall()
        print(data2)
        query = 'SELECT sum(price)*0.1 AS total_commission, avg(price)*0.1 AS avg_commission, COUNT(ticket_id) AS total_tickets FROM ((booking_agent NATURAL JOIN purchases) NATURAL JOIN ticket) NATURAL JOIN flight WHERE datediff(now(), purchase_date)<=30 AND email=\'{}\''.format(email)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        total_commission = float(data.get('total_commission')) if data.get('total_commission') else None
        average_commission = float(data.get('avg_commission')) if data.get('avg_commission') else None
        total_tickets = data.get('total_tickets')
    cursor.close()
    conn.commit()
    conn.close()
    if username and password:
        return render_template('agent_home.html', search_result=data0, airlines=data1, myflight=data2, total_commission=total_commission, average_commission=average_commission, total_tickets=total_tickets, name=email)
    else:
        session.clear()
        return render_template('search.html', search_result=data0, airlines=data1)

#Define a route for agent search result with flight number
@app.route('/agent/number_result', methods=['GET', 'POST'])
def agent_number_result():
    flight_number = request.form.get('flight_number')
    airline_name = request.form.get('airline_name')
    username = session.get('username')
    password = session.get('password')
    query = ''
    if flight_number:
        query = 'SELECT * FROM flight WHERE airline_name=\'{}\' AND flight_num={}'.format(airline_name,flight_number)
    print('query:', query)
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'agent_role')
    else:
        conn = get_conn('localhost', 'default_user', '', 'flight_ticket', 'default_role')
    conn.autocommit = False
    cursor = conn.cursor()
    if query:
        cursor.execute(query)
        data0 = cursor.fetchall()
    else:
        data0 = None
    print(data0)
    query = 'SELECT * FROM airline'
    print('query:', query)
    cursor.execute(query)
    data1 = cursor.fetchall()
    print(data1)
    if username and password:
        query = 'SELECT airline_name FROM booking_agent_work_for WHERE email=\'{}\''.format(username[6:])
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        data = [line['airline_name'] for line in data]
        for line in data0:
            if line['airline_name'] in data:
                line['purchase'] = 1
            else:
                line['purchase'] = 0
        email = username[6:]
        query = 'SELECT customer_email, airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM ((purchases NATURAL JOIN booking_agent) NATURAL JOIN ticket) NATURAL JOIN flight WHERE status=\'Upcoming\' AND email=\'{}\''.format(email)
        print('query:', query)
        cursor.execute(query)
        data2 = cursor.fetchall()
        print(data2)
        query = 'SELECT sum(price)*0.1 AS total_commission, avg(price)*0.1 AS avg_commission, COUNT(ticket_id) AS total_tickets FROM ((booking_agent NATURAL JOIN purchases) NATURAL JOIN ticket) NATURAL JOIN flight WHERE datediff(now(), purchase_date)<=30 AND email=\'{}\''.format(email)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        total_commission = float(data.get('total_commission')) if data.get('total_commission') else None
        average_commission = float(data.get('avg_commission')) if data.get('avg_commission') else None
        total_tickets = data.get('total_tickets')
    cursor.close()
    conn.commit()
    conn.close()
    if username and password:
        return render_template('agent_home.html', search_result=data0, airlines=data1, myflight=data2, total_commission=total_commission, average_commission=average_commission, total_tickets=total_tickets, name=email)
    else:
        session.clear()
        return render_template('search.html', search_result=data0, airlines=data1)

#Define a route for agent search result about commission
@app.route('/agent/commission_result', methods=['GET', 'POST'])
def agent_commission_result():
    commission_from = request.form.get('from')
    commission_to = request.form.get('to')
    username = session.get('username')
    password = session.get('password')
    query = ''
    if username and password:
        print('commission_result')
        conn = get_conn('localhost', username, password, 'flight_ticket', 'agent_role')
        conn.autocommit = False
        cursor = conn.cursor()
        query = 'SELECT * FROM airline'
        print('query:', query)
        cursor.execute(query)
        data0 = cursor.fetchall()
        print(data0)
        email = username[6:]
        query = 'SELECT customer_email, airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM ((purchases NATURAL JOIN booking_agent) NATURAL JOIN ticket) NATURAL JOIN flight WHERE status=\'Upcoming\' AND email=\'{}\''.format(email)
        print('query:', query)
        cursor.execute(query)
        data1 = cursor.fetchall()
        print(data1)
        if commission_from and commission_to:
            query = 'CALL agent_ranged_commission(\'{}\', \'{}\', \'{}\')'.format(email,commission_from, commission_to)
            print('query:', query)
            cursor.execute(query)
            data = cursor.fetchone()
            print(data)
            total_commission = float(data.get('total_commission')) if data.get('total_commission') else None
            average_commission = float(data.get('avg_commission')) if data.get('avg_commission') else None
            total_tickets = data.get('total_tickets')
            session['agent_commission_from'] = commission_from
            session['agent_commission_to'] = commission_to
            print('agent_commission_from', session.get('agent_commission_from'))
            print('agent_commission_to', session.get('agent_commission_to'))
        else:
            query = 'SELECT sum(price)*0.1 AS total_commission, avg(price)*0.1 AS avg_commission, COUNT(ticket_id) AS total_tickets FROM ((booking_agent NATURAL JOIN purchases) NATURAL JOIN ticket) NATURAL JOIN flight WHERE datediff(now(), purchase_date)<=30 AND email=\'{}\''.format(email)
            print('query:', query)
            cursor.execute(query)
            data = cursor.fetchone()
            print(data)
            total_commission = float(data.get('total_commission')) if data.get('total_commission') else None
            average_commission = float(data.get('avg_commission')) if data.get('avg_commission') else None
            total_tickets = data.get('total_tickets')
            session.pop('agent_commission_from', None)
            session.pop('agent_commission_to', None)
        cursor.close()
        conn.commit()
        conn.close()
        return render_template('agent_home.html', airlines=data0, myflight=data1, total_commission=total_commission, average_commission=average_commission, total_tickets=total_tickets, name=email)
    else:
        session.clear()
        return redirect(url_for('search'))

#Define a route for agent purchase
@app.route('/agent/purchase', methods=['GET', 'POST'])
def agent_purchase():
    ticket_info = list(request.form.keys())[0].split(',')
    airline_name = ticket_info[0]
    flight_num = ticket_info[1]
    session['agent_airline_name'] = airline_name
    session['agent_flight_num'] = flight_num
    username = session.get('username')
    password = session.get('password')
    if username and password:
        return render_template('agent_purchase.html')
    else:
        session.clear()
        return redirect(url_for('search'))

#Define a route for agent purchase ticket
@app.route('/agent/purchase_ticket', methods=['GET', 'POST'])
def agent_purchase_ticket():
    agent_customer_email = request.form.get('email')
    airline_name = session.get('agent_airline_name')
    flight_num = session.get('agent_flight_num')
    username = session.get('username')
    password = session.get('password')
    if username and password and airline_name and flight_num:
        session['agent_customer_email'] = agent_customer_email
        conn = get_conn('localhost', username, password, 'flight_ticket', 'agent_role')
        conn.autocommit = False
        cursor = conn.cursor()
        query = ''
        query = 'SELECT airline_name FROM booking_agent_work_for WHERE email=\'{}\' AND airline_name=\'{}\''.format(username[6:],airline_name)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        if data:
            query = 'SELECT email FROM customer WHERE email=\'{}\''.format(agent_customer_email)
            print('query:', query)
            cursor.execute(query)
            data = cursor.fetchone()
            print(data)
            if data:
                query = 'CALL customer_purchase(\'{}\', \'{}\')'.format(airline_name,flight_num)
                print('query:', query)
                cursor.execute(query)
                data = cursor.fetchall()
                print(data)
                cursor.close()
                conn.commit()
                conn.close()
                session.pop('airline_name', None)
                session.pop('flight_num', None)
                return render_template('choose_ticket(for_agent).html', airline_name=airline_name, flight_num=flight_num, tickets=data)
            else:
                cursor.close()
                conn.commit()
                conn.close()
                error = 'The email {} does not exist!'.format(agent_customer_email)
                return render_template('agent_purchase.html', error=error)
        else:
            return redirect(url_for(agent_back))
    else:
        session.clear()
        return redirect(url_for('search'))

#Define a route for agent purchase register
@app.route('/agent/purchase_register')
def agent_purchase_register():
    return render_template('agent_purchase_info.html')

#Define a route for agent purchase register cont.
@app.route('/agent/purchase_register_cont', methods=['GET', 'POST'])
def agent_purchase_register_cont():
    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')
    building_number = request.form.get('building_number')
    street = request.form.get('street')
    city = request.form.get('city')
    state = request.form.get('state')
    phone_number = request.form.get('phone_number')
    passport_number = request.form.get('passport_number')
    passport_expiration = request.form.get('passport_expiration')
    passport_country = request.form.get('passport_country')
    date_of_birth = request.form.get('date_of_birth')
    conn = get_conn('localhost', 'default_user', '', 'flight_ticket', 'register_role')
    conn.autocommit = False
    query = ''
    query = 'SELECT email FROM customer WHERE email=\'{}\''.format(email)
    print('query:', query)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchone()
    print(data)
    if data:
        cursor.close()
        conn.commit()
        conn.close()
        error = 'The email {} already exists!'.format(email)
        return render_template('agent_purchase_info.html', error=error)
    else:
        query = 'SELECT md5(\'{}\')'.format(password)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        password = data['md5(\'{}\')'.format(password)]
        query = 'INSERT INTO customer VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', {}, \'{}\', \'{}\', \'{}\', \'{}\')'.format(email,name,password,building_number,street,city,state,phone_number,passport_number,passport_expiration,passport_country,date_of_birth)
        print('query:', query)
        cursor.execute(query)
        query = 'CREATE USER \'customer_{}\'@\'localhost\' IDENTIFIED BY \'{}\''.format(email,password)
        print('query:', query)
        cursor.execute(query)
        query = 'GRANT customer_role TO \'customer_{}\'@\'localhost\''.format(email)
        print('query:', query)
        cursor.execute(query)
        cursor.close()
        conn.commit()
        conn.close()
        agent_customer_email = email
        airline_name = session.get('agent_airline_name')
        flight_num = session.get('agent_flight_num')
        username = session.get('username')
        password = session.get('password')
        if username and password and airline_name and flight_num:
            session['agent_customer_email'] = agent_customer_email
            conn = get_conn('localhost', username, password, 'flight_ticket', 'agent_role')
            cursor = conn.cursor()
            query = ''
            query = 'CALL customer_purchase(\'{}\', \'{}\')'.format(airline_name,flight_num)
            print('query:', query)
            cursor.execute(query)
            data = cursor.fetchall()
            print(data)
            cursor.close()
            conn.close()
            session.pop('airline_name', None)
            session.pop('flight_num', None)
            return render_template('choose_ticket(for_agent).html', airline_name=airline_name, flight_num=flight_num, tickets=data)
        else:
            session.clear()
            return redirect(url_for('search'))

#Define a route for agent purchase result
@app.route('/agent/purchase_result', methods=['GET', 'POST'])
def agent_purchase_result():
    ticket_id = list(request.form.keys())[0]
    username = session.get('username')
    password = session.get('password')
    customer_email = session.get('agent_customer_email')
    if username and password and customer_email:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'agent_role')
        conn.autocommit = False
        cursor = conn.cursor()
        query = ''
        query = 'SELECT date_format(now(), \'%Y-%m-%d\') AS today'
        print('query:', query)
        cursor.execute(query)
        today = cursor.fetchone().get('today')
        print(today)
        query = 'SELECT booking_agent_id FROM booking_agent WHERE email=\'{}\''.format(username[6:])
        print('query:', query)
        cursor.execute(query)
        booking_agent_id = cursor.fetchone().get('booking_agent_id')
        print(booking_agent_id)
        query = 'INSERT INTO purchases VALUES({}, \'{}\', \'{}\', \'{}\')'.format(ticket_id,customer_email,booking_agent_id,today)
        print('query:', query)
        cursor.execute(query)
        query = 'SELECT email, name FROM customer WHERE email=\'{}\''.format(customer_email)
        print('query:', query)
        cursor.execute(query)
        data0 = cursor.fetchone()
        print(data0)
        query = 'SELECT ticket_id, airline_name, flight_num FROM ticket WHERE ticket_id=\'{}\''.format(ticket_id)
        print('query:', query)
        cursor.execute(query)
        data1 = cursor.fetchone()
        print(data1)
        cursor.close()
        conn.commit()
        conn.close()
        session.pop('agent_customer_email', None)
        return render_template('purchase_result(for_agent).html', customer_info=data0, ticket_info=data1, booking_agent_id=booking_agent_id)
    else:
        session.clear()
        return redirect(url_for('search'))

#Define a route for agent back to home
@app.route('/agent/back', methods=['GET', 'POST'])
def agent_back():
    username = session.get('username')
    password = session.get('password')
    email = username[6:]
    conn = get_conn('localhost', username, password, 'flight_ticket', 'agent_role')
    conn.autocommit = False
    cursor = conn.cursor()
    query = ''
    query = 'SELECT * FROM airline'
    print('query:', query)
    cursor.execute(query)
    data0 = cursor.fetchall()
    print(data0)
    query = 'SELECT customer_email, airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM ((purchases NATURAL JOIN booking_agent) NATURAL JOIN ticket) NATURAL JOIN flight WHERE status=\'Upcoming\' AND email=\'{}\''.format(email)
    print('query:', query)
    cursor.execute(query)
    data1 = cursor.fetchall()
    print(data1)
    query = 'SELECT sum(price)*0.1 AS total_commission, avg(price)*0.1 AS avg_commission, COUNT(ticket_id) AS total_tickets FROM ((booking_agent NATURAL JOIN purchases) NATURAL JOIN ticket) NATURAL JOIN flight WHERE datediff(now(), purchase_date)<=30 AND email=\'{}\''.format(email)
    print('query:', query)
    cursor.execute(query)
    data = cursor.fetchone()
    print(data)
    total_commission = float(data.get('total_commission')) if data.get('total_commission') else None
    average_commission = float(data.get('avg_commission')) if data.get('avg_commission') else None
    total_tickets = data.get('total_tickets')
    cursor.close()
    conn.commit()
    conn.close()
    return render_template('agent_home.html', airlines=data0, myflight=data1, total_commission=total_commission, average_commission=average_commission, total_tickets=total_tickets, name=email)

#Define a route for staff register
@app.route('/register/staff', methods=['GET', 'POST'])
def register_staff():
    username = request.form.get('username')
    password = request.form.get('password')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    date_of_birth = request.form.get('date_of_birth')
    airline_name = request.form.get('airline_name')
    conn = get_conn('localhost', 'default_user', '', 'flight_ticket', 'register_role')
    conn.autocommit = False
    query = ''
    query = 'SELECT username FROM airline_staff WHERE username=\'{}\''.format(username)
    print('query:', query)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchone()
    print(data)
    if data:
        cursor.close()
        conn.commit()
        conn.close()
        error = 'The username is already used!'
        return render_template('register.html', error=error)
    else:
        query = 'SELECT md5(\'{}\')'.format(password)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        password = data['md5(\'{}\')'.format(password)]
        query = 'INSERT INTO airline_staff VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')'.format(username,password,first_name,last_name,date_of_birth,airline_name)
        print('query:', query)
        cursor.execute(query)
        query = 'CREATE USER \'staff_{}\'@\'localhost\' IDENTIFIED BY \'{}\''.format(username,password)
        print('query:', query)
        cursor.execute(query)
        query = 'GRANT staff_role TO \'staff_{}\'@\'localhost\''.format(username)
        print('query:', query)
        cursor.execute(query)
        cursor.close()
        conn.commit()
        conn.close()
        session['username'] = 'staff_{}'.format(username)
        session['password'] = password
        conn = get_conn('localhost', 'staff_{}'.format(username), password, 'flight_ticket', 'staff_role')
        conn.autocommit = False
        cursor = conn.cursor()
        query = ''
        query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM flight NATURAL JOIN airline_staff WHERE status=\'Upcoming\' AND username=\'{}\' AND datediff(departure_time, now())<=30'.format(username)
        print('query:', query)
        cursor.execute(query)
        data0 = cursor.fetchall()
        print(data0)
        query = 'SELECT booking_agent_id AS id FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN flight) NATURAL JOIN airline_staff WHERE username=\'{}\' AND booking_agent_id IS NOT NULL AND date_format((now()-INTERVAL 1 month), \'%m\')=date_format(purchase_date, \'%m\') GROUP BY booking_agent_id ORDER BY COUNT(ticket_id) DESC LIMIT 5'.format(username)
        print('query:', query)
        cursor.execute(query)
        data1 = cursor.fetchall()
        print(data1)
        data1 = [id['id'] for id in data1]
        query = 'SELECT booking_agent_id AS id FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN flight) NATURAL JOIN airline_staff WHERE username=\'{}\' AND booking_agent_id IS NOT NULL AND date_format((now()-INTERVAL 1 year), \'%Y\')=date_format(purchase_date, \'%Y\') GROUP BY booking_agent_id ORDER BY COUNT(ticket_id) DESC LIMIT 5'.format(username)
        print('query:', query)
        cursor.execute(query)
        data2 = cursor.fetchall()
        print(data2)
        data2 = [id['id'] for id in data2]
        query = 'SELECT booking_agent_id AS id FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN flight) NATURAL JOIN airline_staff WHERE username=\'{}\' AND booking_agent_id IS NOT NULL AND date_format((now()-INTERVAL 1 year), \'%Y\')=date_format(purchase_date, \'%Y\') GROUP BY booking_agent_id ORDER BY SUM(price) DESC LIMIT 5'.format(username)
        print('query:', query)
        cursor.execute(query)
        data3 = cursor.fetchall()
        print(data3)
        data3 = [id['id'] for id in data3]
        query = 'CALL staff_customer_ticket(\'{}\')'.format(username)
        print('query:', query)
        cursor.execute(query)
        data4 = cursor.fetchall()
        print(data4)
        query = 'SELECT airport_city FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN (flight JOIN airport ON(flight.arrival_airport=airport.airport_name))) NATURAL JOIN airline_staff WHERE username=\'{}\' AND period_diff(date_format(now(), \'%Y%m\'), date_format(purchase_date, \'%Y%m\'))<=3 GROUP BY airport_city ORDER BY COUNT(ticket_id) DESC LIMIT 3'.format(username)
        print('query:', query)
        cursor.execute(query)
        data5 = cursor.fetchall()
        print(data5)
        data5 = [city['airport_city'] for city in data5]
        query = 'SELECT airport_city FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN (flight JOIN airport ON(flight.arrival_airport=airport.airport_name))) NATURAL JOIN airline_staff WHERE username=\'{}\' AND date_format((now()-INTERVAL 1 year), \'%Y\')=date_format(purchase_date, \'%Y\') GROUP BY airport_city ORDER BY COUNT(ticket_id) DESC LIMIT 3'.format(username)
        print('query:', query)
        cursor.execute(query)
        data6 = cursor.fetchall()
        print(data6)
        data6 = [city['airport_city'] for city in data6]
        query = 'SELECT airline_name FROM airline_staff WHERE username=\'{}\''.format(username)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        airline_name = data.get('airline_name')
        query = 'SELECT COUNT(ticket_id) AS amount FROM (purchases NATURAL JOIN ticket) NATURAL JOIN flight WHERE date_format(purchase_date, \'%Y\')=date_format((now() - INTERVAL (1) year), \'%Y\') AND airline_name=\'{}\''.format(airline_name)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        ticketsold_year = data['amount']
        query = 'SELECT COUNT(ticket_id) AS amount FROM (purchases NATURAL JOIN ticket) NATURAL JOIN flight WHERE date_format(purchase_date, \'%Y-%m\')=date_format((now() - INTERVAL (1) month), \'%Y-%m\') AND airline_name=\'{}\''.format(airline_name)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        ticketsold_month = data['amount']
        cursor.close()
        conn.commit()
        conn.close()
        return render_template('staff_home.html', username=username, operator=0, admin=0, myflight=data0, agent_bynum_month=data1, agent_bynum_year=data2, agent_bycom_year=data3, customers=data4, destination_month=data5, destination_year=data6, ticketsold_year=ticketsold_year, ticketsold_month=ticketsold_month, airline=airline_name)

#Define a route for passing revenue data in the last month
@app.route('/revenue_data_month')
def revenue_data_month():
    username = session.get('username')
    password = session.get('password')
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'staff_role')
        conn.autocommit = False
        cursor = conn.cursor()
        query = ''
        query = 'CALL staff_month_revenue_direct(\'{}\')'.format(username[6:])
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        direct = float(data['revenue']) if data['revenue'] else None
        query = 'CALL staff_month_revenue_indirect(\'{}\')'.format(username[6:])
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        indirect = float(data['revenue']) if data['revenue'] else None
        data = [{"type":"direct", "value":direct},{"type":"indirect", "value" : indirect}]
        cursor.close()
        conn.commit()
        conn.close()
    else:
        data = []
    return jsonify(data)

#Define a route for passing revenue data in the last year
@app.route('/revenue_data_year')
def revenue_data_year():
    username = session.get('username')
    password = session.get('password')
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'staff_role')
        conn.autocommit = False
        cursor = conn.cursor()
        query = ''
        query = 'CALL staff_year_revenue_direct(\'{}\')'.format(username[6:])
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        direct = float(data['revenue']) if data['revenue'] else None
        query = 'CALL staff_year_revenue_indirect(\'{}\')'.format(username[6:])
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        indirect = float(data['revenue']) if data['revenue'] else None
        data = [{"type":"direct", "value":direct},{"type":"indirect", "value" : indirect}]
        cursor.close()
        conn.commit()
        conn.close()
    else:
        data = []
    return jsonify(data)

#Define a route for passing ticket statistics
@app.route('/ticket_sold_data')
def ticket_sold_data():
    username = session.get('username')
    password = session.get('password')
    if username and password:
        staff_ticket_from = session.get('staff_ticket_from')
        staff_ticket_to = session.get('staff_ticket_to')
        if staff_ticket_from and staff_ticket_to:
            conn = get_conn('localhost', username, password, 'flight_ticket', 'staff_role')
            cursor = conn.cursor()
            query = ''
            query = 'CALL staff_ticket_stats_ranged(\'{}\',\'{}\',\'{}\')'.format(username[6:],staff_ticket_from,staff_ticket_to)
            print('query:', query)
            cursor.execute(query)
            data = cursor.fetchall()
            print(data)
            for line in data:
                line['num_ticket'] = float(line['num_ticket'])
            cursor.close()
            conn.close()
        else:
            conn = get_conn('localhost', username, password, 'flight_ticket', 'staff_role')
            cursor = conn.cursor()
            query = ''
            query = 'CALL staff_ticket_stats_recent(\'{}\')'.format(username[6:])
            print('query:', query)
            cursor.execute(query)
            data = cursor.fetchall()
            print(data)
            for line in data:
                line['num_ticket'] = float(line['num_ticket'])
            cursor.close()
            conn.close()
    else:
        data = []
    return jsonify(data)

#Define a route for staff search result
@app.route('/staff/result', methods=['GET', 'POST'])
def staff_result():
    departure_city = request.form.get('departure_city')
    arrival_city = request.form.get('arrival_city')
    departure_date_from = request.form.get('departure_date_from')
    departure_date_to = request.form.get('departure_date_to')
    arrival_date_from = request.form.get('arrival_date_from')
    arrival_date_to = request.form.get('arrival_date_to')
    username = session.get('username')
    password = session.get('password')
    query = ''
    if departure_city:
        if query == '':
            query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM (flight JOIN airport AS ad ON(flight.departure_airport=ad.airport_name)) JOIN airport AS aa ON(flight.arrival_airport=aa.airport_name) WHERE ad.airport_city=\'{}\''.format(departure_city)
        else:
            query += " AND ad.airport_city=\'{}\'".format(departure_city)
    if arrival_city:
        if query == '':
            query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM (flight JOIN airport AS ad ON(flight.departure_airport=ad.airport_name)) JOIN airport AS aa ON(flight.arrival_airport=aa.airport_name) WHERE aa.airport_city=\'{}\''.format(arrival_city)
        else:
            query += ' AND aa.airport_city=\'{}\''.format(arrival_city)
    if departure_date_from:
        if query == '':
            query = 'SELECT * FROM flight WHERE DATE_FORMAT(departure_time, \'%Y-%m-%e\')>=DATE_FORMAT(\'{}\', \'%Y-%m-%e\')'.format(departure_date_from)
        else:
            query += ' AND DATE_FORMAT(departure_time, \'%Y-%m-%e\')>=DATE_FORMAT(\'{}\', \'%Y-%m-%e\')'.format(departure_date_from)
    if departure_date_to:
        if query == '':
            query = 'SELECT * FROM flight WHERE DATE_FORMAT(departure_time, \'%Y-%m-%e\')<=DATE_FORMAT(\'{}\', \'%Y-%m-%e\')'.format(departure_date_to)
        else:
            query += ' AND DATE_FORMAT(departure_time, \'%Y-%m-%e\')<=DATE_FORMAT(\'{}\', \'%Y-%m-%e\')'.format(departure_date_to)
    if arrival_date_from:
        if query == '':
            query = 'SELECT * FROM flight WHERE DATE_FORMAT(arrival_time, \'%Y-%m-%e\')>=DATE_FORMAT(\'{}\', \'%Y-%m-%e\')'.format(arrival_date_from)
        else:
            query += ' AND DATE_FORMAT(arrival_time, \'%Y-%m-%e\')>=DATE_FORMAT(\'{}\', \'%Y-%m-%e\')'.format(arrival_date_from)
    if arrival_date_to:
        if query == '':
            query = 'SELECT * FROM flight WHERE DATE_FORMAT(arrival_time, \'%Y-%m-%e\')<=DATE_FORMAT(\'{}\', \'%Y-%m-%e\')'.format(arrival_date_to)
        else:
            query += ' AND DATE_FORMAT(arrival_time, \'%Y-%m-%e\')<=DATE_FORMAT(\'{}\', \'%Y-%m-%e\')'.format(arrival_date_to)
    print('query:', query)
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'staff_role')
        conn.autocommit = False
        cursor = conn.cursor()
        username = username[6:]
        query_bar = 'SELECT airline_name FROM airline_staff WHERE username=\'{}\''.format(username)
        print('query:', query_bar)
        cursor.execute(query_bar)
        data = cursor.fetchone()
        print(data)
        airline_name = data.get('airline_name')
        if query:
            query += ' AND airline_name=\'{}\''.format(airline_name)
    else:
        conn = get_conn('localhost', 'default_user', '', 'flight_ticket', 'default_role')
        conn.autocommit = False
        cursor = conn.cursor()
        if query:
            query += ' AND status=\'Upcoming\''
    if query:
        cursor.execute(query)
        data00 = cursor.fetchall()
    else:
        data00 = None
    print(data00)
    query = 'SELECT * FROM airline'
    print('query:', query)
    cursor.execute(query)
    data11 = cursor.fetchall()
    print(data11)
    if username and password:
        query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM flight NATURAL JOIN airline_staff WHERE status=\'Upcoming\' AND username=\'{}\' AND datediff(departure_time, now())<=30'.format(username)
        print('query:', query)
        cursor.execute(query)
        data0 = cursor.fetchall()
        print(data0)
        query = 'SELECT booking_agent_id AS id FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN flight) NATURAL JOIN airline_staff WHERE username=\'{}\' AND booking_agent_id IS NOT NULL AND date_format((now()-INTERVAL 1 month), \'%m\')=date_format(purchase_date, \'%m\') GROUP BY booking_agent_id ORDER BY COUNT(ticket_id) DESC LIMIT 5'.format(username)
        print('query:', query)
        cursor.execute(query)
        data1 = cursor.fetchall()
        print(data1)
        data1 = [id['id'] for id in data1]
        query = 'SELECT booking_agent_id AS id FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN flight) NATURAL JOIN airline_staff WHERE username=\'{}\' AND booking_agent_id IS NOT NULL AND date_format((now()-INTERVAL 1 year), \'%Y\')=date_format(purchase_date, \'%Y\') GROUP BY booking_agent_id ORDER BY COUNT(ticket_id) DESC LIMIT 5'.format(username)
        print('query:', query)
        cursor.execute(query)
        data2 = cursor.fetchall()
        print(data2)
        data2 = [id['id'] for id in data2]
        query = 'SELECT booking_agent_id AS id FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN flight) NATURAL JOIN airline_staff WHERE username=\'{}\' AND booking_agent_id IS NOT NULL AND date_format((now()-INTERVAL 1 year), \'%Y\')=date_format(purchase_date, \'%Y\') GROUP BY booking_agent_id ORDER BY SUM(price) DESC LIMIT 5'.format(username)
        print('query:', query)
        cursor.execute(query)
        data3 = cursor.fetchall()
        print(data3)
        data3 = [id['id'] for id in data3]
        query = 'CALL staff_customer_ticket(\'{}\')'.format(username)
        print('query:', query)
        cursor.execute(query)
        data4 = cursor.fetchall()
        print(data4)
        query = 'SELECT airport_city FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN (flight JOIN airport ON(flight.arrival_airport=airport.airport_name))) NATURAL JOIN airline_staff WHERE username=\'{}\' AND period_diff(date_format(now(), \'%Y%m\'), date_format(purchase_date, \'%Y%m\'))<=3 GROUP BY airport_city ORDER BY COUNT(ticket_id) DESC LIMIT 3'.format(username)
        print('query:', query)
        cursor.execute(query)
        data5 = cursor.fetchall()
        print(data5)
        data5 = [city['airport_city'] for city in data5]
        query = 'SELECT airport_city FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN (flight JOIN airport ON(flight.arrival_airport=airport.airport_name))) NATURAL JOIN airline_staff WHERE username=\'{}\' AND date_format((now()-INTERVAL 1 year), \'%Y\')=date_format(purchase_date, \'%Y\') GROUP BY airport_city ORDER BY COUNT(ticket_id) DESC LIMIT 3'.format(username)
        print('query:', query)
        cursor.execute(query)
        data6 = cursor.fetchall()
        print(data6)
        data6 = [city['airport_city'] for city in data6]
        query = 'SELECT permission_type FROM permission WHERE username=\'{}\''.format(username)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        operator, admin = 0, 0
        for line in data:
            if line['permission_type'] == 'Operator':
                operator = 1
            if line['permission_type'] == 'Admin':
                admin = 1
        query = 'SELECT COUNT(ticket_id) AS amount FROM (purchases NATURAL JOIN ticket) NATURAL JOIN flight WHERE date_format(purchase_date, \'%Y\')=date_format((now() - INTERVAL (1) year), \'%Y\') AND airline_name=\'{}\''.format(airline_name)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        ticketsold_year = data['amount']
        query = 'SELECT COUNT(ticket_id) AS amount FROM (purchases NATURAL JOIN ticket) NATURAL JOIN flight WHERE date_format(purchase_date, \'%Y-%m\')=date_format((now() - INTERVAL (1) month), \'%Y-%m\') AND airline_name=\'{}\''.format(airline_name)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        ticketsold_month = data['amount']
        session.pop('staff_ticket_from', None)
        session.pop('staff_ticket_to', None)
    cursor.close()
    conn.commit()
    conn.close()
    if username and password:
        return render_template('staff_home.html', search_result=data00, username=username, operator=operator, admin=admin, myflight=data0, agent_bynum_month=data1, agent_bynum_year=data2, agent_bycom_year=data3, customers=data4, destination_month=data5, destination_year=data6, ticketsold_year=ticketsold_year, ticketsold_month=ticketsold_month, airline=airline_name)
    else:
        session.clear()
        return render_template('search.html', search_result=data00, airlines=data11)

#Define a route for staff abstract search result
@app.route('/staff/abstract_result', methods=['GET', 'POST'])
def staff_abstract_result():
    searchText = request.form.get('searchText')
    username = session.get('username')
    password = session.get('password')
    query = ''
    if searchText:
        query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM (flight JOIN airport AS ad ON(flight.departure_airport=ad.airport_name)) JOIN airport AS aa ON(flight.arrival_airport=aa.airport_name) WHERE (status LIKE \'%{}%\' OR departure_airport LIKE \'%{}%\' OR arrival_airport LIKE \'%{}%\' OR ad.airport_city LIKE \'%{}%\' OR aa.airport_city LIKE \'%{}%\')'.format(searchText, searchText, searchText, searchText, searchText)
    print('query:', query)
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'staff_role')
        conn.autocommit = False
        cursor = conn.cursor()
        username = username[6:]
        query_bar = 'SELECT airline_name FROM airline_staff WHERE username=\'{}\''.format(username)
        print('query:', query_bar)
        cursor.execute(query_bar)
        data = cursor.fetchone()
        print(data)
        airline_name = data.get('airline_name')
        if query:
            query += ' AND airline_name=\'{}\''.format(airline_name)
    else:
        conn = get_conn('localhost', 'default_user', '', 'flight_ticket', 'default_role')
        conn.autocommit = False
        cursor = conn.cursor()
        if query:
            query += ' AND status = \'Upcoming\''
    if query:
        cursor.execute(query)
        data00 = cursor.fetchall()
    else:
        data00 = None
    print(data00)
    query = 'SELECT * FROM airline'
    print('query:', query)
    cursor.execute(query)
    data11 = cursor.fetchall()
    print(data11)
    if username and password:
        query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM flight NATURAL JOIN airline_staff WHERE status=\'Upcoming\' AND username=\'{}\' AND datediff(departure_time, now())<=30'.format(username)
        print('query:', query)
        cursor.execute(query)
        data0 = cursor.fetchall()
        print(data0)
        query = 'SELECT booking_agent_id AS id FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN flight) NATURAL JOIN airline_staff WHERE username=\'{}\' AND booking_agent_id IS NOT NULL AND date_format((now()-INTERVAL 1 month), \'%m\')=date_format(purchase_date, \'%m\') GROUP BY booking_agent_id ORDER BY COUNT(ticket_id) DESC LIMIT 5'.format(username)
        print('query:', query)
        cursor.execute(query)
        data1 = cursor.fetchall()
        print(data1)
        data1 = [id['id'] for id in data1]
        query = 'SELECT booking_agent_id AS id FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN flight) NATURAL JOIN airline_staff WHERE username=\'{}\' AND booking_agent_id IS NOT NULL AND date_format((now()-INTERVAL 1 year), \'%Y\')=date_format(purchase_date, \'%Y\') GROUP BY booking_agent_id ORDER BY COUNT(ticket_id) DESC LIMIT 5'.format(username)
        print('query:', query)
        cursor.execute(query)
        data2 = cursor.fetchall()
        print(data2)
        data2 = [id['id'] for id in data2]
        query = 'SELECT booking_agent_id AS id FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN flight) NATURAL JOIN airline_staff WHERE username=\'{}\' AND booking_agent_id IS NOT NULL AND date_format((now()-INTERVAL 1 year), \'%Y\')=date_format(purchase_date, \'%Y\') GROUP BY booking_agent_id ORDER BY SUM(price) DESC LIMIT 5'.format(username)
        print('query:', query)
        cursor.execute(query)
        data3 = cursor.fetchall()
        print(data3)
        data3 = [id['id'] for id in data3]
        query = 'CALL staff_customer_ticket(\'{}\')'.format(username)
        print('query:', query)
        cursor.execute(query)
        data4 = cursor.fetchall()
        print(data4)
        query = 'SELECT airport_city FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN (flight JOIN airport ON(flight.arrival_airport=airport.airport_name))) NATURAL JOIN airline_staff WHERE username=\'{}\' AND period_diff(date_format(now(), \'%Y%m\'), date_format(purchase_date, \'%Y%m\'))<=3 GROUP BY airport_city ORDER BY COUNT(ticket_id) DESC LIMIT 3'.format(username)
        print('query:', query)
        cursor.execute(query)
        data5 = cursor.fetchall()
        print(data5)
        data5 = [city['airport_city'] for city in data5]
        query = 'SELECT airport_city FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN (flight JOIN airport ON(flight.arrival_airport=airport.airport_name))) NATURAL JOIN airline_staff WHERE username=\'{}\' AND date_format((now()-INTERVAL 1 year), \'%Y\')=date_format(purchase_date, \'%Y\') GROUP BY airport_city ORDER BY COUNT(ticket_id) DESC LIMIT 3'.format(username)
        print('query:', query)
        cursor.execute(query)
        data6 = cursor.fetchall()
        print(data6)
        data6 = [city['airport_city'] for city in data6]
        query = 'SELECT permission_type FROM permission WHERE username=\'{}\''.format(username)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        operator, admin = 0, 0
        for line in data:
            if line['permission_type'] == 'Operator':
                operator = 1
            if line['permission_type'] == 'Admin':
                admin = 1
        query = 'SELECT COUNT(ticket_id) AS amount FROM (purchases NATURAL JOIN ticket) NATURAL JOIN flight WHERE date_format(purchase_date, \'%Y\')=date_format((now() - INTERVAL (1) year), \'%Y\') AND airline_name=\'{}\''.format(airline_name)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        ticketsold_year = data['amount']
        query = 'SELECT COUNT(ticket_id) AS amount FROM (purchases NATURAL JOIN ticket) NATURAL JOIN flight WHERE date_format(purchase_date, \'%Y-%m\')=date_format((now() - INTERVAL (1) month), \'%Y-%m\') AND airline_name=\'{}\''.format(airline_name)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        ticketsold_month = data['amount']
        session.pop('staff_ticket_from', None)
        session.pop('staff_ticket_to', None)
    cursor.close()
    conn.commit()
    conn.close()
    if username and password:
        return render_template('staff_home.html', search_result=data00, username=username, operator=operator, admin=admin, myflight=data0, agent_bynum_month=data1, agent_bynum_year=data2, agent_bycom_year=data3, customers=data4, destination_month=data5, destination_year=data6, ticketsold_year=ticketsold_year, ticketsold_month=ticketsold_month, airline=airline_name)
    else:
        session.clear()
        return render_template('search.html', search_result=data00, airlines=data11)

#Define a route for staff search result with flight number
@app.route('/staff/number_result', methods=['GET', 'POST'])
def staff_number_result():
    flight_number = request.form.get('flight_number')
    username = session.get('username')
    password = session.get('password')
    query = ''
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'staff_role')
        conn.autocommit = False
        cursor = conn.cursor()
        username = username[6:]
        query_bar = 'SELECT airline_name FROM airline_staff WHERE username=\'{}\''.format(username)
        print('query:', query_bar)
        cursor.execute(query_bar)
        data = cursor.fetchone()
        print(data)
        airline_name = data.get('airline_name')
        if flight_number:
            query = 'SELECT * FROM flight WHERE airline_name=\'{}\' AND flight_num={}'.format(airline_name,flight_number)
        print('query:', query)
        if query:
            cursor.execute(query)
            data00 = cursor.fetchall()
        else:
            data00 = None
        print(data00)
        query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM flight NATURAL JOIN airline_staff WHERE status=\'Upcoming\' AND username=\'{}\' AND datediff(departure_time, now())<=30'.format(username)
        print('query:', query)
        cursor.execute(query)
        data0 = cursor.fetchall()
        print(data0)
        query = 'SELECT booking_agent_id AS id FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN flight) NATURAL JOIN airline_staff WHERE username=\'{}\' AND booking_agent_id IS NOT NULL AND date_format((now()-INTERVAL 1 month), \'%m\')=date_format(purchase_date, \'%m\') GROUP BY booking_agent_id ORDER BY COUNT(ticket_id) DESC LIMIT 5'.format(username)
        print('query:', query)
        cursor.execute(query)
        data1 = cursor.fetchall()
        print(data1)
        data1 = [id['id'] for id in data1]
        query = 'SELECT booking_agent_id AS id FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN flight) NATURAL JOIN airline_staff WHERE username=\'{}\' AND booking_agent_id IS NOT NULL AND date_format((now()-INTERVAL 1 year), \'%Y\')=date_format(purchase_date, \'%Y\') GROUP BY booking_agent_id ORDER BY COUNT(ticket_id) DESC LIMIT 5'.format(username)
        print('query:', query)
        cursor.execute(query)
        data2 = cursor.fetchall()
        print(data2)
        data2 = [id['id'] for id in data2]
        query = 'SELECT booking_agent_id AS id FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN flight) NATURAL JOIN airline_staff WHERE username=\'{}\' AND booking_agent_id IS NOT NULL AND date_format((now()-INTERVAL 1 year), \'%Y\')=date_format(purchase_date, \'%Y\') GROUP BY booking_agent_id ORDER BY SUM(price) DESC LIMIT 5'.format(username)
        print('query:', query)
        cursor.execute(query)
        data3 = cursor.fetchall()
        print(data3)
        data3 = [id['id'] for id in data3]
        query = 'CALL staff_customer_ticket(\'{}\')'.format(username)
        print('query:', query)
        cursor.execute(query)
        data4 = cursor.fetchall()
        print(data4)
        query = 'SELECT airport_city FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN (flight JOIN airport ON(flight.arrival_airport=airport.airport_name))) NATURAL JOIN airline_staff WHERE username=\'{}\' AND period_diff(date_format(now(), \'%Y%m\'), date_format(purchase_date, \'%Y%m\'))<=3 GROUP BY airport_city ORDER BY COUNT(ticket_id) DESC LIMIT 3'.format(username)
        print('query:', query)
        cursor.execute(query)
        data5 = cursor.fetchall()
        print(data5)
        data5 = [city['airport_city'] for city in data5]
        query = 'SELECT airport_city FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN (flight JOIN airport ON(flight.arrival_airport=airport.airport_name))) NATURAL JOIN airline_staff WHERE username=\'{}\' AND date_format((now()-INTERVAL 1 year), \'%Y\')=date_format(purchase_date, \'%Y\') GROUP BY airport_city ORDER BY COUNT(ticket_id) DESC LIMIT 3'.format(username)
        print('query:', query)
        cursor.execute(query)
        data6 = cursor.fetchall()
        print(data6)
        data6 = [city['airport_city'] for city in data6]
        query = 'SELECT permission_type FROM permission WHERE username=\'{}\''.format(username)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        operator, admin = 0, 0
        for line in data:
            if line['permission_type'] == 'Operator':
                operator = 1
            if line['permission_type'] == 'Admin':
                admin = 1
        query = 'SELECT COUNT(ticket_id) AS amount FROM (purchases NATURAL JOIN ticket) NATURAL JOIN flight WHERE date_format(purchase_date, \'%Y\')=date_format((now() - INTERVAL (1) year), \'%Y\') AND airline_name=\'{}\''.format(airline_name)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        ticketsold_year = data['amount']
        query = 'SELECT COUNT(ticket_id) AS amount FROM (purchases NATURAL JOIN ticket) NATURAL JOIN flight WHERE date_format(purchase_date, \'%Y-%m\')=date_format((now() - INTERVAL (1) month), \'%Y-%m\') AND airline_name=\'{}\''.format(airline_name)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        ticketsold_month = data['amount']
        session.pop('staff_ticket_from', None)
        session.pop('staff_ticket_to', None)
        cursor.close()
        conn.commit()
        conn.close()
        return render_template('staff_home.html', search_result=data00, username=username, operator=operator, admin=admin, myflight=data0, agent_bynum_month=data1, agent_bynum_year=data2, agent_bycom_year=data3, customers=data4, destination_month=data5, destination_year=data6, ticketsold_year=ticketsold_year, ticketsold_month=ticketsold_month, airline=airline_name)
    else:
        cursor.close()
        conn.commit()
        conn.close()
        session.clear()
        return redirect(url_for('search'))

#Define a route for flight update
@app.route('/staff/flight_update', methods=['GET', 'POST'])
def staff_flight_update():
    status = request.form.get('status')
    for k in request.form.keys():
        if k != 'status':
            ticket_info = k.split(',')
    airline_name = ticket_info[0]
    flight_num = ticket_info[1]
    username = session.get('username')
    password = session.get('password')
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'operator_role')
        conn.autocommit = False
        cursor = conn.cursor()
        query = ''
        query = 'UPDATE flight SET status=\'{}\' WHERE airline_name=\'{}\' AND flight_num=\'{}\''.format(status,airline_name,flight_num)
        print('query:', query)
        cursor.execute(query)
        username = username[6:]
        query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM flight NATURAL JOIN airline_staff WHERE status=\'Upcoming\' AND username=\'{}\' AND datediff(departure_time, now())<=30'.format(username)
        print('query:', query)
        cursor.execute(query)
        data0 = cursor.fetchall()
        print(data0)
        query = 'SELECT booking_agent_id AS id FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN flight) NATURAL JOIN airline_staff WHERE username=\'{}\' AND booking_agent_id IS NOT NULL AND date_format((now()-INTERVAL 1 month), \'%m\')=date_format(purchase_date, \'%m\') GROUP BY booking_agent_id ORDER BY COUNT(ticket_id) DESC LIMIT 5'.format(username)
        print('query:', query)
        cursor.execute(query)
        data1 = cursor.fetchall()
        print(data1)
        data1 = [id['id'] for id in data1]
        query = 'SELECT booking_agent_id AS id FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN flight) NATURAL JOIN airline_staff WHERE username=\'{}\' AND booking_agent_id IS NOT NULL AND date_format((now()-INTERVAL 1 year), \'%Y\')=date_format(purchase_date, \'%Y\') GROUP BY booking_agent_id ORDER BY COUNT(ticket_id) DESC LIMIT 5'.format(username)
        print('query:', query)
        cursor.execute(query)
        data2 = cursor.fetchall()
        print(data2)
        data2 = [id['id'] for id in data2]
        query = 'SELECT booking_agent_id AS id FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN flight) NATURAL JOIN airline_staff WHERE username=\'{}\' AND booking_agent_id IS NOT NULL AND date_format((now()-INTERVAL 1 year), \'%Y\')=date_format(purchase_date, \'%Y\') GROUP BY booking_agent_id ORDER BY SUM(price) DESC LIMIT 5'.format(username)
        print('query:', query)
        cursor.execute(query)
        data3 = cursor.fetchall()
        print(data3)
        data3 = [id['id'] for id in data3]
        query = 'CALL staff_customer_ticket(\'{}\')'.format(username)
        print('query:', query)
        cursor.execute(query)
        data4 = cursor.fetchall()
        print(data4)
        query = 'SELECT airport_city FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN (flight JOIN airport ON(flight.arrival_airport=airport.airport_name))) NATURAL JOIN airline_staff WHERE username=\'{}\' AND period_diff(date_format(now(), \'%Y%m\'), date_format(purchase_date, \'%Y%m\'))<=3 GROUP BY airport_city ORDER BY COUNT(ticket_id) DESC LIMIT 3'.format(username)
        print('query:', query)
        cursor.execute(query)
        data5 = cursor.fetchall()
        print(data5)
        data5 = [city['airport_city'] for city in data5]
        query = 'SELECT airport_city FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN (flight JOIN airport ON(flight.arrival_airport=airport.airport_name))) NATURAL JOIN airline_staff WHERE username=\'{}\' AND date_format((now()-INTERVAL 1 year), \'%Y\')=date_format(purchase_date, \'%Y\') GROUP BY airport_city ORDER BY COUNT(ticket_id) DESC LIMIT 3'.format(username)
        print('query:', query)
        cursor.execute(query)
        data6 = cursor.fetchall()
        print(data6)
        data6 = [city['airport_city'] for city in data6]
        query = 'SELECT permission_type FROM permission WHERE username=\'{}\''.format(username)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        operator, admin = 0, 0
        for line in data:
            if line['permission_type'] == 'Operator':
                operator = 1
            if line['permission_type'] == 'Admin':
                admin = 1
        query = 'SELECT airline_name FROM airline_staff WHERE username=\'{}\''.format(username)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        airline_name = data.get('airline_name')
        query = 'SELECT COUNT(ticket_id) AS amount FROM (purchases NATURAL JOIN ticket) NATURAL JOIN flight WHERE date_format(purchase_date, \'%Y\')=date_format((now() - INTERVAL (1) year), \'%Y\') AND airline_name=\'{}\''.format(airline_name)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        ticketsold_year = data['amount']
        query = 'SELECT COUNT(ticket_id) AS amount FROM (purchases NATURAL JOIN ticket) NATURAL JOIN flight WHERE date_format(purchase_date, \'%Y-%m\')=date_format((now() - INTERVAL (1) month), \'%Y-%m\') AND airline_name=\'{}\''.format(airline_name)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        ticketsold_month = data['amount']
        cursor.close()
        conn.commit()
        conn.close()
        session.pop('staff_ticket_from', None)
        session.pop('staff_ticket_to', None)
        return render_template('staff_home.html', username=username, operator=operator, admin=admin, myflight=data0, agent_bynum_month=data1, agent_bynum_year=data2, agent_bycom_year=data3, customers=data4, destination_month=data5, destination_year=data6, ticketsold_year=ticketsold_year, ticketsold_month=ticketsold_month, airline=airline_name)
    else:
        session.clear()
        return redirect(url_for('search'))

#Define a route for viewing customers
@app.route('/staff/view_customer', methods=['GET', 'POST'])
def staff_view_customer():
    ticket_info = list(request.form.keys())[0].split(',')
    airline_name = ticket_info[0]
    flight_num = ticket_info[1]
    username = session.get('username')
    password = session.get('password')
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'staff_role')
        cursor = conn.cursor()
        query = ''
        query = 'SELECT email, name FROM (purchases JOIN customer ON(purchases.customer_email=customer.email)) NATURAL JOIN ticket WHERE airline_name=\'{}\' AND flight_num=\'{}\''.format(airline_name,flight_num)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        cursor.close()
        conn.close()
        return render_template('staff_flightcustomer.html', flight_num=flight_num, airline_name=airline_name, customer_result=data)
    else:
        session.clear()
        return redirect(url_for('search'))

#Define a route for viewing flights
@app.route('/staff/view_flight', methods=['GET', 'POST'])
def staff_view_flight():
    email = list(request.form.keys())[0]
    username = session.get('username')
    password = session.get('password')
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'staff_role')
        conn.autocommit = False
        cursor = conn.cursor()
        query = ''
        query = 'SELECT airline_name FROM airline_staff WHERE username=\'{}\''.format(username[6:])
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        airline_name = data.get('airline_name')
        query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM (purchases NATURAL JOIN ticket) NATURAL JOIN flight WHERE customer_email=\'{}\' AND airline_name=\'{}\''.format(email,airline_name)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        cursor.close()
        conn.commit()
        conn.close()
        return render_template('staff_customerflight.html', username=email, flight_result=data)
    else:
        session.clear()
        return redirect(url_for('search'))

#Define a route for track report
@app.route('/staff/track_report', methods=['GET', 'POST'])
def staff_track_report():
    staff_ticket_from = request.form.get('from')
    staff_ticket_to = request.form.get('to')
    session['staff_ticket_from'] = staff_ticket_from
    session['staff_ticket_to'] = staff_ticket_to
    username = session.get('username')
    password = session.get('password')
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'staff_role')
        conn.autocommit = False
        cursor = conn.cursor()
        query = ''
        username = username[6:]
        query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM flight NATURAL JOIN airline_staff WHERE status=\'Upcoming\' AND username=\'{}\' AND datediff(departure_time, now())<=30'.format(username)
        print('query:', query)
        cursor.execute(query)
        data0 = cursor.fetchall()
        print(data0)
        query = 'SELECT booking_agent_id AS id FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN flight) NATURAL JOIN airline_staff WHERE username=\'{}\' AND booking_agent_id IS NOT NULL AND date_format((now()-INTERVAL 1 month), \'%m\')=date_format(purchase_date, \'%m\') GROUP BY booking_agent_id ORDER BY COUNT(ticket_id) DESC LIMIT 5'.format(username)
        print('query:', query)
        cursor.execute(query)
        data1 = cursor.fetchall()
        print(data1)
        data1 = [id['id'] for id in data1]
        query = 'SELECT booking_agent_id AS id FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN flight) NATURAL JOIN airline_staff WHERE username=\'{}\' AND booking_agent_id IS NOT NULL AND date_format((now()-INTERVAL 1 year), \'%Y\')=date_format(purchase_date, \'%Y\') GROUP BY booking_agent_id ORDER BY COUNT(ticket_id) DESC LIMIT 5'.format(username)
        print('query:', query)
        cursor.execute(query)
        data2 = cursor.fetchall()
        print(data2)
        data2 = [id['id'] for id in data2]
        query = 'SELECT booking_agent_id AS id FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN flight) NATURAL JOIN airline_staff WHERE username=\'{}\' AND booking_agent_id IS NOT NULL AND date_format((now()-INTERVAL 1 year), \'%Y\')=date_format(purchase_date, \'%Y\') GROUP BY booking_agent_id ORDER BY SUM(price) DESC LIMIT 5'.format(username)
        print('query:', query)
        cursor.execute(query)
        data3 = cursor.fetchall()
        print(data3)
        data3 = [id['id'] for id in data3]
        query = 'CALL staff_customer_ticket(\'{}\')'.format(username)
        print('query:', query)
        cursor.execute(query)
        data4 = cursor.fetchall()
        print(data4)
        query = 'SELECT airport_city FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN (flight JOIN airport ON(flight.arrival_airport=airport.airport_name))) NATURAL JOIN airline_staff WHERE username=\'{}\' AND period_diff(date_format(now(), \'%Y%m\'), date_format(purchase_date, \'%Y%m\'))<=3 GROUP BY airport_city ORDER BY COUNT(ticket_id) DESC LIMIT 3'.format(username)
        print('query:', query)
        cursor.execute(query)
        data5 = cursor.fetchall()
        print(data5)
        data5 = [city['airport_city'] for city in data5]
        query = 'SELECT airport_city FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN (flight JOIN airport ON(flight.arrival_airport=airport.airport_name))) NATURAL JOIN airline_staff WHERE username=\'{}\' AND date_format((now()-INTERVAL 1 year), \'%Y\')=date_format(purchase_date, \'%Y\') GROUP BY airport_city ORDER BY COUNT(ticket_id) DESC LIMIT 3'.format(username)
        print('query:', query)
        cursor.execute(query)
        data6 = cursor.fetchall()
        print(data6)
        data6 = [city['airport_city'] for city in data6]
        query = 'SELECT permission_type FROM permission WHERE username=\'{}\''.format(username)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        operator, admin = 0, 0
        for line in data:
            if line['permission_type'] == 'Operator':
                operator = 1
            if line['permission_type'] == 'Admin':
                admin = 1
        query = 'SELECT airline_name FROM airline_staff WHERE username=\'{}\''.format(username)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        airline_name = data.get('airline_name')
        query = 'SELECT COUNT(ticket_id) AS amount FROM (purchases NATURAL JOIN ticket) NATURAL JOIN flight WHERE date_format(purchase_date, \'%Y\')=date_format((now() - INTERVAL (1) year), \'%Y\') AND airline_name=\'{}\''.format(airline_name)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        ticketsold_year = data['amount']
        query = 'SELECT COUNT(ticket_id) AS amount FROM (purchases NATURAL JOIN ticket) NATURAL JOIN flight WHERE date_format(purchase_date, \'%Y-%m\')=date_format((now() - INTERVAL (1) month), \'%Y-%m\') AND airline_name=\'{}\''.format(airline_name)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        ticketsold_month = data['amount']
        query = 'CALL staff_ticket_sum_ranged(\'{}\', \'{}\', \'{}\')'.format(username, staff_ticket_from, staff_ticket_to)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        ticketsold_stime = data['amount']
        cursor.close()
        conn.commit()
        conn.close()
        return render_template('staff_home.html', username=username, operator=operator, admin=admin, myflight=data0, agent_bynum_month=data1, agent_bynum_year=data2, agent_bycom_year=data3, customers=data4, destination_month=data5, destination_year=data6, ticketsold_year=ticketsold_year, ticketsold_month=ticketsold_month, ticketsold_stime=ticketsold_stime, airline=airline_name)
    else:
        session.clear()
        return redirect(url_for('search'))
    
#Define a route for admin home
@app.route('/staff_admin/home')
def staff_admin_home():
    username = session.get('username')
    return render_template('staff_admin_home.html', username=username[6:])

#Define a route for creating new flights
@app.route('/staff_admin/new_flights', methods=['GET', 'POST'])
def staff_admin_new_flights():
    flight_num = request.form.get('flight_num')
    departure_airport = request.form.get('departure_airport')
    departure_time = request.form.get('departure_time')
    arrival_airport = request.form.get('arrival_airport')
    arrival_time = request.form.get('arrival_time')
    price = request.form.get('price')
    status = request.form.get('status')
    plane_id = request.form.get('plane_id')
    departure_time = departure_time.replace('T', ' ')[:16]+':00'
    arrival_time = arrival_time.replace('T', ' ')[:16]+':00'
    username = session.get('username')
    password = session.get('password')
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'admin_role')
        conn.autocommit = False
        cursor = conn.cursor()
        query = ''
        query = 'SELECT airline_name FROM airline_staff WHERE username=\'{}\''.format(username[6:])
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        airline_name = data.get('airline_name')
        query = 'SELECT * FROM airplane WHERE airline_name=\'{}\' AND airplane_id={}'.format(airline_name,plane_id)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        if data:
            query = 'SELECT flight_num FROM flight WHERE flight_num={} AND airline_name=\'{}\''.format(flight_num,airline_name)
            print('query:', query)
            cursor.execute(query)
            data = cursor.fetchone()
            print(data)
            if data:
                cursor.close()
                conn.commit()
                conn.close()
                error = 'The flight number is already used!'
                return render_template('staff_admin_home.html', error=error, username=username[6:])
            query = 'SELECT a.airport_name FROM airport AS a, airport AS b WHERE a.airport_name=\'{}\' AND b.airport_name=\'{}\''.format(departure_airport, arrival_airport)
            print('query:', query)
            cursor.execute(query)
            data = cursor.fetchone()
            print(data)
            if not data:
                cursor.close()
                conn.commit()
                conn.close()
                error = 'Check the airport name(s)!'
                return render_template('staff_admin_home.html', error=error, username=username[6:])
            query = 'CALL admin_check_new_flight(\'{}\',{},\'{}\',\'{}\')'.format(airline_name,plane_id,departure_time,arrival_time)
            print('query:', query)
            cursor.execute(query)
            data = cursor.fetchone()
            print(data)
            if data:
                cursor.close()
                conn.commit()
                conn.close()
                error = 'Time conflict!'
                return render_template('staff_admin_home.html', error=error, username=username[6:])
            else:
                query = 'INSERT INTO flight VALUES(\'{}\', {}, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', {})'.format(airline_name,flight_num,departure_airport,departure_time,arrival_airport,arrival_time,price,status,plane_id)
                print('query:', query)
                cursor.execute(query)
                query = 'SELECT MAX(ticket_id) AS id FROM ticket WHERE 1'
                print('query:', query)
                cursor.execute(query)
                data = cursor.fetchone()
                print(data)
                ticket_id_start = int(data['id'])+1
                query = 'SELECT seats FROM airplane WHERE airline_name=\'{}\' AND airplane_id={}'.format(airline_name,plane_id)
                print('query:', query)
                cursor.execute(query)
                data = cursor.fetchone()
                print(data)
                seats = int(data['seats'])
                for i in range(seats):
                    query = 'INSERT INTO ticket VALUES({}, \'{}\', {})'.format(ticket_id_start+i,airline_name, flight_num)
                    print('query:', query)
                    cursor.execute(query)
                cursor.close()
                conn.commit()
                conn.close()
                return render_template('staff_admin_home.html', username=username[6:])
        else:
            cursor.close()
            conn.commit()
            conn.close()
            error = 'Check your airplane id!'
            return render_template('staff_admin_home.html', error=error, username=username[6:])
    else:
        session.clear()
        return redirect(url_for('search'))
    
#Define a route for creating new airplanes
@app.route('/staff_admin/new_airplanes', methods=['GET', 'POST'])
def staff_admin_new_airplanes():
    airplane_id = request.form.get('airplane_id')
    seats = request.form.get('seats')
    username = session.get('username')
    password = session.get('password')
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'admin_role')
        conn.autocommit = False
        cursor = conn.cursor()
        query = ''
        query = 'SELECT airline_name FROM airline_staff WHERE username=\'{}\''.format(username[6:])
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        airline_name = data.get('airline_name')
        query = 'SELECT airline_name FROM airplane WHERE airline_name=\'{}\' AND airplane_id=\'{}\''.format(airline_name,airplane_id)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        if data:
            cursor.close()
            conn.commit()
            conn.close()
            error = 'The airplane id is already used!'
            return render_template('staff_admin_home.html', error=error, username=username[6:])
        else:
            query = 'INSERT INTO airplane VALUES(\'{}\', {}, {})'.format(airline_name, airplane_id, seats)
            print('query:', query)
            cursor.execute(query)
            cursor.close()
            conn.commit()
            conn.close()
            return render_template('staff_admin_home.html', username=username[6:])
    else:
        session.clear()
        return redirect(url_for('search'))

#Define a route for creating new airports
@app.route('/staff_admin/new_airports', methods=['GET', 'POST'])
def staff_admin_new_airports():
    airport_name = request.form.get('airport_name')
    airport_city = request.form.get('airport_city')
    username = session.get('username')
    password = session.get('password')
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'admin_role')
        conn.autocommit = False
        cursor = conn.cursor()
        query = ''
        query = 'SELECT airport_name FROM airport WHERE airport_name=\'{}\''.format(airport_name)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        if data:
            cursor.close()
            conn.commit()
            conn.close()
            error = 'The airport id already exists!'
            return render_template('staff_admin_home.html', error=error, username=username[6:])
        else:
            query = 'INSERT INTO airport VALUES(\'{}\', \'{}\')'.format(airport_name, airport_city)
            print('query:', query)
            cursor.execute(query)
            cursor.close()
            conn.commit()
            conn.close()
            return render_template('staff_admin_home.html', username=username[6:])
    else:
        session.clear()
        return redirect(url_for('search'))

#Define a route for granting new permission
@app.route('/staff_admin/new_permission', methods=['GET', 'POST'])
def staff_admin_new_permission():
    target_username = request.form.get('username')
    permission = request.form.get('permission')
    username = session.get('username')
    password = session.get('password')
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'admin_role')
        conn.autocommit = False
        cursor = conn.cursor()
        query = ''
        query = 'SELECT airline_name FROM airline_staff WHERE username=\'{}\''.format(username[6:])
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        airline_name = data.get('airline_name')
        query = 'SELECT username FROM airline_staff WHERE username=\'{}\' AND airline_name=\'{}\''.format(target_username,airline_name)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        if data:
            query = 'SELECT permission_type FROM permission WHERE username=\'{}\''.format(target_username)
            print('query:', query)
            cursor.execute(query)
            data = cursor.fetchall()
            print(data)
            admin = False
            for line in data:
                if line['permission_type'] == 'Admin':
                    admin = True
                if permission == line['permission_type']:
                    cursor.close()
                    conn.commit()
                    conn.close()
                    error = 'The permission type is already owned!'
                    return render_template('staff_admin_home.html', error=error, username=username[6:])
            query = 'INSERT INTO permission VALUES(\'{}\', \'{}\')'.format(target_username,permission)
            print('query:', query)
            cursor.execute(query)
            if not admin:
                if permission == 'Admin':
                    query = 'GRANT admin_role TO \'staff_{}\'@\'localhost\' WITH ADMIN OPTION'.format(target_username)
                    print('query:', query)
                    cursor.execute(query)
                    query = 'GRANT operator_role TO \'staff_{}\'@\'localhost\' WITH ADMIN OPTION'.format(target_username)
                    print('query:', query)
                    cursor.execute(query)
                else:
                    query = 'GRANT operator_role TO \'staff_{}\'@\'localhost\''.format(target_username)
                    print('query:', query)
                    cursor.execute(query)
            cursor.close()
            conn.commit()
            conn.close()
            return render_template('staff_admin_home.html', username=username[6:])
        else:
            cursor.close()
            conn.commit()
            conn.close()
            error = 'Check the username!'
            return render_template('staff_admin_home.html', error=error, username=username[6:])
    else:
        session.clear()
        return redirect(url_for('search'))

#Define a route for granting new agents
@app.route('/staff_admin/new_agents', methods=['GET', 'POST'])
def staff_admin_new_agents():
    email = request.form.get('email')
    username = session.get('username')
    password = session.get('password')
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'admin_role')
        conn.autocommit = False
        cursor = conn.cursor()
        query = ''
        query = 'SELECT airline_name FROM airline_staff WHERE username=\'{}\''.format(username[6:])
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        airline_name = data.get('airline_name')
        query = 'SELECT email FROM booking_agent WHERE email=\'{}\''.format(email)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        if data:
            query = 'SELECT email FROM booking_agent_work_for WHERE email=\'{}\' AND airline_name=\'{}\''.format(email,airline_name)
            print('query:', query)
            cursor.execute(query)
            data = cursor.fetchone()
            print(data)
            if data:
                cursor.close()
                conn.commit()
                conn.close()
                error = 'The agent is already working for your airline!'
                return render_template('staff_admin_home.html', error=error, username=username[6:])
            else:
                query = 'INSERT INTO booking_agent_work_for VALUES(\'{}\', \'{}\')'.format(email, airline_name)
                print('query:', query)
                cursor.execute(query)
                cursor.close()
                conn.commit()
                conn.close()
                return render_template('staff_admin_home.html', username=username[6:])
        else:
            cursor.close()
            conn.commit()
            conn.close()
            error = 'Check the email!'
            return render_template('staff_admin_home.html', error=error, username=username[6:])
    else:
        session.clear()
        return redirect(url_for('search'))

#Define a route for staff back to home
@app.route('/staff/back', methods=['GET', 'POST'])
def staff_back():
    username = session.get('username')
    password = session.get('password')
    if username and password:
        conn = get_conn('localhost', username, password, 'flight_ticket', 'staff_role')
        conn.autocommit = False
        cursor = conn.cursor()
        query = ''
        username = username[6:]
        query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM flight NATURAL JOIN airline_staff WHERE status=\'Upcoming\' AND username=\'{}\' AND datediff(departure_time, now())<=30'.format(username)
        print('query:', query)
        cursor.execute(query)
        data0 = cursor.fetchall()
        print(data0)
        query = 'SELECT booking_agent_id AS id FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN flight) NATURAL JOIN airline_staff WHERE username=\'{}\' AND booking_agent_id IS NOT NULL AND date_format((now()-INTERVAL 1 month), \'%m\')=date_format(purchase_date, \'%m\') GROUP BY booking_agent_id ORDER BY COUNT(ticket_id) DESC LIMIT 5'.format(username)
        print('query:', query)
        cursor.execute(query)
        data1 = cursor.fetchall()
        print(data1)
        data1 = [id['id'] for id in data1]
        query = 'SELECT booking_agent_id AS id FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN flight) NATURAL JOIN airline_staff WHERE username=\'{}\' AND booking_agent_id IS NOT NULL AND date_format((now()-INTERVAL 1 year), \'%Y\')=date_format(purchase_date, \'%Y\') GROUP BY booking_agent_id ORDER BY COUNT(ticket_id) DESC LIMIT 5'.format(username)
        print('query:', query)
        cursor.execute(query)
        data2 = cursor.fetchall()
        print(data2)
        data2 = [id['id'] for id in data2]
        query = 'SELECT booking_agent_id AS id FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN flight) NATURAL JOIN airline_staff WHERE username=\'{}\' AND booking_agent_id IS NOT NULL AND date_format((now()-INTERVAL 1 year), \'%Y\')=date_format(purchase_date, \'%Y\') GROUP BY booking_agent_id ORDER BY SUM(price) DESC LIMIT 5'.format(username)
        print('query:', query)
        cursor.execute(query)
        data3 = cursor.fetchall()
        print(data3)
        data3 = [id['id'] for id in data3]
        query = 'CALL staff_customer_ticket(\'{}\')'.format(username)
        print('query:', query)
        cursor.execute(query)
        data4 = cursor.fetchall()
        print(data4)
        query = 'SELECT airport_city FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN (flight JOIN airport ON(flight.arrival_airport=airport.airport_name))) NATURAL JOIN airline_staff WHERE username=\'{}\' AND period_diff(date_format(now(), \'%Y%m\'), date_format(purchase_date, \'%Y%m\'))<=3 GROUP BY airport_city ORDER BY COUNT(ticket_id) DESC LIMIT 3'.format(username)
        print('query:', query)
        cursor.execute(query)
        data5 = cursor.fetchall()
        print(data5)
        data5 = [city['airport_city'] for city in data5]
        query = 'SELECT airport_city FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN (flight JOIN airport ON(flight.arrival_airport=airport.airport_name))) NATURAL JOIN airline_staff WHERE username=\'{}\' AND date_format((now()-INTERVAL 1 year), \'%Y\')=date_format(purchase_date, \'%Y\') GROUP BY airport_city ORDER BY COUNT(ticket_id) DESC LIMIT 3'.format(username)
        print('query:', query)
        cursor.execute(query)
        data6 = cursor.fetchall()
        print(data6)
        data6 = [city['airport_city'] for city in data6]
        query = 'SELECT permission_type FROM permission WHERE username=\'{}\''.format(username)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        operator, admin = 0, 0
        for line in data:
            if line['permission_type'] == 'Operator':
                operator = 1
            if line['permission_type'] == 'Admin':
                admin = 1
        query = 'SELECT airline_name FROM airline_staff WHERE username=\'{}\''.format(username)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        airline_name = data.get('airline_name')
        query = 'SELECT COUNT(ticket_id) AS amount FROM (purchases NATURAL JOIN ticket) NATURAL JOIN flight WHERE date_format(purchase_date, \'%Y\')=date_format((now() - INTERVAL (1) year), \'%Y\') AND airline_name=\'{}\''.format(airline_name)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        ticketsold_year = data['amount']
        query = 'SELECT COUNT(ticket_id) AS amount FROM (purchases NATURAL JOIN ticket) NATURAL JOIN flight WHERE date_format(purchase_date, \'%Y-%m\')=date_format((now() - INTERVAL (1) month), \'%Y-%m\') AND airline_name=\'{}\''.format(airline_name)
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        ticketsold_month = data['amount']
        cursor.close()
        conn.commit()
        conn.close()
        session.pop('staff_ticket_from', None)
        session.pop('staff_ticket_to', None)
        return render_template('staff_home.html', username=username, operator=operator, admin=admin, myflight=data0, agent_bynum_month=data1, agent_bynum_year=data2, agent_bycom_year=data3, customers=data4, destination_month=data5, destination_year=data6, ticketsold_year=ticketsold_year, ticketsold_month=ticketsold_month, airline=airline_name)
    else:
        session.clear()
        return redirect(url_for('search'))

#Define a route for login
@app.route('/login')
def login():
    return render_template('login.html')

#Define a route for login branch
@app.route('/login/login_branch', methods=['GET', 'POST'])
def login_branch():
    email = request.form.get('email')
    password = request.form.get('password')
    id = request.form.get('id')
    login_type = request.form.get('login_type')
    conn = get_conn('localhost', 'default_user', '', 'flight_ticket', 'register_role')
    conn.autocommit = False
    cursor = conn.cursor()
    query = ''
    query = 'SELECT md5(\'{}\')'.format(password)
    print('query:', query)
    cursor.execute(query)
    data = cursor.fetchone()
    password = data['md5(\'{}\')'.format(password)]
    if login_type == 'customer':
        query = 'SELECT name FROM customer WHERE email=\'{}\' AND password=\'{}\''.format(email,password) 
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        if data:
            cursor.close()
            conn.commit()
            conn.close()
            session['username'] = 'customer_{}'.format(email)
            session['password'] = password
            conn = get_conn('localhost', 'customer_{}'.format(email), password, 'flight_ticket', 'customer_role')
            conn.autocommit = False
            cursor = conn.cursor()
            query = ''
            query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM ((customer JOIN purchases ON(customer.email=purchases.customer_email)) NATURAL JOIN ticket) NATURAL JOIN flight WHERE status=\'Upcoming\' AND email=\'{}\''.format(email)
            print('query:', query)
            cursor.execute(query)
            data0 = cursor.fetchall()
            print(data0)
            query = 'SELECT * FROM airline'
            print('query:', query)
            cursor.execute(query)
            data1 = cursor.fetchall()
            print(data1)
            name = data.get('name')
            cursor.close()
            conn.commit()
            conn.close()
            session.pop('customer_track_from', None)
            session.pop('customer_track_to', None)
            return render_template('customer_home.html', name=name, myflight=data0, airlines=data1)
        else:
            error = 'Wrong password or wrong email!'
            cursor.close()
            conn.commit()
            conn.close()
            return render_template('login.html', error=error)
    elif login_type == 'booking_agent':
        query = 'SELECT email FROM booking_agent WHERE email=\'{}\' AND password=\'{}\' AND booking_agent_id=\'{}\''.format(email,password, id) 
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        if data:
            cursor.close()
            conn.commit()
            conn.close()
            session['username'] = 'agent_{}'.format(email)
            session['password'] = password
            conn = get_conn('localhost', 'agent_{}'.format(email), password, 'flight_ticket', 'agent_role')
            conn.autocommit = False
            cursor = conn.cursor()
            query = ''
            query = 'SELECT * FROM airline'
            print('query:', query)
            cursor.execute(query)
            data0 = cursor.fetchall()
            print(data0)
            query = 'SELECT customer_email, airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM ((purchases NATURAL JOIN booking_agent) NATURAL JOIN ticket) NATURAL JOIN flight WHERE status=\'Upcoming\' AND email=\'{}\''.format(email)
            print('query:', query)
            cursor.execute(query)
            data1 = cursor.fetchall()
            print(data1)
            query = 'SELECT sum(price)*0.1 AS total_commission, avg(price)*0.1 AS avg_commission, count(ticket_id) AS total_tickets FROM ((booking_agent NATURAL JOIN purchases) NATURAL JOIN ticket) NATURAL JOIN flight WHERE datediff(now(), purchase_date)<=30 AND email=\'{}\''.format(email)
            print('query:', query)
            cursor.execute(query)
            data = cursor.fetchone()
            print(data)
            total_commission = float(data.get('total_commission')) if data.get('total_commission') else None
            average_commission = float(data.get('avg_commission')) if data.get('avg_commission') else None
            total_tickets = data.get('total_tickets')
            print('total_commission:', total_commission)
            print('average_commission', average_commission)
            cursor.close()
            conn.commit()
            conn.close()
            return render_template('agent_home.html', airlines=data0, myflight=data1, total_commission=total_commission, average_commission=average_commission, total_tickets=total_tickets, name=email)
        else:
            error = 'Wrong password or wrong email!'
            cursor.close()
            conn.commit()
            conn.close()
            return render_template('login.html', error=error)
    elif login_type == 'staff':
        query = 'SELECT username FROM airline_staff WHERE username=\'{}\' AND password=\'{}\''.format(email,password) 
        print('query:', query)
        cursor.execute(query)
        data = cursor.fetchone()
        if data:
            cursor.close()
            conn.commit()
            conn.close()
            session['username'] = 'staff_{}'.format(email)
            session['password'] = password
            conn = get_conn('localhost', 'staff_{}'.format(email), password, 'flight_ticket', 'staff_role')
            conn.autocommit = False
            cursor = conn.cursor()
            query = ''
            username = email
            query = 'SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id FROM flight NATURAL JOIN airline_staff WHERE status=\'Upcoming\' AND username=\'{}\' AND datediff(departure_time, now())<=30'.format(username)
            print('query:', query)
            cursor.execute(query)
            data0 = cursor.fetchall()
            print(data0)
            query = 'SELECT booking_agent_id AS id FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN flight) NATURAL JOIN airline_staff WHERE username=\'{}\' AND booking_agent_id IS NOT NULL AND date_format((now()-INTERVAL 1 month), \'%m\')=date_format(purchase_date, \'%m\') GROUP BY booking_agent_id ORDER BY COUNT(ticket_id) DESC LIMIT 5'.format(username)
            print('query:', query)
            cursor.execute(query)
            data1 = cursor.fetchall()
            print(data1)
            data1 = [id['id'] for id in data1]
            query = 'SELECT booking_agent_id AS id FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN flight) NATURAL JOIN airline_staff WHERE username=\'{}\' AND booking_agent_id IS NOT NULL AND date_format((now()-INTERVAL 1 year), \'%Y\')=date_format(purchase_date, \'%Y\') GROUP BY booking_agent_id ORDER BY COUNT(ticket_id) DESC LIMIT 5'.format(username)
            print('query:', query)
            cursor.execute(query)
            data2 = cursor.fetchall()
            print(data2)
            data2 = [id['id'] for id in data2]
            query = 'SELECT booking_agent_id AS id FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN flight) NATURAL JOIN airline_staff WHERE username=\'{}\' AND booking_agent_id IS NOT NULL AND date_format((now()-INTERVAL 1 year), \'%Y\')=date_format(purchase_date, \'%Y\') GROUP BY booking_agent_id ORDER BY SUM(price) DESC LIMIT 5'.format(username)
            print('query:', query)
            cursor.execute(query)
            data3 = cursor.fetchall()
            print(data3)
            data3 = [id['id'] for id in data3]
            query = 'CALL staff_customer_ticket(\'{}\')'.format(username)
            print('query:', query)
            cursor.execute(query)
            data4 = cursor.fetchall()
            print(data4)
            query = 'SELECT airport_city FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN (flight JOIN airport ON(flight.arrival_airport=airport.airport_name))) NATURAL JOIN airline_staff WHERE username=\'{}\' AND period_diff(date_format(now(), \'%Y%m\'), date_format(purchase_date, \'%Y%m\'))<=3 GROUP BY airport_city ORDER BY COUNT(ticket_id) DESC LIMIT 3'.format(username)
            print('query:', query)
            cursor.execute(query)
            data5 = cursor.fetchall()
            print(data5)
            data5 = [city['airport_city'] for city in data5]
            query = 'SELECT airport_city FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN (flight JOIN airport ON(flight.arrival_airport=airport.airport_name))) NATURAL JOIN airline_staff WHERE username=\'{}\' AND date_format((now()-INTERVAL 1 year), \'%Y\')=date_format(purchase_date, \'%Y\') GROUP BY airport_city ORDER BY COUNT(ticket_id) DESC LIMIT 3'.format(username)
            print('query:', query)
            cursor.execute(query)
            data6 = cursor.fetchall()
            print(data6)
            data6 = [city['airport_city'] for city in data6]
            query = 'SELECT permission_type FROM permission WHERE username=\'{}\''.format(username)
            print('query:', query)
            cursor.execute(query)
            data = cursor.fetchall()
            print(data)
            operator, admin = 0, 0
            for line in data:
                if line['permission_type'] == 'Operator':
                    operator = 1
                if line['permission_type'] == 'Admin':
                    admin = 1
            print('operator:', operator)
            print('admin:', admin)
            query = 'SELECT airline_name FROM airline_staff WHERE username=\'{}\''.format(username)
            print('query:', query)
            cursor.execute(query)
            data = cursor.fetchone()
            print(data)
            airline_name = data.get('airline_name')
            query = 'SELECT COUNT(ticket_id) AS amount FROM (purchases NATURAL JOIN ticket) NATURAL JOIN flight WHERE date_format(purchase_date, \'%Y\')=date_format((now() - INTERVAL (1) year), \'%Y\') AND airline_name=\'{}\''.format(airline_name)
            print('query:', query)
            cursor.execute(query)
            data = cursor.fetchone()
            print(data)
            ticketsold_year = data['amount']
            query = 'SELECT COUNT(ticket_id) AS amount FROM (purchases NATURAL JOIN ticket) NATURAL JOIN flight WHERE date_format(purchase_date, \'%Y-%m\')=date_format((now() - INTERVAL (1) month), \'%Y-%m\') AND airline_name=\'{}\''.format(airline_name)
            print('query:', query)
            cursor.execute(query)
            data = cursor.fetchone()
            print(data)
            ticketsold_month = data['amount']
            cursor.close()
            conn.commit()
            conn.close()
            return render_template('staff_home.html', username=username, operator=operator, admin=admin, myflight=data0, agent_bynum_month=data1, agent_bynum_year=data2, agent_bycom_year=data3, customers=data4, destination_month=data5, destination_year=data6, ticketsold_year=ticketsold_year, ticketsold_month=ticketsold_month, airline=airline_name)
        else:
            error = 'Wrong password or wrong email!'
            cursor.close()
            conn.commit()
            conn.close()
            return render_template('login.html', error=error)
    else:
        print('Something unexpected happens')
        cursor.close()
        conn.commit()
        conn.close()
        return redirect(url_for('search'))

#Define a route for logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('search'))

app.secret_key = 'some key that you will never guess'

if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)