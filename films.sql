-- table creation
create table top_films (
	id serial primary key,
	title varchar(255),
	year int4
)

-- clean data
select 
	title, left("year", 4)::integer, rated, 
	case split_part(runtime, ' ', 1) runtime, 
	genre, director, actors, plot, country, awards, poster, imdbrating::float, 
	replace(imdbvotes, ',', '')::integer imdbvotes, 
	replace(right(boxoffice, -1), ',', '')::integer boxoffice 
from films_data 

-- replace N/A by nulls - dynamic query 
do 
$$
declare 
	col_name text;
begin 
	for col_name in 
		select column_name from information_schema.columns
		where table_name = 'films_data'
		and table_schema = 'public'
		and data_type != 'jsonb'
	loop 
		execute format('update films_data set %I = null where %I = %L', col_name, col_name, 'N/A');
	end loop;
end
$$;
