CREATE TABLE Customer_Dim (
	customer_id serial PRIMARY KEY,
	name varchar(30), 
	email varchar(100),
	phone varchar(20),
	start_date date,
	end_date date
)


CREATE TABLE Product_Dim (
	product_id serial PRIMARY KEY,
	product_name varchar(100), 
	category varchar(100),
	start_date date,
	end_date date
)


CREATE TABLE Sales_Fact (
	sale_id serial PRIMARY KEY,
	customer_id int REFERENCES Customer_Dim(customer_id), 
	product_id int REFERENCES Product_Dim(product_id),
	sale_date varchar(20),
	amount numeric(19, 2),
	quantity int
)



INSERT INTO Customer_Dim (name, email, phone, start_date, end_date)
VALUES 
('Анна', 'anna.s@email.com', '+79001112233', '2023-01-01', '9999-12-31'),
('Иван', 'ivan.v@email.com', '+79995554433', '2023-01-10', '9999-12-31'),
('Мария', 'm.kuznetsova@email.com', '+79507776655', '2023-05-20', '9999-12-31');




BEGIN;
UPDATE Customer_Dim
SET end_date = CURRENT_DATE
WHERE name IN ('Иван', 'Мария') 
  AND end_date = '9999-12-31';

INSERT INTO Customer_Dim (name, email, phone, start_date, end_date)
VALUES 
('Иван', 'ivan_new_work@email.com', '+79995554433', CURRENT_DATE, '9999-12-31'),
('Мария', 'm.kuznetsova@email.com', '+70000000000', CURRENT_DATE, '9999-12-31'),
('Алексей', 'petrov@email.com', '+79221112233', CURRENT_DATE, '9999-12-31'),
('Елена', 'sokol@email.com', '+79334445566', CURRENT_DATE, '9999-12-31');

COMMIT;



INSERT INTO Product_Dim (product_name, category, start_date, end_date)
VALUES 
('Футболка Basic White', 'Трикотаж', '2023-01-01', '9999-12-31'),
('Джинсы Straight Fit', 'Деним', '2023-01-01', '9999-12-31'),
('Куртка демисезонная', 'Верхняя одежда', '2023-09-01', '9999-12-31'),
('Худи Oversize', 'Трикотаж', '2023-10-15', '9999-12-31');




BEGIN;
UPDATE Product_Dim
SET end_date = CURRENT_DATE
WHERE product_name IN ('Джинсы Straight Fit', 'Футболка Basic White') 
  AND end_date = '9999-12-31';

INSERT INTO Product_Dim (product_name, category, start_date, end_date)
VALUES 
('Футболка Basic White', 'Трикотажное изделие', CURRENT_DATE, '9999-12-31'),
('Джинсы Straight Fit', 'Брюки', CURRENT_DATE, '9999-12-31'),
('Кепка Logo', 'Аксессуары', CURRENT_DATE, '9999-12-31'),
('Сумка', 'Аксессуары', CURRENT_DATE, '9999-12-31');

COMMIT;




INSERT INTO Sales_Fact (customer_id, product_id, sale_date, amount, quantity)
SELECT 
    c.customer_id, 
    p.product_id, 
    vals.s_date, 
    vals.s_amount, 
    vals.s_qty
FROM (
    VALUES 
        ('Анна', 'Футболка Basic White', '2023-05-15', 1500.00, 1),
        ('Иван', 'Джинсы Straight Fit', '2023-02-01', 4500.00, 1),
        ('Иван', 'Джинсы Straight Fit', CURRENT_DATE::text, 4500.00, 1),
        ('Алексей', 'Кепка Logo', CURRENT_DATE::text, 1200.00, 2),
        ('Мария', 'Сумка', CURRENT_DATE::text, 8000.00, 1)
) AS vals(c_name, p_name, s_date, s_amount, s_qty)
JOIN Customer_Dim c ON c.name = vals.c_name 
    AND vals.s_date::date BETWEEN c.start_date AND c.end_date
JOIN Product_Dim p ON p.product_name = vals.p_name 
    AND vals.s_date::date BETWEEN p.start_date AND p.end_date;





