from flask import Flask, render_template, request, url_for, redirect
import data_manager

app = Flask(__name__)


@app.route('/')
@app.route('/list', methods=['GET', 'POST'])
def route_index():
    questions = data_manager.read_data()
    sorted_questions = data_manager.sort_messages(questions, sort_key='submission_time', reverse=False)
    header = data_manager.format_header()
    return render_template('list.html',
                           questions=sorted_questions,
                           header=header)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
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


@app.route('/add-question', methods=['GET', 'POST'])
def route_add_question():
    if request.method == 'POST':
        new_question = {
            'title': request.form.get('title'),
            'message': request.form.get('message'),
            'submission_time': data_manager.get_time(),
            'id': data_manager.generate_id(),
            'view_number': None,
            'vote_number': None,
            'image': None
        }
        data_manager.add_message(new_question)
        return redirect('/list')
    return render_template('edit_question.html')


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
