WITH t1 AS (
    SELECT 
        csc.commerce_nit,
        csc.commerce_name,
        csc.commerce_email,
        csc.formatted_date,
        csc.successful_count,
        csc.unsuccessful_count,
        co.commission_cost,
        co.percentage_vat,
        d.discount_percentage,
        CASE
            WHEN csc.successful_count BETWEEN co.min_successful_requests AND co.max_successful_requests THEN 'yes'
            ELSE 'no'
        END AS marca_successful,
        CASE
            WHEN csc.unsuccessful_count BETWEEN d.min_unsuccessful_requests AND d.max_unsuccessful_requests THEN 'yes'
            ELSE 'no'
        END AS marca_unsuccessful
    FROM csc AS csc
    LEFT JOIN commissions AS co 
        ON csc.commerce_name = co.trade_name
    LEFT JOIN discounts AS d 
        ON csc.commerce_name = d.trade_name
)
SELECT 
    t1.formatted_date AS month_date,
    t1.commerce_name AS name_trade,
    t1.commerce_nit AS nit,
    (t1.commission_cost * t1.successful_count) * (
        1 - COALESCE(t1.discount_percentage, 0)
    ) AS commission_cost,
    (t1.commission_cost * t1.successful_count) * (
        1 - COALESCE(t1.discount_percentage, 0)
    ) * t1.percentage_vat AS vat_value,
    (t1.commission_cost * t1.successful_count) * (
        1 - COALESCE(t1.discount_percentage, 0)
    ) * (1 + t1.percentage_vat) AS total_value,
    t1.commerce_email AS email
FROM t1
WHERE (
        t1.discount_percentage IS NULL
        AND t1.marca_successful = 'yes'
    )
    OR (
        t1.marca_successful = 'yes'
        AND t1.marca_unsuccessful = 'yes'
    );
