from flask import Flask, jsonify

app = Flask(__name__)


def add(a: int, b: int) -> int:
    return a + b


@app.get("/")
def index():
    return jsonify(message="Hello from the secure pipeline!")


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/add/<int:a>/<int:b>")
def add_route(a: int, b: int):
    return jsonify(result=add(a, b))