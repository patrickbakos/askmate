import csv
import os

PATH_ANSWER = 'sample_data/answer.csv'
PATH_QUESTION = 'sample_data/question.csv'
HEADER_ANSWER = ('id', 'submission_time', 'vote_number', 'message', 'image')
HEADER_QUESTION = ('id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image')


def read_from_csv(file=PATH_QUESTION, id=None, id_key='id'):
    lines = []
    with open(file) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            data = dict(row)
            if id is None or id == data[id_key]:
                lines.append(data)
    if len(lines) > 1:
        return lines
    else:
        return lines[0]


def write_to_csv(data, file=PATH_QUESTION):
    if file == PATH_QUESTION:
        header = HEADER_QUESTION
    else:
        header = HEADER_ANSWER
    with open(file, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()
    for row in data:
        writer.writerow(row)
