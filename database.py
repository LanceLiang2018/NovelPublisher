import requests
import pymongo


class DataBase:
    def __init__(self):
        self.client = None
        self.db = None
        self.col = None
        self.connect_init()

    def connect_init(self):
        # 下面这个是哪个数据库来着？？？
        # self.client = pymongo.MongoClient("mongodb+srv://LanceLiang:1352040930database@lanceliang-lktmq.azure."
        #                                   "mongodb.net/test?retryWrites=true&w=majority")
        self.client = pymongo.MongoClient("mongodb+srv://lanceliang:1352040930database@lanceliang-9kkx3.azure."
                                          "mongodb.net/test?retryWrites=true&w=majority")
        # self.client = pymongo.MongoClient()
        self.db = self.client.novel_publisher
        self.col = self.db.novel_publisher

    def db_init(self):
        collection_names = self.db.list_collection_names()
        if 'novel_publisher' in collection_names:
            self.db.drop_collection('novel_publisher')
        if 'novel_publisher' in collection_names:
            self.db.drop_collection('novel_publisher')
        self.col = self.db.novel_publisher
        # 只有在插入一个数据之后才会建立Collection
        # print(dict(self.col.find({})))
        # self.col.insert_one({'created': True})

    def get_books(self):
        data = list(self.col.distinct('bookname'))
        return data

    def get_chapters(self, bookname=None):
        if bookname is None:
            data = list(self.col.distinct('chaptername'))
        else:
            data = list(self.col.find({'bookname': bookname}, {'bookname': 1, 'chaptername': 1, '_id': 0}))
        return data

    def publish(self, bookname: str, chaptername: str, url: str):
        data = list(self.col.find({'bookname': bookname, 'chaptername': chaptername}, {}))
        if len(data) == 0:
            self.col.insert_one({'bookname': bookname, 'chaptername': chaptername, 'url': url})
        else:
            self.col.update_one({'bookname': bookname, 'chaptername': chaptername},
                                {'$set': {'bookname': bookname, 'chaptername': chaptername, 'url': url}})

    def get_content(self, bookname: str, chaptername: str):
        data = list(self.col.find({'bookname': bookname, 'chaptername': chaptername},
                                  {'bookname': 1, 'chaptername': 1, 'url': 1, '_id': 0}))
        if len(data) == 0:
            return None
        return data[0]['url']


if __name__ == '__main__':
    _db = DataBase()
    _db.db_init()
    _db.publish('TestBook', 'TestChapter', 'https://raw.githubusercontent.com/LanceLiang2018/MyNovels/master/novels/%E7%9F%AD%E7%AF%87/%E6%97%A7%E6%A2%A6/%E6%97%A7%E6%A2%A6.md')
    print(_db.get_books())
    print(_db.get_chapters('TestBook'))
    print(_db.get_content('TestBook', 'TestChapter'))
