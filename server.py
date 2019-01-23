from flask import Flask, render_template, request, url_for, redirect
import connection
import util

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_index():
    questions = connection.read_from_csv()
    sorted_questions = util.sort_messages(questions, sort_key='submission_time')
    return render_template('list.html',
                           questions=sorted_questions)


@app.route('/question/<question_id>')
def route_question(question_id):
    question = connection.read_from_csv(id=question_id)
    answers = connection.read_from_csv(file=connection.PATH_ANSWER, id=question_id, id_key='question_id')
    return render_template('question.html',
                           question=question,
                           answers=answers)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
