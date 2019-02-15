create table planning
(
	id serial not null
		constraint planning_pkey
			primary key,
	title text not null,
	password text not null
);

alter table planning owner to distripp;

create table story
(
	id serial not null
		constraint story_pkey
			primary key,
	planning integer not null
		constraint fk_story__planning
			references planning
				on delete cascade,
	name text not null
);

alter table story owner to distripp;

create index idx_story__planning
	on story (planning);

create table estimate
(
	id serial not null
		constraint estimate_pkey
			primary key,
	story integer not null
		constraint fk_estimate__story
			references story
				on delete cascade,
	est_user text not null,
	estimate text not null,
	est_comment text not null
);

alter table estimate owner to distripp;

create index idx_estimate__story
	on estimate (story);



