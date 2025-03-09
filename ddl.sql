create table documents (
	id serial primary key,
	docpath varchar,
	uploaded_at timestamp default current_timestamp
)

create table extracted_texts (
    id serial primary key,
    docpath varchar,
    pagenumber integer,
    ordernumber integer,
    textvalue text not null,
    extracted_at timestamp default current_timestamp
);

create table extracted_tables_json (
    id serial primary key,
    docpath varchar,
    pagenumber integer,
    tablejson jsonb,
    extracted_at timestamp default current_timestamp
);

create table extracted_tables_raw (
    id serial primary key,
    docpath varchar,
    pagenumber integer,
    tablenumber integer,
    rownumber integer,
    columnname varchar(100),
    value varchar,
    extracted_at timestamp default current_timestamp
);

create table extracted_images (
    id serial primary key,
    docpath varchar,
    image bytea,
    imagepath varchar,
    extracted_at timestamp default current_timestamp
);

create table extracted_charts (
    id serial primary key,
    docpath varchar,
    pagenumber integer,
    image bytea,
    imagepath varchar,
    extracted_at timestamp default current_timestamp
);

create table ner_data (
	id serial primary key,
	entityname varchar,
	entitylabel varchar,
	docid integer,
	pagenumber integer,
	ordernumber integer,
	startposition integer,
	endposition integer,
	extracted_at timestamp default current_timestamp
)