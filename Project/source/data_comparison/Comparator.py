from data_parsing.Planet import *
from data_parsing.Star import *
from data_parsing.System import *
from data_comparison.proposed_change import *


class Comparator():
    def __init__(self, obj1, obj2, origin):
        '''(PlanetaryObject, PlanetaryObject, str) -> NoneTye
        sets up the comparator with two objects of PlanetaryObject
        type of two objects must match
        str must be one of {"NASA archive", "exoplanet.eu"}

        raises ObjectTypeMismatchException is objects do not match
        returns NoneType
        '''

        if (type(obj1)) == (type(obj2)):
            self.obj1 = obj1
            self.obj2 = obj2
            self.working_type = type(obj1)
            self.origin = origin
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

        # config of whether to run left join or right join
        if (left_join):
            left_data = self.obj1.getData()
            right_data = self.obj2.getData()
        else:
            left_data = self.obj2.getData()
            right_data = self.obj1.getData()

        missing_keys = []
        # entries are linked using indices
        result_dict = {'data': [], 'left': [], 'right': []}

        # set up the list of data fields
        for key in left_data:
            if not (key in right_data):
                # fields not appearing in either data set
                missing_keys.append(key)
            if key == "":
                left_data[key] = "N/A"
                result_dict['data'].append("N/A")
            else:
                result_dict['data'].append(key)

        # generate entries of left and right based on sql join logic
        for key in result_dict['data']:
            if left_data[key] == "":
                # left missing
                left_data[key] = "N/A"
                result_dict['left'].append("N/A")
            else:
                # exists in left
                result_dict['left'].append(left_data[key])
            if key in missing_keys or key == "":
                # right missing
                result_dict['right'].append("N/A")
            else:
                # exists in right
                result_dict['right'].append(right_data[key])

        return result_dict

    def sqlJoinNewOnly(self, left_join):
        '''(bool) -> Dictionary
        Identical to method sqlJoin except excludes all rows
        which do not have a new or missing data field
        Returns dictionary structured in the same manner as sqlJoin
        '''
        raw_dict = self.sqlJoin(left_join)
        entry_count = len(raw_dict['data'])

        # remove entries not including new or missing fields
        for i in range(0, entry_count):
            if ((raw_dict['right'] == "N/A") or (raw_dict['left'] == "N/A")):
                raw_dict['data'].pop(i)
                raw_dict['left'].pop(i)
                raw_dict['right'].pop(i)
        return raw_dict

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
            # this only gets data in both sets
            if key in right_data:
                # try to numerical compare                    
                try:
                    if (float(left_data[key]) != float(right_data[key])):
                        result_dict[key] = (
                            float(left_data[key]), float(right_data[key]))
                        # otherwise just normal compare
                except ValueError:
                    if (left_data[key].lower() != right_data[key].lower()):
                        result_dict[key] = (left_data[key], right_data[key])
        return result_dict

    def proposedChangeStarCompare(self):
        '''() -> list
        Similar to starCompare but returns a list of Addition
        and Modification Objects
        '''
        # why is variable a list?
        result_dict = []

        main_dictionary = self.starCompare()

        # return list of proposed changes of the planets in star
        for planet in main_dictionary["planetDC"]:
            for field in main_dictionary["planetDC"][planet]:
                if main_dictionary["planetDC"][
                    planet][field][0] != "N/A" and main_dictionary["planetDC"][
                    planet][field][0] != "":
                    result_dict.append(
                        Modification(self.origin,
                                     self.obj2.nameToPlanet[planet],
                                     self.obj1.planetObjects[0], field,
                                     main_dictionary["planetDC"][
                                         planet][field][0],
                                     main_dictionary["planetDC"][
                                         planet][field][1])
                    )
        for field in main_dictionary["starC"]:
            if ((main_dictionary["starC"][field][0] != "N/A") and (
                        main_dictionary["starC"][field][0] != "")):
                result_dict.append(
                    Modification(self.origin,
                                 self.obj2, self.obj1, field,
                                 main_dictionary["starC"][field][0],
                                 main_dictionary["starC"][field][1]))
        for planet in main_dictionary["planetA"]:
            result_dict.append(Addition(self.origin, main_dictionary["planetA"][
                planet]))
        i = 0

        return result_dict

    def starCompare(self):
        '''() -> Dictionary
        Comparison method for only stars
        Will find differing data for both the star and any planets
        attached to the system

        Returns a dictionary of dictionaries

        Main dictionary contains:
          starC: dict of mismatched/CHANGED star data
            keys: star fields
            generated by innerJoinDiff()
          starN: dict of NEW star data
            keys: star fields
            generated by sqlJoinNewOnly(True)
          planetN: dict of NEW planets
            keys: left, right
          planetDN: dict of NEW planet data
            keys: planet names
            generated by sqlJoinNewOnly(True)
          planetDC: dict of mismatched/CHANGED planet data
            keys: planet names
            generated by innerJoinDiff()
          planetA: dict of new planets attached to the star
            keys: planet names

        Raises ObjectTypeIncompatibleException if objects are not
        stars
        '''

        if not (isinstance(self.obj1, Star)):
            # do not call this method for non-stars
            raise ObjectTypeIncompatibleException
        else:
            # starC
            starDataChange = self.innerJoinDiff()

            # starN
            starDataNew = self.sqlJoin(True)

            # planetN
            newPlanets = {}
            newPlanets["left"] = list(set(self.obj1.planetObjects) -
                                      set(self.obj2.planetObjects))

            newPlanets["right"] = list(set(self.obj2.planetObjects) -
                                       set(self.obj1.planetObjects))

            # planetDN and DC:
            newPlanetsData = {}
            planetsDataChange = {}

            # examine all planets attached to system
            planetsAddition = {}

            for planet in self.obj1.planetObjects:
                # if (planet in self.obj2.planetObjects):
                found = 0
                for planetName in self.obj2.nameToPlanet:
                    cleanName = ''.join(
                        ch for ch in planet.name if
                        ch.isalnum()).lower()
                    if (planet.name == planetName):
                        # create comparartor instance on planets
                        planetCompare = Comparator(planet,
                                                   self.obj2.nameToPlanet[
                                                       planet.name],
                                                   self.origin)
                        # get dictionary of new planet data for that planet
                        newPlanetsData[planet.name] = planetCompare.sqlJoin(
                            True)
                        # get dictionary of changed planet data for that planet
                        planetsDataChange[planet.name] = \
                            planetCompare.innerJoinDiff()
                        found = 1
                    elif (cleanName == ''.join(
                            ch for ch in planetName if
                            ch.isalnum()).lower()):
                        # create comparartor instance on planets
                        planetCompare = Comparator(planet,
                                                   self.obj2.nameToPlanet[
                                                       cleanName],
                                                   self.origin)
                        # get dictionary of new planet data for that planet
                        newPlanetsData[cleanName] = planetCompare.sqlJoin(
                            True)
                        # get dictionary of changed planet data for that planet
                        planetsDataChange[cleanName] = \
                            planetCompare.innerJoinDiff()
                        found = 1

                if found == 0:
                    planetsAddition[planet.name] = planet

            # generates output
            output_dict = {}
            output_dict["starC"] = starDataChange
            output_dict["starN"] = starDataNew
            output_dict["planetN"] = newPlanets
            output_dict["planetDN"] = newPlanetsData
            output_dict["planetDC"] = planetsDataChange
            output_dict["planetA"] = planetsAddition

            return output_dict


class ObjectTypeMismatchException(Exception):
    pass


class ObjectTypeIncompatibleException(Exception):
    pass
