def generate_id():
    with open('uid.csv', 'r', newline='') as csvfile:
        reader = csvfile.readlines()
        if len(reader) == 0:
            new_id = str(1)
        else:
            last_id = int(reader[-1])
            new_id = str(last_id + 1)
    with open('uid.csv', 'a', newline='') as csvfile:
        csvfile.write('\n'+ new_id) # seek method could be better
    return new_id