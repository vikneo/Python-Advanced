SELECT o.order_no, c.full_name, m.full_name FROM "order" as o
JOIN customer as c ON c.customer_id = o.customer_id
JOIN manager as m ON m.manager_id = o.manager_id
WHERE c.city <> m.city
