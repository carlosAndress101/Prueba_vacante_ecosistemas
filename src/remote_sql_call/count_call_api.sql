SELECT 
    c.commerce_id,
    c.commerce_nit,
    c.commerce_name,
    c.commerce_email,
    strftime('%Y%m', ac.date_api_call) AS formatted_date,
    SUM(CASE WHEN ac.ask_status = 'Successful' THEN 1 ELSE 0 END) AS successful_count,
    SUM(CASE WHEN ac.ask_status = 'Unsuccessful' THEN 1 ELSE 0 END) AS unsuccessful_count
FROM commerce AS c
LEFT JOIN apicall AS ac 
    ON c.commerce_id = ac.commerce_id
WHERE ac.date_api_call BETWEEN '{date_init}' AND '{date_end}' AND c.commerce_status = '{trade_status}'
GROUP BY c.commerce_id, strftime('%Y%m', ac.date_api_call);
