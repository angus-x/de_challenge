-- DROP DATABASE IF EXISTS sales;
-- CREATE DATABASE sales;

-- -- CREATE USER db_admin
-- -- WITH SUPERUSER PASSWORD 'db_admin';

-- -- GRANT ALL PRIVILEGES ON DATABASE sales TO db_admin;

-- -- USE sales;
CREATE SCHEMA carsales;
SET search_path TO carsales;

CREATE TABLE IF NOT EXISTS transactions
(
    id bigserial NOT NULL,
    membership_id character varying(50) NOT NULL,
    salesperson_id character varying(50) NOT NULL,
    car_id character varying(50) NOT NULL,
    quantity integer NOT NULL,
    total_price numeric(10, 2) NOT NULL,
    sales_date date NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS member
(
    membership_id character varying(50) NOT NULL,
    name character varying(100) NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    date_of_birth date NOT NULL,
    mobile_no integer NOT NULL,
    email character varying(200) NOT NULL,
    above_18 boolean NOT NULL,
    PRIMARY KEY (membership_id)
);

CREATE TABLE IF NOT EXISTS car
(
    car_id character varying(100) NOT NULL,
    item_name character varying(200) NOT NULL,
    manufacturer_name character varying(100) NOT NULL,
    cost numeric(10, 2) NOT NULL,
    weight_kg integer NOT NULL,
    valid_from date NOT NULL,
    valid_to date,
    PRIMARY KEY (car_id)
);

CREATE TABLE IF NOT EXISTS salesperson
(
    salesperson_id character varying(10) NOT NULL,
    mobile_no integer NOT NULL,
    email character varying(200) NOT NULL,
    PRIMARY KEY (salesperson_id)
);

ALTER TABLE IF EXISTS transactions
    ADD CONSTRAINT fk_member FOREIGN KEY (membership_id)
    REFERENCES member (membership_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS transactions
    ADD CONSTRAINT fk_salesperson FOREIGN KEY (salesperson_id)
    REFERENCES salesperson (salesperson_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS transactions
    ADD CONSTRAINT fk_car FOREIGN KEY (car_id)
    REFERENCES car (car_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;