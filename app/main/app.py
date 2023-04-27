from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == "__main__" :
    app.run(debug=True)

app.run(host='0.0.0.0', port=81)