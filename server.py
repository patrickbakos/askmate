from flask import Flask, render_template, request, url_for, redirect
import data_manager

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_index():
    questions = data_manager.read_data()
    sorted_questions = data_manager.sort_messages(questions, sort_key='submission_time', reverse=False)
    header = data_manager.format_header()
    return render_template('list.html',
                           questions=sorted_questions,
                           header=header)


@app.route('/question/<question_id>')
def route_question(question_id):
    question = data_manager.read_data(id=question_id)
    answers = data_manager.read_data(file=data_manager.answer, id=question_id, id_key='question_id')
    question_header = data_manager.format_header()
    answer_header = data_manager.format_header(data_manager.answer_header)
    return render_template('question.html',
                           question=question,
                           answers=answers,
                           question_header=question_header,
                           answer_header=answer_header)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
