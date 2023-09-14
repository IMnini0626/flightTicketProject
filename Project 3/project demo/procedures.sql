DELIMITER //
CREATE PROCEDURE customer_recent_spending(email VARCHAR(50))
BEGIN
WITH A AS(
SELECT date_format((now()- INTERVAL (cast(mysql.help_topic.help_topic_id as signed)-1) month), '%Y-%m') AS month
FROM mysql.help_topic
WHERE cast(mysql.help_topic.help_topic_id as signed) <=6
),
B AS(
SELECT date_format(purchase_date, '%Y-%m') AS month, sum(price) AS spending_bar
FROM (purchases NATURAL JOIN ticket) NATURAL JOIN flight
WHERE customer_email=email AND period_diff(date_format(now(), '%Y%m'), date_format(purchase_date, '%Y%m'))<6
GROUP BY date_format(purchase_date, '%Y-%m')
)
SELECT month, coalesce(spending_bar,0) AS spending
FROM A NATURAL LEFT OUTER JOIN B
ORDER BY month;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE customer_ranged_spending(IN email VARCHAR(50), IN from_date date, IN to_date date)
BEGIN
WITH A AS(
SELECT date_format((now()- INTERVAL (cast(mysql.help_topic.help_topic_id as signed)-1) month), '%Y-%m') AS month
FROM mysql.help_topic
WHERE date_format((now()- INTERVAL (cast(mysql.help_topic.help_topic_id as signed)-1) month), '%Y-%m')>=date_format(from_date, '%Y-%m') AND date_format((now()- INTERVAL (cast(mysql.help_topic.help_topic_id as signed)-1) month), '%Y-%m')<=date_format(to_date, '%Y-%m')
),
B AS(
SELECT date_format(purchase_date, '%Y-%m') AS month, sum(price) AS spending_bar
FROM (purchases NATURAL JOIN ticket) NATURAL JOIN flight
WHERE customer_email=email AND purchase_date>=from_date AND purchase_date<=to_date
GROUP BY date_format(purchase_date, '%Y-%m')
)
SELECT month, coalesce(spending_bar,0) AS spending
FROM A NATURAL LEFT OUTER JOIN B
ORDER BY month;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE agent_customer_ticket(IN agent_email VARCHAR(50))
BEGIN
SELECT customer_email AS name, COUNT(ticket_id) AS number_of_tickets
FROM ((booking_agent NATURAL JOIN purchases) NATURAL JOIN ticket) NATURAL JOIN flight
WHERE email = agent_email AND period_diff(date_format(now(), '%Y%m'), date_format(purchase_date, '%Y%m'))<6
GROUP BY customer_email
ORDER BY COUNT(ticket_id)
LIMIT 5;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE agent_customer_commission(IN agent_email VARCHAR(50))
BEGIN
SELECT customer_email AS name, SUM(price)*0.05 AS spending
FROM ((booking_agent NATURAL JOIN purchases) NATURAL JOIN ticket) NATURAL JOIN flight
WHERE email = agent_email AND period_diff(date_format(now(), '%Y%m'), date_format(purchase_date, '%Y%m'))<=12
GROUP BY customer_email
ORDER BY SUM(price)*0.05
LIMIT 5;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE agent_customer_ticket_ranged(IN agent_email VARCHAR(50), IN from_date date, IN to_date date)
BEGIN
SELECT customer_email AS name, COUNT(ticket_id) AS number_of_tickets
FROM ((booking_agent NATURAL JOIN purchases) NATURAL JOIN ticket) NATURAL JOIN flight
WHERE email = agent_email AND purchase_date>=from_date AND purchase_date<=to_date
GROUP BY customer_email
ORDER BY COUNT(ticket_id)
LIMIT 5;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE agent_customer_commission_ranged(IN agent_email VARCHAR(50), IN from_date date, IN to_date date)
BEGIN
SELECT customer_email AS name, SUM(price)*0.05 AS spending
FROM ((booking_agent NATURAL JOIN purchases) NATURAL JOIN ticket) NATURAL JOIN flight
WHERE email = agent_email AND purchase_date>=from_date AND purchase_date<=to_date
GROUP BY customer_email
ORDER BY SUM(price)*0.05
LIMIT 5;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE agent_ranged_commission(IN agent_email VARCHAR(50), IN from_date date, IN to_date date)
BEGIN
SELECT sum(price)*0.05 AS total_commission, avg(price)*0.05 AS avg_commission, COUNT(ticket_id) AS total_tickets
FROM ((booking_agent NATURAL JOIN purchases) NATURAL JOIN ticket) NATURAL JOIN flight
WHERE purchase_date>=from_date AND purchase_date<=to_date AND email=agent_email;
END
DELIMITER ;

