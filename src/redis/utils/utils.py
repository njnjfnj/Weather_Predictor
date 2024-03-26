from json import dumps

def construct_result(arr, e=''):
    if arr:
        return dumps({"result": arr, "status": "success"})
    else:
        message = str(e) if e != '' else "No matching cities found"
        return dumps({"result": arr, "status": "error", "message": message})

def construct_offsets(page, limit):
    start = (page*limit - 1) - (limit - 1)
    end_non_inclusive = page*limit
    return {"start": start, "end": end_non_inclusive}

def construct_cities_count(amount, e=''):
    if amount:
        return dumps({"result": amount, "status": "success"})
    else:
        message = e if e != '' else "No matching cities found"
        return dumps({"result": amount, "status": "error", "message": message})