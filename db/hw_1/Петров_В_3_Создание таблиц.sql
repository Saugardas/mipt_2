-- сначала справочники, чтобы было куда ссылаться в дальнейшем
create table wealth_segments (
	id serial primary key,
	name varchar not null
);

create table genders (
	id serial primary key,
	name varchar not null
);

create table order_statuses (
	id serial primary key,
	name varchar not null
);

create table addresses (
	id serial primary key,
	address text not null,
	postcode integer not null,
	state varchar(15) not null,
	country varchar(15) not null,
	property_valuation integer not null
);

-- не соотвествует product_id, тк при одном product_id в данных есть разные наборы product_infos
create table product_infos (
	id serial primary key,
	brand varchar(15) not null,
	line varchar(15) not null,
	product_class varchar(15) not null,
	product_size varchar(15) not null,
	standart_cost decimal(10, 2) not null
);

-- customers со ссылками на genders/wealth_segments/addresses
create table customers (
	id serial primary key,
	first_name varchar(25) not null,
	last_name varchar(25), -- в данных есть пропуски
	gender_id integer references genders,
	dob date,
	job_title varchar(25),
	job_industry_category varchar(15),
	wealth_segment_id integer references wealth_segments,
	owns_car boolean not null,
	address_id integer references addresses
);

-- transactions со ссылками на products/order_statuses/customers
create table transactions (
	id serial primary key,
	product_id integer,
	product_info_id integer references product_infos,
	customer_id integer references customers,
	transaction_date date not null,
	online_order boolean not null,
	order_status_id integer references order_statuses,
	list_price decimal(10,2) not null
);
