import pymongo


class Handle_mongo(object):


    __data_collection_name = 'collection_xxxx_item'
    __db_name = 'db_xxxx'
    def __init__(self):
        super().__init__()
        myclient = pymongo.MongoClient('mongodb://127.0.0.1:27017')
        self.db = myclient[self.__db_name]

    @property
    def collection(self):
        return self.db[self.__data_collection_name]

    def save_item(self, item):
        if not item:
            print('item is empty')
            return
        item = dict(item)
        if (type(item) is not dict):
            print('item is not dict')
            return

        xxxxId = item['xxxxId']
        if not bookId:
            print("missing xxxxId",item)
            return
        # 根据id 去更新
        self.collection.update({'xxxxId': xxxxId}, item, True)

    def get_item(self):
        return self.collection.find({})

mongo = Handle_mongo()