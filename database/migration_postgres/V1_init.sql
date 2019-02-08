create database distripp
	with owner distripp;

create table planning
(
	id serial not null
		constraint planning_pk
			primary key,
	title varchar(100) not null,
	password varchar(50) not null
);

alter table planning owner to distripp;

create table stories
(
	id serial not null
		constraint stories_pk
			primary key,
	name varchar(50) not null,
	planningid integer not null
		constraint stories_planning_id_fk
			references planning
);

alter table stories owner to distripp;

create table estimates
(
	id serial not null
		constraint estimates_pk
			primary key,
	est_user varchar(50) not null,
	estimate varchar(3),
	est_comment varchar(500),
	storyid integer not null
		constraint estimates_stories_id_fk
			references stories
);

alter table estimates owner to distripp;

