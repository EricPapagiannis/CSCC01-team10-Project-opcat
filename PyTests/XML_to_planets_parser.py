import xml.etree.ElementTree as ET, urllib.request, gzip, io

url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
oec = ET.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.request.urlopen(url).read())))


class System:
    def __init__(self):
        self.data = dict();

    def __str__(self):
        out = "";
        for i in self.data:
            out += (i + ":");
            out += str(self.data[i]);
            out += " ";
        return out;

    class Builder:
        def __init__(self, name):
            self._data = {"nameSystem": name};

        def addVal(self, name, val):
            val = self._fixVal(val);
            self._data[name] = val;
            return self;

        def addValList(self, name, val):
            if isinstance(val, list):
                self._data[name] = val
            else:
                val = self._fixVal(val)
                self._data[name] = [val]
            return self

        def addToValList(self, name, val):
            val = self._fixVal(val)
            self._data[name] += [val]
            return self

        def getData(self):
            return self._data

        def getVal(self, name):
            return self._data[name]

        def compile(self):
            system = System();
            system.data = self._data;
            return system;

        def _fixVal(self, val):
            temp = None;
            if (val != ''):
                try:
                    temp = float(val);
                except ValueError:
                    temp = val;
                except TypeError:
                    temp = "N/A";
            else:
                temp = "N/A";
            return temp;


class Star:
    def __init__(self):
        self.data = dict();

    def __str__(self):
        out = "";
        for i in self.data:
            out += (i + ":");
            out += str(self.data[i]);
            out += " ";
        return out;

    class Builder:
        def __init__(self, name):
            self._data = {"nameStar": name};

        def addVal(self, name, val):
            val = self._fixVal(val);
            self._data[name] = val;
            return self;

        def addValList(self, name, val):
            if isinstance(val, list):
                self._data[name] = val
            else:
                val = self._fixVal(val)
                self._data[name] = [val]
            return self

        def addToValList(self, name, val):
            val = self._fixVal(val)
            self._data[name] += [val]
            return self

        def getData(self):
            return self._data

        def getVal(self, name):
            return self._data[name]

        def compile(self):
            star = Star();
            star.data = self._data;
            return star;

        def _fixVal(self, val):
            temp = None;
            if (val != ''):
                try:
                    temp = float(val);
                except ValueError:
                    temp = val;
                except TypeError:
                    temp = "N/A";
            else:
                temp = "N/A";
            return temp;


class Planet:
    def __init__(self):
        self.data = dict();

    def __str__(self):
        out = "";
        for i in self.data:
            out += (i + ":");
            out += str(self.data[i]);
            out += " ";
        return out;

    class Builder:
        def __init__(self, name):
            self._data = {"namePlanet": name};

        def addVal(self, name, val):
            val = self._fixVal(val);
            self._data[name] = val;
            return self;

        def addValList(self, name, val):
            if isinstance(val, list):
                self._data[name] = val
            else:
                val = self._fixVal(val)
                self._data[name] = [val]
            return self

        def addToValList(self, name, val):
            val = self._fixVal(val)
            self._data[name] += [val]
            return self

        def getData(self):
            return self._data

        def getVal(self, name):
            return self._data[name]

        def compile(self):
            planet = Planet();
            planet.data = self._data;
            return planet;

        def _fixVal(self, val):
            temp = None;
            if (val != ''):
                try:
                    temp = float(val);
                except ValueError:
                    temp = val;
                except TypeError:
                    temp = "N/A";
            else:
                temp = "N/A";
            return temp;


def buildSystemFromXML():
    for system in oec.findall(".//system"):
        i = 0
        for child in system.findall(".//name"):
            if child.tag == "name":
                if i == 0:
                    systemName = child.text
                    systemBuilder = System.Builder(systemName)
                elif i == 1:
                    systemBuilder.addValList("otherNamesSystem", child.text)
                else:
                    systemBuilder.addToValList("otherNamesSystem", child.text)
                i += 1
            else:
                systemBuilder.addToValList("otherNamesSystem", child.text)

        for child in system:
            if (child.tag.lower() != "star") and (child.tag.lower() != "name"):
                systemBuilder.addVal(child.tag, child.text)

        for star in system.findall(".//star"):
            ii = 0
            for child in star.findall(".//name"):
                if child.tag == "name":
                    if ii == 0:
                        starBuilder = Star.Builder(child.text)
                        systemBuilder.addValList("stars", child.text)
                    elif ii == 1:
                        starBuilder.addValList("otherNamesStar", child.text)
                    else:
                        starBuilder.addToValList("otherNamesStar", child.text)
                    ii += 1
                else:
                    starBuilder.addToValList("otherNamesStar", child.text)

            for child in star:
                if (child.tag.lower() != "planet") and (child.tag.lower() != "name"):
                    starBuilder.addVal(child.tag, child.text)

            for planet in star.findall(".//planet"):
                iii = 0
                for child in planet.findall(".//name"):
                    if child.tag == "name":
                        if iii == 0:
                            planetBuilder = Planet.Builder(child.text)
                            starBuilder.addValList("planets", child.text)
                        elif iii == 1:
                            planetBuilder.addValList("otherNamesPlanet", child.text)
                        else:
                            planetBuilder.addToValList("otherNamesPlanet", child.text)
                        iii += 1
                    else:
                        planetBuilder.addToValList("otherNamesPlanet", child.text)

                for child in planet:
                    if (child.tag.lower() != "name"):
                        planetBuilder.addVal(child.tag, child.text)

                planetBuilder.addVal("nameSystem", systemBuilder.getVal("nameSystem"))
                systemData = systemBuilder.getData()
                if "otherNamesSystem" in systemData:
                    planetBuilder.addValList("otherNamesSystem", systemData["otherNamesSystem"])

                planetBuilder.addVal("nameStar", starBuilder.getVal("nameStar"))
                starData = starBuilder.getData()

                if "otherNamesStar" in starData:
                    planetBuilder.addValList("otherNamesStar", starData["otherNamesStar"])
                planet = planetBuilder.compile()
                print("PLANET: ", planet)
            starBuilder.addVal("nameSystem", systemBuilder.getVal("nameSystem"))
            starBuilder.addValList("otherNamesSystem", systemBuilder.getVal("otherNamesSystem"))
            star = starBuilder.compile()
            print("STAR: ", star)
        system = systemBuilder.compile()
        print("SYSTEM: ", system)
        print('\n\n')


# buildPlanetFromXML()
buildSystemFromXML()
