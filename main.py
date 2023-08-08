import os
from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")


@app.route("/")
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
