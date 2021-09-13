import json
import datetime



class BaseAlreadyExistsError(Exception):
    pass


class DateAlreadyExistsError(Exception):
    pass


class DigitGroupAlreadyExistsError(Exception):
    pass



def load_data(fileName):

    try:
        # try reading json file

        with open(fileName, 'r') as f:
            data = json.load(f)

    except FileNotFoundError:
        # file doesnt exist, create new json

        data = {
            "bases": {} 
        }

        with open(fileName, 'w') as jf:
            jf.write(json.dumps(data, indent=4))

    return data


def add_base(base, data):

    base = str(base)

    if base in data["bases"]:
        raise BaseAlreadyExistsError
        #Todo: raise exception
    
    newBase = {
        "alltime": {
            "all": {
                "average_time": 0.0,
                "success_rate": 0,
                "rounds_played": 0,
                "total_time": 0
            },
            "addition": {
                "average_time": 0.0,
                "success_rate": 0,
                "rounds_played": 0,
                "total_time": 0
            },
            "subtraction": {
                "average_time": 0.0,
                "success_rate": 0,
                "rounds_played": 0,
                "total_time": 0
            },
            "multiplication": {
                "average_time": 0.0,
                "success_rate": 0,
                "rounds_played": 0,
                "total_time": 0
            },
            "division": {
                "average_time": 0.0,
                "success_rate": 0,
                "rounds_played": 0,
                "total_time": 0
            }
        }
    }
    data["bases"][base] = newBase
    return data


def add_date(base, data):

    base = str(base)

    if base not in data["bases"]:
        data = add_base(base, data)

    date = datetime.datetime.now().strftime("%Y-%m-%d")

    if(date in data["bases"][base]):
        raise DateAlreadyExistsError

    preset = {
        "all": {
            "average_time": 0.0,
            "success_rate": 0,
            "rounds_played": 0,
            "total_time": 0,
        },
        "addition": {
            "average_time": 0.0,
            "success_rate": 0,
            "rounds_played": 0,
            "total_time": 0,
        },
        "subtraction": {
            "average_time": 0.0,
            "success_rate": 0,
            "rounds_played": 0,
            "total_time": 0,
        },
        "multiplication": {
            "average_time": 0.0,
            "success_rate": 0,
            "rounds_played": 0,
            "total_time": 0,
        },
        "division": {
            "average_time": 0.0,
            "success_rate": 0,
            "rounds_played": 0,
            "total_time": 0,
        }
    }

    data["bases"][base][date] = preset

    return data


def add_digits(base, data, digits): # both to date and global

    base = str(base)

    keyName = "1"
    for i in range(1, digits):
        keyName += '0'
    
    keyName = keyName + '-' + keyName + '0'


    date = datetime.datetime.now().strftime("%Y-%m-%d")

    if keyName in data["bases"][base][date]["all"]:
        raise DigitGroupAlreadyExistsError


    preset = {
        "average_time": 0.0,
        "success_rate": 0,
        "rounds_played": 0,
        "total_time": 0,
        "best_time": None
    }

    # use copy so that dict keys dont reffer to the same value  
    data["bases"][base][date]["all"][keyName] = preset.copy()
    data["bases"][base][date]["addition"][keyName] = preset.copy()
    data["bases"][base][date]["subtraction"][keyName] = preset.copy()
    data["bases"][base][date]["multiplication"][keyName] = preset.copy()
    data["bases"][base][date]["division"][keyName] = preset.copy()

    if keyName not in data["bases"][base]["alltime"]["all"]:
        date = "alltime"

        data["bases"][base][date]["all"][keyName] = preset.copy()
        data["bases"][base][date]["addition"][keyName] = preset.copy()
        data["bases"][base][date]["subtraction"][keyName] = preset.copy()
        data["bases"][base][date]["multiplication"][keyName] = preset.copy()
        data["bases"][base][date]["division"][keyName] = preset.copy()

    return data

def save_data(fileName, data):

    with open(fileName, 'w') as jf:
        json.dump(data, jf, indent=4)


# fileName = "stats.json"

# data = load_data(fileName)
# data = add_date(5, data)

# if data is not None:
#     save_data(fileName, data)
    



# print(data)
