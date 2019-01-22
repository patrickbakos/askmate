from flask import Flask, render_template, request, url_for, redirect
import connection

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def route_index():
    messages = connection.read_from_csv()
    return render_template('index.html',
                           messages=messages)


@app.route('/question/<question_id>')
def route_question(question_id):
    question = connection.read_from_csv(id=question_id)
    return render_template('question.html',
                           question=question)



if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
