    SELECT full_name FROM customer
    LEFT JOIN "order" as o ON o.customer_id = customer.customer_id
    WHERE o.customer_id is NULL
    ORDER BY full_name
    