class PlanetaryObject:
    def __init__(self, name=None):
        self.data = dict()
        self.name = self._fixStr(name)
        if name is None:
            pass
        else:
            self.data["name" + self.__class__.__name__] = None
            self.data[name] = None

    def __str__(self):
        '''
        Builds up and returns a human-readable representation of 
        PlanetaryObject, including all the keys and corresponding data values;
        If references to other planetary objects are present, they are ignored.
        '''
        list_objects = ["Planet", "Star", "System", "PlanetaryObject"]
        s = ""
        s += "Object type : "
        s += self.__class__.__name__
        s += "\n"
        s += "Name: "
        s += self.name
        s += "\n"
        for key in self.data.keys():
            s += str(key)
            s += " :   "
            if self.data[key].__class__.__name__ in list_objects:
                s += "Points to an instance of class "
                s += self.data[key].__class__.__name__
            elif str(self.data[key]) == "":
                s += 'N/A'
            else:
                s += str(self.data[key])
            s += "\n"
        s += "\n"
        return s

    def addVal(self, name, val):
        '''(str, Object) -> None
        Adds a key value pair to the database in the planetary object
        '''
        if isinstance(name, str):
            name = self._fixStr(name)

        if isinstance(val, PlanetaryObject):
            self.data[name] = val
        elif isinstance(val, str):
            self.data[name] = self._fixStr(val)
        else:
            val = self._fixVal(val)
            self.data[name] = val

    def addValList(self, name, val):
        '''(str, Object) -> None
        Similiar to addVal, except the value in this case is made into
        a list first, if it's not already a list, then stored in the 
        database
        '''
        if isinstance(name, str):
            name = self._fixStr(name)

        if isinstance(val, list):
            self.data[name] = val
        elif isinstance(val, str):
            self.data[name] = [self._fixStr(val)]
        else:
            val = self._fixVal(val)
            self.data[name] = [val]
        return self

    def addToValList(self, name, val):
        '''(str, Object) -> None
        adds a new object to a key value pair, with a key assumption
        being the value in the key value pair is a list. It's appended to the
        end of that last.
        '''
        if isinstance(name, str):
            name = self._fixStr(name)
        if isinstance(val, str):
            val = self._fixStr(val)
        else:
            val = self._fixVal(val)
        self.data[name] += [val]
        return self

    def getData(self):
        '''() -> Dict of Objects
        Returns all the data kept in the planetary object as a dictionary
        '''
        return self.data

    def getName(self):
        '''() -> String
        returns the object's name
        '''
        return self.name

    def getVal(self, name):
        '''(Str) -> Object
        Given a key, returns the object kept at that key, 
        assuming the key exists
        '''
        return self.data[name]

    def _fixVal(self, val):
        temp = None
        if (val != ''):
            try:
                temp = float(val)
            except ValueError:
                temp = val
            except TypeError:
                temp = "N/A"
        else:
            temp = "N/A"
        return temp

    def _fixStr(self, val):
        """ (str) -> str
        Given a str, clean it and return it
        """
        if isinstance(val, str):
            return val.replace("\"", "").strip()
        else:
            return val
