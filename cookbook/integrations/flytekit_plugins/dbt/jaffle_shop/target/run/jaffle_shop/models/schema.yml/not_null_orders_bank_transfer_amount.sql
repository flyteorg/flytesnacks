select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select bank_transfer_amount
from "jaffle_shop"."dbt_demo"."orders"
where bank_transfer_amount is null



      
    ) dbt_internal_test