select x.*,
(Accidents - Accident_prev)/Accidents as pct_urban_rural
from
(
select land_use_name, to_char(local_time, 'yyyy-mm'), count(consecutive_number) Accidents ,
lag(count(consecutive_number),1) over (partition by land_use_name order by to_char(local_time, 'yyyy-mm') ) Accident_prev
from crash
where local_time >= '2021-01-01' and local_time <= '2021-12-31' and land_use_name not in('Others')
group by land_use_name, to_char(local_time, 'yyyy-mm')
)x
