
DATALAYER = None

def getDataLayer():
    global DATALAYER
    if DATALAYER == None:
        DATALAYER = DataLayer()
    return DATALAYER

class DataCache:
    def __init__(self):
        self.id = DataLayer._indx
        DataLayer._indx = DataLayer._indx + 1
        self.data: list[dict] = [{}]

    def getKeys(self):
        return self.data.keys()
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, DataCache):
            return self.id == __value.id
        return False

class DataLayer:
    _indx = 0

    def __init__(self):
        self.cacheStore = []

    def getCache(self, id):
        if id < len(self.cacheStore) and id >= 0:
            return self.cacheStore[id]
        return None
    
    def createCache(self, data=[{}]):
        cache = DataCache()
        cache.data = data
        self.cacheStore.append(cache)
        return cache.id