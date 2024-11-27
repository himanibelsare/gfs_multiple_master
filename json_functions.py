import json
import threading
data_lock = threading.Lock()

# add to json/modify existing values
def update_json(data_update, file_path):
    flag = 1
    with data_lock:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            keys = list(data_update.keys())
            if keys[0] in data:
                flag = 2

            data.update(data_update)

            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            with open(file_path, 'w') as file:
                json.dump(data_update, file, indent=4)
    return flag

# returns value corresponding to given key
def read_from_json(key, file_path):
    flag = 2
    record = None
    with data_lock:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            if key in data:
                flag = 1
                record = data[key]
        except FileNotFoundError:
            flag = 0
    return [flag, record]

# delete from json and return popped value
def remove_from_json(key, file_path):
    flag = 1
    value = None
    with data_lock:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            if key not in data:
                flag = 2
            else:
                value = data.pop(key)
            
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            flag = 0
    return [flag, value]
