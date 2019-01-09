from flask import Flask, render_template
import data_manager
import util

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    sorted_messages = util.sort_by_key()
    return render_template('index.html', sorted_messages=sorted_messages)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
