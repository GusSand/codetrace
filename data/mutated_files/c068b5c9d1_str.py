import settings
import psycopg2, psycopg2.extras
from core import DBUtil

class SQLDataTable():
    columns = []
    rows = []

    def __tmp8(__tmp1):
        __tmp1.columns = []
        __tmp1.rows = []

    def __tmp7(__tmp1):
        return ','.join(__tmp1.columns)

    def __tmp5(__tmp1, rowIdx, anonymous=False):
        pass


class SQLTableAdapter():
    conn:object = None
    table:SQLDataTable = SQLDataTable() 

    def __tmp8(__tmp1, __tmp0:<FILL>):
        __tmp1.conn = DBUtil.getConnection(__tmp0)
        __tmp1.table

    def __getColumns(__tmp1, __tmp2):
        cur = __tmp1.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "SELECT column_name FROM information_schema.columns WHERE table_schema='public' and table_name = '%s'"
        cur.execute(sql,__tmp2)
        __tmp1.table.columns = cur.fetchall()
        cur.close()

    def __getRows(__tmp1, __tmp2:str):
        cur = __tmp1.conn.cursor()
        sql = "SELECT * FROM %s"
        cur.execute(sql,__tmp2)
        __tmp1.table.rows = cur.fetchall()
        cur.close()

    def __tmp9(__tmp1, __tmp2):
        __tmp1.table = SQLDataTable()
        __tmp1.__getColumns(__tmp2)
        __tmp1.__getRows(__tmp2)

    def __tmp3(__tmp1, __tmp0):
        if __tmp1.conn:
            __tmp1.conn.close()
        __tmp1.conn = DBUtil.getConnection(__tmp0)

    def __tmp4(__tmp1):
        if __tmp1.conn:
            __tmp1.conn.close()
        __tmp1.table = None



class __typ0():
    SOURCE = 'source'
    DESTINATION = 'destination'
    table_list = []

    def __tmp8(__tmp1):
        __tmp1.table_list = DBUtil.getTableList(DBUtil.getConnection(__tmp1.SOURCE))
        print(len(__tmp1.table_list))

    def __tmp6(__tmp1):
        for table in __tmp1.table_list:
            pass