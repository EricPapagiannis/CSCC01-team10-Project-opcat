from Planet import *
from Star import *
from System import *


class comparator():


    def __init__(obj1, obj2):
        '''(PlanetaryObject, PlanetaryObject) -> NoneTye
        sets up the comparator with two objects of PlanetaryObject
        type must match
        raises ObjectTypeMismatchException
        returns NoneType
        '''

        if (type(obj1)) == (type(obj2)):
            self.obj1 = obj1
            self.obj2 = obj2
            self.working_type = type(obj1)
        else:
            raise ObjectTypeMismatchException


    def sqlJoin(left_join):
        '''(bool) -> Dictionary
        works similar to joins in sql
        if input bool is true, a left join is performed
        if input bool is false, a right join is performed
        returns a Dictionary containing three keys,
        first with a list of field names
        the rest with lists of data values in the same order
        SQL join logic will determine what is included
        '''

        if (left_join):
            left_data = self.obj1.getData()
            right_data = self.obj2.getData()
        else:
            left_data = self.obj2.getData()
            right_data = self.obj1.getData()

        missing_keys = []
        result_dict = {'data':[], 'left':[], 'right':[]}

        for key in left_data:
            if not(key in right_data):
                missing_keys.append(key)
            result_dict['data'].append(key)

        for key in result_dict['data']:
            result_dict['left'].append(left_data[key])
            if key in missing_keys:
                result_dict['right'].append(None)
            else:
                result_dict['right'].append(right_data[key])

        return result_dict
    
    def innerJoinDiff():
        '''() -> Dictionary
        Selects fields akin to SQL inner join
        On selected fields, find differing field values
        Returns a dictionary with keys corresponding to any differing field
        values. The keys map to tuples of the values of (obj1, obj2).
        '''

        left_data = self.obj1.getData()
        right_data = self.obj2.getData()

        result_dict = {}

        for key in left_data:
            if key in right_data:
                if (left_data[key] != right_data[key]):
                    result_dict[key] = (left_data[key], right_data[key])

        return result_dict



class ObjectTypeMismatchException(Exception):
    pass
