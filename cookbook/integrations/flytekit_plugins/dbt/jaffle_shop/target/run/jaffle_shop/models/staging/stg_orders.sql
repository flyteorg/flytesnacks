
  create view "jaffle_shop"."dbt_demo"."stg_orders__dbt_tmp" as (
    with source as (
    select * from "jaffle_shop"."dbt_demo"."raw_orders"

),

renamed as (

    select
        id as order_id,
        user_id as customer_id,
        order_date,
        status

    from source

)

select * from renamed
  );