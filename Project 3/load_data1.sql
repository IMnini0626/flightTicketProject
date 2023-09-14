INSERT INTO `flight` (`airline_name`, `flight_num`, `departure_airport`, `departure_time`, `arrival_airport`, `arrival_time`, `price`, `status`, `airplane_id`) VALUES
('Jet Blue', 976, 'La Guardia', '2018-11-20 07:50:00', 'O\'Hare', '2018-11-20 21:50:00', '350', 'Upcoming', 2),
('Jet Blue', 927, 'O\'Hare', '2019-01-20 14:00:00', 'JFK', '2019-01-01 14:00:00', '420', 'Upcoming', 1),
('Jet Blue', 457, 'JFK', '2018-12-10 20:50:00', 'O\'Hare', '2018-12-11 02:00:00', '700', 'Upcoming', 3),
('Jet Blue', 149, 'SFO', '2019-03-24 08:00:00', 'Louisville SDF', '2018-03-24 21:00:00', '880', 'Upcoming', 1),
('Jet Blue', 485, 'La Guardia', '2018-09-01 04:00:00', 'JFK', '2018-09-01 10:00:00', '550', 'Delayed', 3);

INSERT INTO `ticket` (`ticket_id`, `airline_name`, `flight_num`) VALUES
(11, 'Jet Blue', 485),
(12, 'Jet Blue', 139),
(13, 'Jet Blue', 927),
(14, 'Jet Blue', 915),
(15, 'Jet Blue', 457),
(16, 'Jet Blue', 976),
(17, 'Jet Blue', 139),
(18, 'Jet Blue', 927),
(19, 'Jet Blue', 915),
(20, 'Jet Blue', 927),
(21, 'Jet Blue', 485),
(22, 'Jet Blue', 457),
(23, 'Jet Blue', 927),
(24, 'Jet Blue', 915),
(25, 'Jet Blue', 139),
(26, 'Jet Blue', 296),
(27, 'Jet Blue', 485),
(28, 'Jet Blue', 485),
(29, 'Jet Blue', 915),
(30, 'Jet Blue', 455),
(31, 'Jet Blue', 455),
(32, 'Jet Blue', 915),
(33, 'Jet Blue', 296),
(34, 'Jet Blue', 485),
(35, 'Jet Blue', 927),
(36, 'Jet Blue', 139),
(37, 'Jet Blue', 457),
(38, 'Jet Blue', 457),
(39, 'Jet Blue', 455);


INSERT INTO `purchases` (`ticket_id`, `customer_email`, `booking_agent_id`, `purchase_date`) VALUES
(10, 'yangxiaocheng1112@gmail.com', 1, '2022-4-23'),
(11, 'Customer@nyu.edu', 3, '2022-4-28'),
(12, 'Customer@nyu.edu', 2, '2022-4-27'),
(13, 'yangxiaocheng1112@gmail.com', 3, '2022-4-17'),
(14, 'two@nyu.edu', 4, '2022-4-17'),
(15, 'xy2128@nyu.edu', NULL, '2022-4-24'),
(16, 'Customer@nyu.edu', 2, '2021-4-14'),
(17, 'yxc_yxc@yeah.net', 3, '2021-4-18'),
(18, 'Customer@nyu.edu', 4, '2021-4-25'),
(19, 'one@nyu.edu', 4, '2022-4-26'),
(20, 'yangxiaocheng1112@gmail.com', 1, '2022-4-21'),
(21, 'two@nyu.edu', NULL, '2022-4-29'),
(22, 'yxc_yxc@yeah.net', 2, '2021-4-29'),
(23, 'yxc_yxc@yeah.net', 3, '2022-4-15'),
(24, 'xy2128@nyu.edu', 1, '2019-4-22'),
(25, 'Customer@nyu.edu', 3, '2019-4-16'),
(26, 'Customer@nyu.edu', 3, '2022-4-22'),
(27, 'Customer@nyu.edu', 4, '2022-4-11'),
(28, 'yangxiaocheng1112@gmail.com', 3, '2022-4-25'),
(29, 'yxc_yxc@yeah.net', NULL, '2020-4-18'),
(30, 'yangxiaocheng1112@gmail.com', 3, '2022-4-21'),
(31, 'yangxiaocheng1112@gmail.com', 2, '2022-4-29'),
(32, 'one@nyu.edu', 1, '2022-3-29'),
(33, 'one@nyu.edu', 4, '2022-2-22'),
(34, 'one@nyu.edu', 2, '2022-4-14'),
(35, 'Customer@nyu.edu', 3, '2022-1-23'),
(36, 'yxc_yxc@yeah.net', 4, '2022-4-17'),
(37, 'yangxiaocheng1112@gmail.com', 3, '2022-4-23'),
(38, 'Customer@nyu.edu', 2, '2022-4-10'),
(39, 'xy2128@nyu.edu', 2, '2022-4-22');

