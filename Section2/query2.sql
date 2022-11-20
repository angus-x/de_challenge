
-- find top 3 items by sales quantity

select * from (
	select C.item_name, rank() over (order by sum(T.quantity) desc) as quantity_rank
	from carsales.transactions T
	left join carsales.car C
	on T.car_id = C.car_id
	group by C.car_id
	
	) ranked
where quantity_rank <=3
order by quantity_rank desc