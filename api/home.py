from flask import Flask, render_template
from . import index

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.py', message=index.message)

if __name__ == '__main__':
    app.run(debug=True)
    