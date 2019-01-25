from flask import Flask, render_template, request, url_for, redirect
import data_manager

app = Flask(__name__)


@app.route('/')
@app.route('/list', methods=['GET', 'POST'])
def route_index():
    reverse_dict = {
        'Ascending': False,
        'Descending': True
    }
    if request.args.get('sort_key') is None:
        sort_key = 'submission_time'
        sort_reverse = False
    else:
        sort_key = request.args.get('sort_key')
        sort_reverse = request.args.get('reverse')
        if sort_reverse == "False":
            sort_reverse = False
        else:
            sort_reverse = True

    questions = data_manager.read_data()
    sorted_questions = data_manager.sort_messages(questions, sort_key=sort_key, reverse_sorting=sort_reverse)
    header = data_manager.question_header
    formatted_header = data_manager.format_header(header)
    return render_template('list.html',
                           questions=sorted_questions,
                           header=header,
                           formatted_header=formatted_header,
                           reverse_dict=reverse_dict
                           )


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def route_question(question_id):
    question = data_manager.read_data(id=question_id)
    print(question[0]['id'])
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
    return render_template('edit_question.html',
                           title_field='',
                           message_field='',
                           specific_url=url_for('route_add_question')
                           )


@app.route('/edit-question/<question_id>', methods=['GET', 'POST'])
def route_edit_question(question_id):
    question = data_manager.read_data(id=question_id)
    if request.method == 'POST':
        question = {
            'id': question[0]['id'],
            'title': request.form.get('title'),
            'message': request.form.get('message'),
            'submission_time': data_manager.get_time(),
            'vote_number': question[0]['vote_number'],
            'image': question[0]['image'],
            'view_number': question[0]['view_number']
        }
        data_manager.edit_message(question)
        return redirect(url_for('route_question', question_id=question_id))

    return render_template('edit_question.html',
                           title_field=question[0]['title'],
                           message_field=question[0]['message'],
                           specific_url=url_for('route_edit_question', question_id=question_id)
                           )


@app.route('/delete-question/<question_id>')
def route_delete_question(question_id):
    data_manager.delete_message(id=question_id, file=data_manager.question)
    data_manager.delete_message(id=question_id, id_key='question_id', file=data_manager.answer)
    return redirect(url_for('route_index'))


@app.route('/answer/<answer_id>')
def route_answer(answer_id):
    question_id = data_manager.get_question_id(answer_id)
    question = data_manager.read_data(file=data_manager.question, id=question_id)
    answer = data_manager.read_data(file=data_manager.answer, id=answer_id)
    url_delete = url_for('route_delete_answer', answer_id=answer_id)
    return render_template('answer.html',
                           answer_id=answer_id,
                           answer_header=data_manager.answer_header,
                           answer=answer,
                           question_header=data_manager.question_header,
                           question=question,
                           url_delete=url_delete
                           )


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def route_add_answer(question_id):
    if request.method == 'POST':
        new_answer = {
            'id': data_manager.generate_id(file=data_manager.answer),
            'submission_time': data_manager.get_time(),
            'vote_number': None,
            'question_id': question_id,
            'message': request.form.get('message'),
            'image': None
        }
        data_manager.add_message(new_answer, file=data_manager.answer)
        return redirect(url_for('route_answer', answer_id=new_answer['id']))
    return render_template('edit_answer.html',
                           question_id=question_id)


@app.route('/answer/<answer_id>/delete')
def route_delete_answer(answer_id):
    question_id = data_manager.get_question_id(answer_id)
    data_manager.delete_message(id=answer_id, file=data_manager.answer)
    return redirect(url_for('route_question', question_id=question_id))


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
