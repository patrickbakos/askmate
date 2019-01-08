from flask import Flask, render_template
import data_manager
import util

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    questions = []
    messages = data_manager.read_from_csv()
    sorted_messages = util.sort_by_key()
    return render_template('index.html',
                           messages=messages,
                           sorted_messages=sorted_messages)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
