import mysql.connector
import time

class WikiDB:
    def __init__(self):
        self.db = None
        self.cursor = None

    def connect(self):
        self.db = mysql.connector.Connect(host="liyiying.com", user="irgroup", password="werethebest", database="wikipagelinks")
        self.cursor = self.db.cursor()

    def get_page_id_if_redirect(self, id):
        self.cursor.execute("select rd_namespace, rd_title from redirect where rd_from=%s", (id, ))

        idx = 0
        ret = None
        for r in self.cursor:
            if idx > 0:
                print "Error: more than 1 redirect"
            else:
                ret = r

            idx += 1

        if r[0] != 0:
            return None

        ret, title = self.get_page_id_from_title(r[1])
        return ret, title

    def get_page_id_from_title(self, title):
        self.cursor.execute("select page_id, page_is_redirect from page where page_namespace=0 and page_title=%s", (title, ))

        idx = 0
        ret = None
        for r in self.cursor:
            if idx > 0:
                print "Warning: page id not unique given page title"
            else:
                ret = r

            idx += 1

        if ret[1] == 1:
            # print "redirect:", title
            ret = self.get_page_id_if_redirect(ret[0])
        else:
            ret = ret[0], title

        return ret

    def get_page_links(self, id):
        start = time.time()
        self.cursor.execute("select pl_namespace, pl_title from pagelinks where pl_from=%s", (id, ))
        titles = []
        for r in self.cursor:
            if r[0] == 0:
                titles.append(r[1])

        ret = []
        for r in titles:
            page_id, page_title = self.get_page_id_from_title(r)
            ret.append((page_id, page_title))
            # print page_id, page_title
            end = time.time()
            print "Current:", end - start

        end = time.time()
        print "Total:", end - start
        return ret

if __name__ == '__main__':
    db = WikiDB()
    db.connect()

    page_id, page_title = db.get_page_id_from_title("World_War_II")
    links = db.get_page_links(page_id)
