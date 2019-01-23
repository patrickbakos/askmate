import connection
import time

question = connection.PATH_QUESTION
answer = connection.PATH_ANSWER


def get_time():



def add_message(message, file=question):
    old_messages = connection.read_from_csv(file)
    for row in old_messages:
        if row['id'] == message['id']:
            row = message
            return connection.write_to_csv(old_messages, file)
    old_messages.append(message)
    return connection.write_to_csv((old_messages, file))


def delete_message(id, file=question):
    old_messages = connection.read_from_csv(file, id)
    for row in old_messages:
        if row['id'] == id:
            old_messages.remove(row)
            return connection.write_to_csv(old_messages, file)

