from flask import Flask, render_template, request, redirect, url_for
import data_manager
import util
import copy

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    sorted_messages = util.sort_by_key()
    return render_template('index.html', sorted_messages=sorted_messages)


@app.route('/question/<question_id>')
def get_question_details(question_id):
    question = data_manager.read_from_csv(id=question_id)
    title = copy.deepcopy(question["title"])
    del question["title"]

    question_header = []

    for details in question:
        formatted_header = details.replace("_", " ").capitalize()  # Style formatting of the string for proper look
        if formatted_header not in question_header:
            question_header.append(formatted_header)

    all_answers = data_manager.read_from_csv(data_manager.ANSWER_FILE_PATH)

    answers = []

    for answer in all_answers:
        if answer["question_id"] == question_id:
            answers.append(answer)

    answers_header = []

    for details in answers:
        for key in details:
            formatted_header = key.replace("_", " ").capitalize()
            if formatted_header not in answers_header:
                answers_header.append(formatted_header)
    edit_question_url = url_for('route_edit_question', question_id=question_id)
    return render_template('question_details.html',
                           question=question,
                           question_header=question_header,
                           title=title,
                           answers=answers,
                           answers_header=answers_header,
                           edit_question_url=edit_question_url)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add_question.html')
    else:
        new_question = {
            'title': request.form.get('title'),
            'message': request.form.get('message')
        }

        # Generating the final dictionary for the new question
        new_question_final = data_manager.collect_data(new_question)

        # Writing the new question to the csv
        data_manager.write_to_csv(new_question_final)

        # Generating the URL for the new question
        question_id = new_question_final['id']
        question_url = url_for('get_question_details', question_id=question_id)

        return redirect(question_url)


@app.route('/question/<question_id>/edit-question', methods=['GET', 'POST'])
def route_edit_question(question_id):
    if request.method == 'GET':
        return render_template('edit_question.html')
    else:
        question = data_manager.read_from_csv(id=question_id)
        question['title'] = request.form.get('title')
        question['message'] = request.form.get('message')
        question['submission_time'] = data_manager.get_time()
        question_url = url_for('get_question_details', question_id=question_id)
        data_manager.write_to_csv(question, is_new=False)
        return redirect(question_url)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    if request.method == 'GET':
        return render_template('answer.html')
    else:
        new_answer = {'message': request.form.get('answer')}

        # Generating the final dictionary for the  new question
        new_answer_final = data_manager.collect_data(new_answer, header=data_manager.ANSWERS_HEADER)
        new_answer_final['question_id'] = question_id
        # Writing the new question to the csv
        data_manager.write_to_csv(new_answer_final, data_manager.ANSWER_FILE_PATH)

        # Generating the URL for the new answer
        answer_url = url_for('get_question_details', question_id=question_id)

        return redirect(answer_url)


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    # Reading all data from question.csv to a list of dictionaries
    question_reader = data_manager.read_from_csv()

    # Deleting the question's dict from the list
    for row in question_reader:
        if row['id'] == question_id:
            question_reader.remove(row)

    # Writing back the list to the csv
    data_manager.overwrite_old_csv(question_reader)

    # Deleting the answers given to that question
    answer_ids = data_manager.find_answer_id(question_id)
    for id in answer_ids:
        delete_answer(id)

    return redirect('/')


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    # Reading all data from answer.csv to a list of dictionaries
    answer_reader = data_manager.read_from_csv(file=data_manager.ANSWER_FILE_PATH)

    # Deleting the answer's dict from the list
    for row in answer_reader:
        if row['id'] == answer_id:
            answer_reader.remove(row)
            question_id = row['question_id']

    # Writing back the list to the csv
    data_manager.overwrite_old_csv(answer_reader, file=data_manager.ANSWER_FILE_PATH)

    question_url = url_for('get_question_details', question_id=question_id)
    return redirect(question_url)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
