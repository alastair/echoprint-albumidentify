import util
import logging
from util import attrdict

class Result(attrdict):
    def __init__(self, result_type, result_dict):
        self.type = result_type
        assert(isinstance(result_dict,dict))
        self.__dict__.update(result_dict)
    
    def __repr__(self):
        return "<Result - %s>" % (self.type)
    
    def __str__(self):
        return "<Result - %s>" % (self.type)

def make_results(result_type, response, accessor_function):
    try:
        data = accessor_function(response)
        if isinstance(data, list):
            return [Result(result_type, item) for item in data]
        elif isinstance(data, dict):
            return Result(result_type, data)
        else:
             return data
    except IndexError:
        logging.info("No songs found")

