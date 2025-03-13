SELECT DISTINCT maker FROM product
INNER JOIN pc ON pc.model = product.model
WHERE pc.speed >= 450