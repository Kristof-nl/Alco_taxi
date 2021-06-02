from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/beer')
def beer():
    return render_template("beer.html")


@app.route('/wine')
def wine():
    return render_template("wine.html")


if __name__ == "__main__":
    app.run(debug=True)
