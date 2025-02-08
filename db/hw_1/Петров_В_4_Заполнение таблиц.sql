INSERT INTO wealth_segments (name) values ('Mass Customer'), ('Affluent Customer'), ('High Net Worth');
INSERT INTO genders (name) values ('Male'), ('Female');
INSERT INTO order_statuses (name) values ('Approved'), ('Cancelled');

-- введём адрес только для трёх customers (для разнообразия для customer №4,5,6 с разными wealth_segment_id и owns_car)
INSERT INTO addresses (address, postcode, state, country, property_valuation) values
	('17979 Del Mar Point', 2448, 'New South Wales', 'Australia', 4),
	('9 Oakridge Court', 3216, 'VIC', 'Australia', 9),
	('4 Delaware Trail', 2210, 'New South Wales', 'Australia', 9);

insert into product_infos (brand, line, product_class, product_size, standart_cost) values
	('Giant Bicycles', 'Standard', 'medium', 'large', 528.43),
	('Giant Bicycles', 'Standard', 'medium', 'large', 528.48),
	('WeareA2B', 'Standard', 'medium', 'medium', 778.69);

insert into customers(id, first_name, last_name, gender_id, dob, job_title, job_industry_category, wealth_segment_id, owns_car, address_id) values
	(4, 'Talbot', null, 1, '03-10-1961', null, 'IT', 1, false, 1),
	(5, 'Sheila-kathryn', 'Calton', 2, '13-05-1977', 'Senior Editor', null, 2, true, 2),
	(6, 'Curr', 'Duckhouse', 1, '16-09-1966', null, 'Retail', 3, true, 3);

-- по транзакции на пользователя
insert into transactions(id, product_id, product_info_id, customer_id, transaction_date, online_order, order_status_id, list_price) values
	(12441, 95, 1, 4, '03-04-2017', false, 1, 569.56),
	(7692, 39, 2, 5, '14-12-2017', false, 1, 1812.75),
	(5749, 54, 3, 6, '27-10-2017', true, 1, 1807.45);