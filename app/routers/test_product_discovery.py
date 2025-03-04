# tests/test_product_discovery.py
def test_discover_products_serpapi():
    response = client.get("/products/discover")
    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert len(data["products"]) == 10
    assert all("product" in p and "price" in p for p in data["products"])