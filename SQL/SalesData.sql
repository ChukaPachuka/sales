create table receipts (
    id serial primary key,
    doc_id varchar(50),
    item varchar(255),
    category varchar(100),
    amount int,
    price numeric(10,2),
    discount numeric(10,2),
    created_at timestamp default current_timestamp
);
