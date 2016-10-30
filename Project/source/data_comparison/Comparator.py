from data_parsing.Planet import *
from data_parsing.Star import *
from data_parsing.System import *


class Comparator():
    def __init__(self, obj1, obj2):
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

    def sqlJoin(self, left_join):
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
        result_dict = {'data': [], 'left': [], 'right': []}

        for key in left_data:
            if not (key in right_data):
                missing_keys.append(key)
            result_dict['data'].append(key)

        for key in result_dict['data']:
            result_dict['left'].append(left_data[key])
            if key in missing_keys:
                result_dict['right'].append(None)
            else:
                result_dict['right'].append(right_data[key])

        return result_dict

    def innerJoinDiff(self):
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

if __name__ == "__main__":
    import data_parsing.XML_data_parser as XML
    import data_parsing.CSV_data_parser as CSV

    EXO_planets = CSV.buildListPlanets("exoplanetEU_csv",
                                       ["mass", "radius", "period",
                                        "semimajoraxis"], "eu")
    a = XML.buildSystemFromXML()
    planets = a[5]
    for planet in EXO_planets:
        if planet.data["namePlanet"] == "11 Com b":
            b = planet
    b.data["mass"] = 20
    print(b)
    p = planets["11 Com b"]
    print(p)
    c = Comparator(b, p)
    d = c.sqlJoin(True)
    print(d)
