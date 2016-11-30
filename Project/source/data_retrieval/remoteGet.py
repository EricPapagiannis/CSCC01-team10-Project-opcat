class remoteGet:
    def __init__(self, link, saveTo):
        self._link = link
        self._saveTo = saveTo

    def getFile(self):
        '''(NoneType) -> NoneType
        Retrieves file from set url to set local destination
        Raises CannotRetrieveFileException
        Returns NoneType
        '''
        import urllib
        try:
            urllib.request.urlretrieve(self._link, self._saveTo)
        except:
            raise CannotRetrieveFileException(self._link, self._saveTo)

    def isNew(self):
        '''(NoneType) -> bool
        returns true if file at remote URL is different than file located at local destination
        else returns false
        Raises CannotRetrieveFileException
        Returns bool
        '''
        import hashlib
        import urllib
        import os
        try:
            urllib.request.urlretrieve(self._link, self._saveTo + ".TMP")
        except:
            raise CannotRetrieveFileException(self._link, self._saveTo)
        hashgen = hashlib.md5()
        with open(self._saveTo + ".TMP", 'rb') as afile:
            buf = afile.read()
            hashgen.update(buf)
        csumNew = hashgen.hexdigest()
        hashgen2 = hashlib.md5()
        with open(self._saveTo, 'rb') as afile:
            buf2 = afile.read()
            hashgen2.update(buf2)
        csumOriginal = hashgen2.hexdigest()
        os.remove(self._saveTo + ".TMP")
        return not (csumNew == csumOriginal)


class CannotRetrieveFileException(Exception):
    pass
