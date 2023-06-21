from flask import Flask

import controller.root as root
import controller.map as map


app = Flask(__name__)
app.register_blueprint(root.blueprint, url_prefix='/')
app.register_blueprint(map.blueprint, url_prefix='/map')


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == '__main__':
    app.run(port=4321, processes=1)
