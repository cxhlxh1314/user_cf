from flask import Flask, jsonify
from flask_docs import ApiDoc


app = Flask(__name__)


ApiDoc(
    app,
    title="Sample App",
    version="1.0.0",
    description="A simple app API",
)

@api.route("/add_data", methods=["POST"])
def add_data():
    """Add some data

    ### args
    |  args | required | request type | type |  remarks |
    |-------|----------|--------------|------|----------|
    | title |  true    |    body      | str  | blog title    |
    | name  |  true    |    body      | str  | person's name |

    ### request
    ```json
    {"title": "xxx", "name": "xxx"}
    ```

    ### return
    ```json
    {"code": xxxx, "msg": "xxx", "data": null}
    ```
    """
    return jsonify({"api": "add data"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

    app.register_blueprint(api, url_prefix="/api")
