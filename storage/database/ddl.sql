-- public.documents definition

-- Drop table

-- DROP TABLE public.documents;

CREATE TABLE IF NOT EXISTS public.documents (
	id serial4 NOT NULL,
	docpath varchar NULL,
	uploaded_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT documents_pkey PRIMARY KEY (id)
);


-- public.extracted_charts definition

-- Drop table

-- DROP TABLE public.extracted_charts;

CREATE TABLE IF NOT EXISTS public.extracted_charts (
	id serial4 NOT NULL,
	docid int4 NULL,
	pagenumber int4 NULL,
	image bytea NULL,
	imagepath varchar NULL,
	extracted_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT extracted_charts_pkey PRIMARY KEY (id)
);


-- public.extracted_images definition

-- Drop table

-- DROP TABLE public.extracted_images;

CREATE TABLE IF NOT EXISTS public.extracted_images (
	id serial4 NOT NULL,
	docid int4 NULL,
	pagenumber int4 NULL,
	image bytea NULL,
	imagepath varchar NULL,
	caption varchar NULL,
	extracted_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT extracted_images_pkey PRIMARY KEY (id)
);


-- public.extracted_tables_json definition

-- Drop table

-- DROP TABLE public.extracted_tables_json;

CREATE TABLE IF NOT EXISTS public.extracted_tables_json (
	id serial4 NOT NULL,
	docid int4 NULL,
	pagenumber int4 NULL,
	tablejson jsonb NULL,
	extracted_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT extracted_tables_json_pkey PRIMARY KEY (id)
);


-- public.extracted_tables_raw definition

-- Drop table

-- DROP TABLE public.extracted_tables_raw;

CREATE TABLE IF NOT EXISTS public.extracted_tables_raw (
	id serial4 NOT NULL,
	docid int4 NULL,
	pagenumber int4 NULL,
	tableid int4 NULL,
	rownumber int4 NULL,
	columnname varchar(100) NULL,
	value varchar NULL,
	extracted_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT extracted_tables_raw_pkey PRIMARY KEY (id)
);


-- public.extracted_texts definition

-- Drop table

-- DROP TABLE public.extracted_texts;

CREATE TABLE IF NOT EXISTS public.extracted_texts (
	id serial4 NOT NULL,
	docid int4 NULL,
	pagenumber int4 NULL,
	ordernumber int4 NULL,
	textvalue text NOT NULL,
	extracted_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT extracted_texts_pkey PRIMARY KEY (id)
);


-- public.ner_data definition

-- Drop table

-- DROP TABLE public.ner_data;

CREATE TABLE IF NOT EXISTS public.ner_data (
	id serial4 NOT NULL,
	entityname varchar NULL,
	entitylabel varchar NULL,
	docid int4 NULL,
	pagenumber int4 NULL,
	ordernumber int4 NULL,
	startposition int4 NULL,
	endposition int4 NULL,
	extracted_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT ner_data_pkey PRIMARY KEY (id)
);