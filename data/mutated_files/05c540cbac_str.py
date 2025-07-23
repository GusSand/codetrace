import settings
import psycopg2, psycopg2.extras
from core import DBUtil

class SQLDataTable():
    columns = []
    rows = []

    def __tmp5(__tmp0):
        __tmp0.columns = []
        __tmp0.rows = []

    def __tmp3(__tmp0):
        return ','.join(__tmp0.columns)

    def getValueString(__tmp0, rowIdx, anonymous=False):
        pass


class SQLTableAdapter():
    conn:object = None
    table:SQLDataTable = SQLDataTable() 

    def __tmp5(__tmp0, dbConfig:str):
        __tmp0.conn = DBUtil.getConnection(dbConfig)
        __tmp0.table

    def __getColumns(__tmp0, tableName):
        cur = __tmp0.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "SELECT column_name FROM information_schema.columns WHERE table_schema='public' and table_name = '%s'"
        cur.execute(sql,tableName)
        __tmp0.table.columns = cur.fetchall()
        cur.close()

    def __getRows(__tmp0, tableName:str):
        cur = __tmp0.conn.cursor()
        sql = "SELECT * FROM %s"
        cur.execute(sql,tableName)
        __tmp0.table.rows = cur.fetchall()
        cur.close()

    def getDataTable(__tmp0, tableName:<FILL>):
        __tmp0.table = SQLDataTable()
        __tmp0.__getColumns(tableName)
        __tmp0.__getRows(tableName)

    def __tmp1(__tmp0, dbConfig):
        if __tmp0.conn:
            __tmp0.conn.close()
        __tmp0.conn = DBUtil.getConnection(dbConfig)

    def __tmp2(__tmp0):
        if __tmp0.conn:
            __tmp0.conn.close()
        __tmp0.table = None



class DBCopier():
    SOURCE = 'source'
    DESTINATION = 'destination'
    table_list = []

    def __tmp5(__tmp0):
        __tmp0.table_list = DBUtil.getTableList(DBUtil.getConnection(__tmp0.SOURCE))
        print(len(__tmp0.table_list))

    def __tmp4(__tmp0):
        for table in __tmp0.table_list:
            pass