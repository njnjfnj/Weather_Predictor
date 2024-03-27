import logging

from json import dumps

def construct_result(arr, e=''):
    if arr:
        return dumps({"result": arr, "status": "success"})
    else:
        message = str(e) if e != '' else "No matching cities found"
        return dumps({"result": arr, "status": "error", "message": message})

def construct_offsets(page, limit):
    if page == 0 and limit and limit > 0:
        return {"start": page, "end": limit}

    if page >= 0:
        if limit and limit > 0:
            start = (page*limit - 1) - (limit - 1)
            end_non_inclusive = page*limit
            return {"start": start, "end": end_non_inclusive}
        else:
            msg = "'limit' must an integer value > 0"
            handle_error(msg, ValueError(msg))
    else:
        msg = "'page' must an integer value >= 0"
        handle_error(msg, ValueError(msg))


def construct_cities_count(amount, e=''):
    if not isinstance(amount, int):
        raise TypeError("Argument 'amount' must be an integer")
    
    if amount:
        return dumps({"result": amount, "status": "success"})
    else:
        message = e if e != '' else "No matching cities found"
        return dumps({"result": amount, "status": "error", "message": message})
    

def handle_error(message, error):
    logging.error(message)
    raise error