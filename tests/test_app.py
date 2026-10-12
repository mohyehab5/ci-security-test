from app.main import add, app


def test_add():
    assert add(2, 3) == 5


def test_index():
    res = app.test_client().get("/")
    assert res.status_code == 200
    assert "message" in res.get_json()


def test_health():
    res = app.test_client().get("/health")
    assert res.get_json() == {"status": "ok"}


def test_add_route():
    res = app.test_client().get("/add/4/6")
    assert res.get_json() == {"result": 10}
