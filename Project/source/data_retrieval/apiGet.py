import requests


class apiGet():
    def __init__(self, baseURL, saveTo):
        self.baseURL = baseURL
        self.saveTo = saveTo

    def getFromAPI(self, parameters):
        '''(String) -> NoneType
        Retrieves using GET with specified paramters
        Saves to file specified self.saveTo
        Returns NoneType
        '''
        fullURL = self.baseURL + parameters
        try:
            res = requests.get(fullURL)
        except:
            raise CannotRetrieveDataException(fullURL)
        if (res.ok):
            output = res.text
        else:
            raise CannotRetrieveDataException(fullURL)
        try:
            outFile = open(self.saveTo, "w")
            outFile.write(output)
            outFile.close()
        except:
            raise CannotSaveFileException(self.saveTo)

    def getTextFromAPI(self, parameters):
        '''(String) -> String
        Retrieves using GET with specified paramters
        Returns .csv file as a string
        '''
        fullURL = self.baseURL + parameters
        try:
            res = requests.get(fullURL)
        except:
            raise CannotRetrieveDataException(fullURL)
        if (res.ok):
            output = res.text
            return output
        else:
            raise CannotRetrieveDataException(fullURL)


class CannotRetrieveDataException(Exception):
    pass


class CannotSaveFileException(Exception):
    pass
