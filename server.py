from flask import Flask, render_template, request, redirect
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


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add_question.html')
    else:
        new_question = {
            'title': request.form.get('title'),
            'message': request.form.get('message')
        }

        # Generating the final dictionary for the  new question
        new_question_final = data_manager.collect_data(new_question)

        # Writing the new question to the csv
        data_manager.write_to_csv(new_question_final)

        question_id = new_question_final['id']

        return redirect('/question/<question_id>') #TODO Generating the url still doesn't work


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
