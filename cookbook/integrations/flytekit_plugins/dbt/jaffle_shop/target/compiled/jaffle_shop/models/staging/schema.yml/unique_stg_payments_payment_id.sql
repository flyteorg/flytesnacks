
    
    

select
    payment_id as unique_field,
    count(*) as n_records

from "jaffle_shop"."dbt_demo"."stg_payments"
where payment_id is not null
group by payment_id
having count(*) > 1


