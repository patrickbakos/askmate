def sort_messages(data, sort_key='title', reverse_sorting=False):
    return sorted(data, key=lambda message: message[sort_key], reverse=reverse_sorting)


