#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import urllib
import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs

__settings__ = xbmcaddon.Addon(id='service.script.integrator')
__addondir__ = xbmc.translatePath(__settings__.getAddonInfo('profile'))
if not xbmcvfs.exists(__addondir__):
    xbmcvfs.mkdir(__addondir__)

class DBWorker:
    _db_connection = None
    _db_cursor = None
    
    def __init__(self):
        self._db_connection = sqlite3.connect(__addondir__ + 'library.db')
        self._db_cursor = self._db_connection.cursor()
        self._db_cursor.execute('CREATE TABLE IF NOT EXISTS Movies (title text, year text, collection text, root text, source text, link text)')
    
    def __del__(self):
        self._db_connection.close()

    def add_movie(self, title, year, collection, root, source='', link=''):
        query = u"INSERT INTO Movies SELECT '{0}', '{1}', '{2}', '{3}', '{4}', '{5}' WHERE NOT EXISTS (SELECT 1 FROM Movies WHERE title='{0}' AND year='{1}' AND collection='{2}')".format(title.replace("'", " "), year, collection, root, source, link)
        self._db_cursor.execute(query)
        self._db_connection.commit()

    def get_movie_title_by_root(self, root):
        query = u"SELECT title, year FROM Movies WHERE root='{0}'".format(root)
        self._db_cursor.execute(query)
        result = self._db_cursor.fetchone()
        return result

    def read_movies(self, collection=None):
        query = 'SELECT * FROM Movies'
        if collection:
            query += " WHERE collection = '%s'" % collection
        movies = self._db_cursor.execute(query)
        result = []
        for movie in movies:
            result.append(movie)
        return result
    
    def get_movie_link(self, title, year, collection):
        #title = str(repr(title))
        query = u"SELECT root, link, source FROM Movies WHERE title='{0}' AND year='{1}' AND collection='{2}'".format(title, year, collection)
        #xbmc.log(query.decode('utf-8'))
        self._db_cursor.execute(query)
        result = self._db_cursor.fetchone()
        if result is not None:
            (root, link, source) = result
            return {'root': root, 'link': link, 'source': source}
        else:
            return None

    def update_link(self, title, year, collection, link, source):
        query = u"UPDATE Movies SET source='{0}', link='{1}' WHERE title='{2}' AND year='{3}' AND collection='{4}'".format(source, link, title, year, collection)
        self._db_cursor.execute(query)
        self._db_connection.commit()

if __name__ == '__main__':
    dbworker = DBWorker()