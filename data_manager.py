import connection
import util

question = connection.PATH_QUESTION
answer = connection.PATH_ANSWER
answer_header = connection.HEADER_ANSWER
question_header = connection.HEADER_QUESTION


def add_message(message, file=question):
    old_messages = connection.read_from_csv(file)
    for row in old_messages:
        if row['id'] == message['id']:
            message = row
            return connection.write_to_csv(old_messages, file)
    old_messages.append(message)
    return connection.write_to_csv((old_messages, file))


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


def sort_messages(data, sort_key='submission_time', reverse=False):
    return util.sort_messages(data=data, sort_key=sort_key, reverse=reverse)


