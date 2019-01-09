import data_manager


def sort_by_key(key='submission_time', reverse=False, database='questions'):
    if database == 'questions':
        database = data_manager.QUESTION_FILE_PATH
    else:
        database = data_manager.ANSWER_FILE_PATH
    file = data_manager.read_from_csv(database)
    file.sort(key=lambda row: row[key], reverse=True)
    return file