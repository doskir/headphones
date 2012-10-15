import unittest
import os
import headphones
from headphones import db
class DBTests(unittest.TestCase):
    def setUp(self):
        headphones.DATA_DIR = os.curdir
        dbpath = os.path.join(headphones.DATA_DIR,"test.db")
        if os.path.exists(dbpath):
            os.remove(dbpath)
        headphones.db.setup_db(dbpath)

    def test_artists_table_insert(self):
        myDB = db.DBConnection("test.db")
        columns = ['12345678-9abc-defg-hijk-lmnopqrstuvw','TestArtistName','TestArtistSortName','2012-10-16','Active',0,'TestAlbum','2012-10-16','abcdefgh-ijkl-mnop-qrst-uf1234567890',0,999,'2012-10-16 01:25:45',None,None,None]
        query = "INSERT INTO artists VALUES (%s)" % self.list_to_sql(columns)
        #insert the test artist into the empty artists table
        myDB.action(query)
        #retrieve the artist back from the artists table
        artists = myDB.select("SELECT * FROM artists")
        self.assertEquals(len(artists),1)
        #check that were getting the original data back
        artistList = [column for column in artists[0]]
        self.assertListEqual(artistList,columns)


    def list_to_sql(self,list):
        s = ""
        for value in list:
            if len(s) > 0:
                s += ","
            if isinstance(value,str):
                s += "'%s'" % str(value)
            elif isinstance(value,int):
                s += str(value)
            elif value == None:
                s += "NULL"            
        return s

if __name__ == '__main__':
    unittest.main()