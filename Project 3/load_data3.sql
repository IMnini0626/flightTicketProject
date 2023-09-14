INSERT INTO `flight` (`airline_name`, `flight_num`, `departure_airport`, `departure_time`, `arrival_airport`, `arrival_time`, `price`, `status`, `airplane_id`) VALUES
('Jet Blue', 076, 'La Guardia', '2022-11-20 07:50:00', 'Hongqiao', '2022-11-20 21:50:00', '350', 'Upcoming', 2),
('Jet Blue', 027, 'O\'Hare', '2022-01-20 14:00:00', 'Pudong', '2022-01-01 14:00:00', '420', 'Upcoming', 1),
('Jet Blue', 057, 'JFK', '2022-12-10 20:50:00', 'Pudong', '2022-12-11 02:00:00', '700', 'Upcoming', 3),
('Jet Blue', 049, 'Hongqiao', '2023-03-24 08:00:00', 'Louisville SDF', '2023-03-24 21:00:00', '880', 'Upcoming', 1),
('Jet Blue', 085, 'La Guardia', '2018-09-01 04:00:00', 'Hongqiao', '2018-09-01 10:00:00', '550', 'Delayed', 3);

INSERT INTO `ticket` (`ticket_id`, `airline_name`, `flight_num`) VALUES
(311, 'Jet Blue', 076),
(312, 'Jet Blue', 076),
(313, 'Jet Blue', 076),
(314, 'Jet Blue', 076),
(315, 'Jet Blue', 076),
(316, 'Jet Blue', 076),
(317, 'Jet Blue', 076),
(318, 'Jet Blue', 027),
(319, 'Jet Blue', 027),
(320, 'Jet Blue', 027),
(321, 'Jet Blue', 027),
(322, 'Jet Blue', 027),
(323, 'Jet Blue', 027),
(324, 'Jet Blue', 027),
(325, 'Jet Blue', 057),
(326, 'Jet Blue', 057),
(327, 'Jet Blue', 057),
(328, 'Jet Blue', 057),
(329, 'Jet Blue', 057),
(330, 'Jet Blue', 057),
(331, 'Jet Blue', 057),
(332, 'Jet Blue', 057),
(333, 'Jet Blue', 057),
(334, 'Jet Blue', 049),
(335, 'Jet Blue', 049),
(336, 'Jet Blue', 049),
(337, 'Jet Blue', 049),
(338, 'Jet Blue', 049),
(339, 'Jet Blue', 049);


INSERT INTO `purchases` (`ticket_id`, `customer_email`, `booking_agent_id`, `purchase_date`) VALUES
(311, 'Customer@nyu.edu', 3, '2022-3-28'),
(312, 'Customer@nyu.edu', 2, '2020-4-27'),
(313, 'yangxiaocheng1112@gmail.com', 3, '2020-4-17'),
(314, 'two@nyu.edu', 4, '2022-3-17'),
(315, 'xy2128@nyu.edu', NULL, '2022-1-24'),
(316, 'Customer@nyu.edu', 2, '2021-4-14'),
(317, 'yxc_yxc@yeah.net', 3, '2021-4-18'),
(318, 'Customer@nyu.edu', 4, '2021-4-25'),
(319, 'one@nyu.edu', 4, '2022-4-26'),
(320, 'yangxiaocheng1112@gmail.com', 1, '2022-4-21'),
(321, 'two@nyu.edu', NULL, '2022-4-29'),
(322, 'yxc_yxc@yeah.net', 2, '2021-4-29'),
(323, 'yxc_yxc@yeah.net', 3, '2022-4-15'),
(324, 'xy2128@nyu.edu', 1, '2019-4-22'),
(325, 'Customer@nyu.edu', 3, '2019-4-16'),
(326, 'Customer@nyu.edu', 3, '2022-4-22'),
(327, 'Customer@nyu.edu', 4, '2022-4-11'),
(328, 'yangxiaocheng1112@gmail.com', 3, '2022-4-25'),
(329, 'yxc_yxc@yeah.net', NULL, '2020-4-18'),
(330, 'yangxiaocheng1112@gmail.com', 3, '2022-4-21'),
(331, 'yangxiaocheng1112@gmail.com', 2, '2022-4-29'),
(332, 'one@nyu.edu', 1, '2022-3-29'),
(333, 'one@nyu.edu', 4, '2022-2-22'),
(334, 'one@nyu.edu', 2, '2022-4-14'),
(335, 'Customer@nyu.edu', 3, '2022-1-23'),
(336, 'yxc_yxc@yeah.net', 4, '2022-4-17'),
(337, 'yangxiaocheng1112@gmail.com', 3, '2022-4-23'),
(338, 'Customer@nyu.edu', 2, '2022-4-10'),
(339, 'xy2128@nyu.edu', 2, '2022-4-22');

