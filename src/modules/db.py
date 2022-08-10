from pysondb import db


class database:
    def __init__(self, dbpath):
        self.Db = db.getDb(dbpath)
        

    def get(self, param=None):
        if param is None:
            data = self.Db.getAll()
        if isinstance(param, int):
            data = self.Db.get(param)
            if param == 0:
                data = self.Db.get()
        if isinstance(param, dict):
            data = self.Db.getBy(param)

        return data
            
        
    def add(self, data):
        if isinstance(data, dict):
            data = self.Db.add(data)
        if isinstance(data, list):
            data = self.Db.addMany(data)

    
    def remove_duplicates(self, setd, base_key):
        return [e for e in setd if not self.get({base_key:e[base_key]})]


    def check_by_key(self, setd, base_key, param_comp):
        return [le for le in setd if le[base_key] == param_comp]