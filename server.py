from flask import Flask, render_template, request, url_for, redirect
import connection

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def route_index():
    messages = connection.read_from_csv()
    return render_template('index.html',
                           messages=messages)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
