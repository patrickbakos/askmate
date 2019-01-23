def sort_messages(data, sort_key='title', reverse=False):
    return sorted(data, key=lambda message: message[sort_key])