DELIMITER //
CREATE PROCEDURE customer_purchase(IN airlinename VARCHAR(50), IN flightnum int(11))
BEGIN
SELECT ticket_id
FROM ticket
WHERE airline_name=airlinename AND flight_num=flightnum AND ticket_id NOT IN(
    SELECT ticket_id
    FROM purchases
    WHERE 1
);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE staff_month_revenue_direct(IN my_username VARCHAR(50))
BEGIN
SELECT SUM(price) AS revenue
FROM (purchases NATURAL JOIN ticket) NATURAL JOIN flight
WHERE date_format((now()-INTERVAL (1) month), '%Y-%m')=date_format(purchase_date, '%Y-%m') AND booking_agent_id IS NULL AND airline_name IN (
    SELECT airline_name
    FROM airline_staff
    WHERE username = my_username
);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE staff_month_revenue_indirect(IN my_username VARCHAR(50))
BEGIN
SELECT SUM(price) AS revenue
FROM (purchases NATURAL JOIN ticket) NATURAL JOIN flight
WHERE date_format((now()-INTERVAL (1) month), '%Y-%m')=date_format(purchase_date, '%Y-%m') AND booking_agent_id IS NOT NULL AND airline_name IN (
    SELECT airline_name
    FROM airline_staff
    WHERE username = my_username
);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE staff_year_revenue_direct(IN my_username VARCHAR(50))
BEGIN
SELECT SUM(price) AS revenue
FROM (purchases NATURAL JOIN ticket) NATURAL JOIN flight
WHERE date_format((now()-INTERVAL (1) year), '%Y')=date_format(purchase_date, '%Y') AND booking_agent_id IS NULL AND airline_name IN (
    SELECT airline_name
    FROM airline_staff
    WHERE username = my_username
);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE staff_ticket_stats_recent(IN my_username VARCHAR(50))
BEGIN
WITH A AS(
SELECT date_format((now() - INTERVAL (2) year + INTERVAL (cast(mysql.help_topic.help_topic_id as signed)-1) month), '%Y-%m') AS month
FROM mysql.help_topic
WHERE date_format((now() - INTERVAL (2) year + INTERVAL (cast(mysql.help_topic.help_topic_id as signed)-1) month), '%Y')=date_format((now() - INTERVAL (1) year), '%Y')
),
B AS(
SELECT date_format(purchase_date, '%Y-%m') AS month, COUNT(ticket_id) AS num_ticket_bar
FROM (purchases NATURAL JOIN ticket) NATURAL JOIN flight
WHERE date_format(purchase_date, '%Y')=date_format((now() - INTERVAL (1) year), '%Y') AND airline_name IN (
    SELECT airline_name
    FROM airline_staff
    WHERE username = my_username
)
GROUP BY date_format(purchase_date, '%Y-%m')
)
SELECT month, coalesce(num_ticket_bar,0) AS num_ticket
FROM A NATURAL LEFT OUTER JOIN B
ORDER BY month;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE staff_ticket_stats_ranged(IN my_username VARCHAR(50), IN from_date date, IN to_date date)
BEGIN
WITH A AS(
SELECT date_format((now() - INTERVAL (cast(mysql.help_topic.help_topic_id as signed)-1) month), '%Y-%m') AS month
FROM mysql.help_topic
WHERE date_format((now() - INTERVAL (cast(mysql.help_topic.help_topic_id as signed)-1) month), '%Y-%m')>=date_format(from_date, '%Y-%m') AND date_format((now() - INTERVAL (cast(mysql.help_topic.help_topic_id as signed)-1) month), '%Y-%m')<=date_format(to_date, '%Y-%m')
),
B AS(
SELECT date_format(purchase_date, '%Y-%m') AS month, COUNT(ticket_id) AS num_ticket_bar
FROM (purchases NATURAL JOIN ticket) NATURAL JOIN flight
WHERE date_format(purchase_date, '%Y-%m')>=date_format(from_date, '%Y-%m') AND date_format(purchase_date, '%Y-%m')<=date_format(to_date, '%Y-%m') AND airline_name IN (
    SELECT airline_name
    FROM airline_staff
    WHERE username = my_username
)
GROUP BY date_format(purchase_date, '%Y-%m')
)
SELECT month, coalesce(num_ticket_bar,0) AS num_ticket
FROM A NATURAL LEFT OUTER JOIN B
ORDER BY month;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE admin_check_new_flight(IN my_airline_name VARCHAR(50), IN my_airplane_id INT(11), IN my_departure_time datetime, IN my_arrival_time datetime)
BEGIN
SELECT airline_name
FROM flight
WHERE airline_name=my_airline_name AND airplane_id=my_airplane_id AND ((my_departure_time>=departure_time AND my_departure_time<=arrival_time) OR (my_arrival_time>=departure_time AND my_arrival_time<=arrival_time) OR (departure_time>=my_departure_time AND departure_time<=my_arrival_time) OR (arrival_time>=my_departure_time AND arrival_time<=my_arrival_time));
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE staff_customer_ticket(IN my_username VARCHAR(50))
BEGIN
WITH A AS (
SELECT customer_email AS email, COUNT(ticket_id) AS num_of_flights
FROM ((purchases NATURAL JOIN ticket) NATURAL JOIN flight) NATURAL JOIN airline_staff
WHERE username=my_username AND date_format((now()-INTERVAL 1 year), '%Y')=date_format(purchase_date, '%Y')
GROUP BY customer_email
)
SELECT email, name, num_of_flights
FROM A NATURAL JOIN customer
WHERE 1
ORDER BY num_of_flights DESC
LIMIT 5;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE staff_ticket_sum_ranged(IN my_username VARCHAR(50), IN from_date date, IN to_date date)
BEGIN
SELECT SUM(ticket_id) AS amount
FROM (purchases NATURAL JOIN ticket) NATURAL JOIN flight
WHERE date_format(purchase_date, '%Y-%m')>=date_format(from_date, '%Y-%m') AND date_format(purchase_date, '%Y-%m')<=date_format(to_date, '%Y-%m') AND airline_name IN (
    SELECT airline_name
    FROM airline_staff
    WHERE username = my_username
);
END //
DELIMITER ;