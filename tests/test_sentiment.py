def test_predict_without_api_key(client):
    response = client.post("/api/v1/sentiment/predict", json={"text": "I love this!"})
    assert response.status_code == 403

def test_predict_with_api_key(client, premium_key):
    response = client.post(
        "/api/v1/sentiment/predict",
        headers=premium_key,
        json={"text": "I love this product!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "positive"
    assert data["confidence"] > 0.5
    assert data["language"] == "en"

def test_predict_arabic(client, premium_key):
    response = client.post(
        "/api/v1/sentiment/predict",
        headers=premium_key,
        json={"text": "هذا المنتج رائع"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "ar"

def test_predict_batch(client, premium_key):
    response = client.post(
        "/api/v1/sentiment/predict/batch",
        headers=premium_key,
        json={"texts": ["I love this!", "This is bad"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 2