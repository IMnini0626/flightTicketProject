from flask import Flask, render_template, request, session, url_for, redirect, jsonify
import pymysql.cursors
import random

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='flight_ticket',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route for search
@app.route('/')
def search():
    return render_template('agent_home.html', name="Yini")

# @app.route('/result', methods=['GET', 'POST'])
# def result():
#     searchText = request.form['searchText']
#     cursor = conn.cursor()
#     query = "SELECT distinct flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.status, flight.price FROM flight, airport WHERE flight.departure_airport LIKE '%%%s%%' or flight.arrival_airport LIKE '%%%s%%'or (flight.departure_airport = airport.airport_name and airport.airport_city LIKE '%%%s%%') or (flight.arrival_airport = airport.airport_name and airport.airport_city LIKE '%%%s%%')" % (searchText, searchText, searchText, searchText)
#     cursor.execute(query)
#     data = cursor.fetchall()
#     cursor.close()
#     return render_template('customer_home.html', username="Yini", search_result=data)

#for customer home
#http://www.mydatastack.com/flaskd3part1 
@app.route('/spending_data')
def spending_data():
    #从query返回值做数据处理，显示从本月开始向后倒推六个月的月份（英语简写），和每月的开销(整数，小数也可以好像)
    processed_data_example = [
        {"month":"2022-1", "spending":3000},
        {"month":"2022-2", "spending":random.random()*10000},
        {"month":"2022-3", "spending":6500},
        {"month":"2022-4", "spending":3000}
    ]
    #最上面import的时候要在flask里面多加一个jsonify不然下面这行用不了
    return jsonify(processed_data_example)

#for agent home
@app.route('/customer_data_ticket')
def customer_data_ticket():
    #从query返回值做数据处理，consumer不够五个也无所谓，也能显示的（0个好像不行）
    customer_data_ticket = [
        {"name":"Jenny", "number_of_tickets":1},
        {"name":"Thomas", "number_of_tickets":1},
        {"name":"Vox", "number_of_tickets":2},
        {"name":"Shoto", "number_of_tickets":1},
        {"name":"Ike", "number_of_tickets":4}
    ]
    return jsonify(customer_data_ticket)

@app.route('/customer_data_commission')
def customer_data_commission():
    #从query返回值做数据处理，consumer不够五个也无所谓，也能显示的（0个好像不行）
    customer_data_commission = [
        {"name":"Jenny", "spending":4000},
        {"name":"Thomas", "spending":3000},
        {"name":"Vox", "spending":6500},
        {"name":"Shoto", "spending":3000},
        {"name":"Ike", "spending":8000}
    ]
    return jsonify(customer_data_commission)



app.secret_key = 'some key that you will never guess'

if __name__ == "__main__":
	app.run('127.0.0.1', 5001, debug = True)