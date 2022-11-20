-- find top 10 members by spending

select * from (
	select M.membership_id, rank() over (order by sum(T.total_price) desc) as spending_rank
	from carsales.transactions T
	left join carsales.member M
	on T.membership_id = M.membership_id
	group by M.membership_id
	
	) ranked
where spending_rank <=10
order by spending_rank desc
