import csv
import os


ANSWERS_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
QUESTIONS_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_FILE_PATH = 'sample_data/answer.csv'
QUESTION_FILE_PATH = 'sample_data/question.csv'


def read_from_csv(file=QUESTION_FILE_PATH, id=None):
    list_of_data = []
    with open(file) as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            data = dict(row)
            if id is not None and row['id'] == id:
                return data
            list_of_data.append(data)
        return list_of_data


def write_to_csv(message, file=QUESTION_FILE_PATH, is_new=True):
    old_message = read_from_csv(file)
    if file == QUESTION_FILE_PATH:
        header = QUESTIONS_HEADER
    else:
        header = ANSWERS_HEADER

    with open(file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()

        for row in old_message:
            if message['id'] == row['id']:
                row = message
            writer.writerow(row)
        if is_new:
            writer.writerow(message)








