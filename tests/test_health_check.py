def test_health_check(client):
    """The initial Django project responds at its root URL."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.content == b"Project Feedback is running."
