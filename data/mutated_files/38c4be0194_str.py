import settings
import psycopg2, psycopg2.extras
from core import DBUtil

class __typ2():
    columns = []
    rows = []

    def __init__(__tmp0):
        __tmp0.columns = []
        __tmp0.rows = []

    def getColString(__tmp0):
        return ','.join(__tmp0.columns)

    def getValueString(__tmp0, rowIdx, anonymous=False):
        pass


class __typ0():
    conn:object = None
    table:__typ2 = __typ2() 

    def __init__(__tmp0, dbConfig):
        __tmp0.conn = DBUtil.getConnection(dbConfig)
        __tmp0.table

    def __getColumns(__tmp0, __tmp1:<FILL>):
        cur = __tmp0.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "SELECT column_name FROM information_schema.columns WHERE table_schema='public' and table_name = '%s'"
        cur.execute(sql,__tmp1)
        __tmp0.table.columns = cur.fetchall()
        cur.close()

    def __getRows(__tmp0, __tmp1:str):
        cur = __tmp0.conn.cursor()
        sql = "SELECT * FROM %s"
        cur.execute(sql,__tmp1)
        __tmp0.table.rows = cur.fetchall()
        cur.close()

    def getDataTable(__tmp0, __tmp1:str):
        __tmp0.table = __typ2()
        __tmp0.__getColumns(__tmp1)
        __tmp0.__getRows(__tmp1)

    def changeConnection(__tmp0, dbConfig):
        if __tmp0.conn:
            __tmp0.conn.close()
        __tmp0.conn = DBUtil.getConnection(dbConfig)

    def clean(__tmp0):
        if __tmp0.conn:
            __tmp0.conn.close()
        __tmp0.table = None



class __typ1():
    SOURCE = 'source'
    DESTINATION = 'destination'
    table_list = []

    def __init__(__tmp0):
        __tmp0.table_list = DBUtil.getTableList(DBUtil.getConnection(__tmp0.SOURCE))
        print(len(__tmp0.table_list))

    def copyToDestination(__tmp0):
        for table in __tmp0.table_list:
            pass