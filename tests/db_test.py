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
    
    def test_albums_table_upsert(self):
        myDB = db.DBConnection("test.db")                
        cvd = {"AlbumID": 'abcdefgh-ijkl-mnop-qrst-uv1234567890'}

        nvd = {"ArtistID":         '12345678-9abc-defg-hijk-lmnopqrstuvw',
                "ArtistName":       'TestArtistName',
                "AlbumTitle":       'TestAlbumTitle',
                "AlbumASIN":        'B12345ABCD',
                "ReleaseDate":      '2012-10-01',
                "DateAdded":        '2012-10-17',
                "Status":           'Skipped',
                "Type":             'Album',
                "ArtworkURL":None,
                "ThumbURL":None,
                "ReleaseID":        '1234abcd-ijkl-mnop-qrst-uf123456abcd',
                "ReleaseCountry":   None,
                "ReleaseFormat":    None,
                }        
        #BASIC INSERTION STAGE
        #insert the album into the empty albums table
        myDB.upsert('albums',nvd,cvd)
        #retrieve the album again
        albums = myDB.select("SELECT * FROM albums")
        #check that were only inserting a single album
        self.assertEquals(len(albums),1)
        album = albums[0]
        #check the album id
        self.assertTrue("AlbumID" in album.keys())
        self.assertTrue(album['AlbumID'] == cvd['AlbumID'])        
        #check all other keys
        for key in nvd.keys():
            self.assertTrue(key in album.keys())
            self.assertTrue(album[key] == nvd[key])

        #UPDATE STAGE
        #modify some of the album properties
        nvd["ArtistName"] = 'DifferentTestArtistName'
        nvd['AlbumTitle'] = 'DifferentTestAlbumTitle'
        nvd['Status'] = 'Wanted'

        #update the album in the database
        myDB.upsert('albums',nvd,cvd)
        #retrieve it again
        albums = myDB.select("SELECT * FROM albums")
        #make sure theres still only one album in the table
        self.assertEquals(len(albums),1)
        album = albums[0]
        #check the album id (should be the same)
        self.assertTrue("AlbumID" in album.keys())
        self.assertTrue(album['AlbumID'] == cvd['AlbumID'])        
        #check all other keys
        for key in nvd.keys():
            self.assertTrue(key in album.keys())
            self.assertTrue(album[key] == nvd[key])

        #INSERTION STAGE 2
        #modify the album id
        cvd['AlbumID'] = 'abcdefgh-qrst-ijkl-mnop-uv1234567890'
        #modify some of the album properties
        nvd['AlbumTitle'] = "ThirdTestAlbumTitle"
        nvd['AlbumASIN'] = 'BABCD51234'
        nvd['Status'] = 'Skipped'
        #insert the album into the database
        myDB.upsert('albums',nvd,cvd)
        #retrieve all albums
        albums = myDB.select("SELECT * FROM albums")
        #check that there are two albums in the table now
        self.assertEquals(len(albums),2)
        #retrieve only the album we just inserted
        albums = myDB.select("SELECT * FROM albums WHERE AlbumID=?",[cvd['AlbumID']])
        #make sure we only got one album
        self.assertEquals(len(albums),1)
        album = albums[0]
        #check the album id
        self.assertTrue("AlbumID" in album.keys())
        self.assertTrue(album['AlbumID'] == cvd['AlbumID'])        
        #check all other keys
        for key in nvd.keys():
            self.assertTrue(key in album.keys())
            self.assertTrue(album[key] == nvd[key])

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