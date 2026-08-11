def test_rate_limit_exceeded(client, demo_key):
    for i in range(6):
        response = client.post(
            "/api/v1/sentiment/predict",
            headers=demo_key,
            json={"text": f"Test {i}"}
        )
    
    assert response.status_code == 429
    assert "Rate limit exceeded" in response.json()["detail"]