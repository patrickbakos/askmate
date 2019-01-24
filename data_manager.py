import connection
import util
import time

question = connection.PATH_QUESTION
answer = connection.PATH_ANSWER
answer_header = connection.HEADER_ANSWER
question_header = connection.HEADER_QUESTION


def add_message(message, file=question):
    old_messages = connection.read_from_csv(file=file)
    old_messages.append(message)
    connection.write_to_csv(old_messages, file=file)


def delete_message(id, file=question):
    old_messages = connection.read_from_csv(file, id)
    for row in old_messages:
        if row['id'] == id:
            old_messages.remove(row)
            return connection.write_to_csv(old_messages, file)


def read_data(file=question, id=None, id_key='id'):
    if file == question:
        header = question_header
    else:
        header = answer_header
    data = connection.read_from_csv(file=file, id=id, id_key=id_key)
    if data is []:
        data.append(dict.fromkeys(header))
    return data


def sort_messages(data, sort_key='submission_time', reverse_sorting=False):
    return util.sort_messages(data=data, sort_key=sort_key, reverse_sorting=reverse_sorting)


def format_header(header=question_header):
    formatted_header = []
    for elem in header:
        formatted_elem = elem.capitalize().replace('_', ' ')
        formatted_header.append(formatted_elem)
    return formatted_header


def generate_id(file=question):
    messages = connection.read_from_csv(file)
    max_id = 0
    for row in messages:
        if int(row['id']) > max_id:
            max_id = int(row['id'])
    new_id = str(max_id + 1)
    return new_id


def get_time():
    return time.time()


'''new_question = {
            'title': 'cuna',
            'message': 'beszarsz cuna',
            'submission_time': get_time(),
            'id': generate_id(),
            'view_number': None,
            'vote_number': None,
            'image': None
            }'''
