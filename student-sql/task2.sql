CREATE TABLE hub_customer (
    customer_hk uuid primary key default gen_random_uuid(),
    customer_id varchar(50) not null unique,
    load_date timestamp not null default now(),
    record_source varchar(100) not null
)


CREATE TABLE hub_product (
    product_hk uuid primary key default gen_random_uuid(),
    product_id varchar(50) not null unique,
    load_date timestamp not null default now(),
    record_source varchar(100) not null
)

CREATE TABLE hub_order (
    order_hk uuid primary key default gen_random_uuid(),
    order_number varchar(50) not null unique,
    load_date timestamp not null default now(),
    record_source varchar(100) not null
)

CREATE TABLE lnk_order_customer (
    link_oc_hk uuid primary key default gen_random_uuid(),
    order_hk uuid references hub_order(order_hk),
    customer_hk uuid references hub_customer(customer_hk),
    load_date timestamp not null default now(),
    record_source varchar(100) not null
)

CREATE TABLE lnk_order_product (
    link_op_hk uuid primary key default gen_random_uuid(),
    order_hk uuid references hub_order(order_hk),
    product_hk uuid references hub_product(product_hk),
    load_date timestamp not null default now(),
    record_source varchar(100) not null
)

CREATE TABLE sat_product_info  (
    product_hk uuid references hub_product(product_hk),
    load_date timestamp not null,
    hash_diff uuid not null,
    product_name varchar(255),
    category varchar(100),
    base_price decimal(12,2),
    record_source varchar(100),
    primary key (product_hk, load_date)
)

CREATE TABLE sat_order_status (
    order_hk uuid references hub_order(order_hk),
    load_date timestamp not null,
    status_name varchar(50),
    primary key (order_hk, load_date)
)


CREATE TABLE sat_order_details (
    order_hk uuid not null,
    order_date date not null,
    load_date timestamp not null,
    total_amount decimal(12,2),
    record_source varchar(100),
    primary key (order_hk, load_date, order_date)
) partition by range (order_date)



CREATE TABLE sat_order_details_2022 partition of sat_order_details
    for values from ('2022-01-01') to ('2023-01-01');

CREATE TABLE sat_order_details_2023 partition of sat_order_details
    for values from ('2023-01-01') to ('2024-01-01');

CREATE TABLE sat_order_details_2024 partition of sat_order_details
    for values from ('2024-01-01') to ('2025-01-01');

CREATE TABLE sat_order_details_2025 partition of sat_order_details
    for values from ('2025-01-01') to ('2026-01-01');


CREATE INDEX idx_order_date on sat_order_details (order_date);


insert into sat_order_details (order_hk, order_date, load_date, total_amount, record_source)
values 
(gen_random_uuid(), '2022-07-15', now(), 1200.00, 'набор для барбекю'),
(gen_random_uuid(), '2023-05-20', now(), 1200.50, 'стейк рибай'),
(gen_random_uuid(), '2023-08-10', now(), 600.00,  'арбузы и дыни'),
(gen_random_uuid(), '2024-01-15', now(), 350.00,  'завтрак: овсянка и мед'),
(gen_random_uuid(), '2024-04-12', now(), 850.00,  'сыр пармезан'),
(gen_random_uuid(), '2024-06-30', now(), 1500.00, 'морепродукты'),
(gen_random_uuid(), '2025-03-05', now(), 500.00,  'фермерский йогурт')


select * 
from sat_order_details 
where order_date >= '2024-01-01' and order_date < '2025-01-01'
