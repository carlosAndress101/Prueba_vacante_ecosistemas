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
    t1.formatted_date AS Fecha_Mes,
    t1.commerce_name AS Nombre,
    t1.commerce_nit AS Nit,
    (t1.commission_cost * t1.successful_count) * (
        1 - COALESCE(t1.discount_percentage, 0)
    ) AS Valor_comision,
    (t1.commission_cost * t1.successful_count) * (
        1 - COALESCE(t1.discount_percentage, 0)
    ) * t1.percentage_vat AS Valor_iva,
    (t1.commission_cost * t1.successful_count) * (
        1 - COALESCE(t1.discount_percentage, 0)
    ) * (1 + t1.percentage_vat) AS Valor_Total,
    t1.commerce_email AS Correo
FROM t1
WHERE (
        t1.discount_percentage IS NULL
        AND t1.marca_successful = 'yes'
    )
    OR (
        t1.marca_successful = 'yes'
        AND t1.marca_unsuccessful = 'yes'
    );
