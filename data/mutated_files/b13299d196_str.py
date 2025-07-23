from typing import TypeAlias
__typ0 : TypeAlias = "bool"
import psycopg2
import settings

class DBUtil():

    @staticmethod
    def getConnection(__tmp2, test:__typ0=False):
        
        connString = DBUtil.getConnString(__tmp2)
        try:
            conn = psycopg2.connect(connString)
            print(f"Connection Successful to the database {__tmp2}!")
            if not test:
                return conn
        except ConnectionError:
            print(f"Connection Error! Please check the configuration of '{__tmp2}'")


    @staticmethod
    def getConnString(__tmp2:str) :
        config = settings.DATABASES.get(__tmp2)
        if config == None:
            raise SystemError(f"Cannot find config for '{__tmp2}") 
        return f"host={config.get('host')} port={config.get('port')} dbname={config.get('db')} user={config.get('user')} password={config.get('password')}"

    @staticmethod
    def __tmp1(conn):
        cur = conn.cursor()
        sql = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' order by 1 asc"
        cur.execute(sql)
        return cur.fetchall()      

    @staticmethod
    def __tmp0(__tmp3:<FILL>, dbConfig) :
        conn = DBUtil.getConnection(dbConfig)
        cur = conn.cursor
        sql = "SELECT 1 FROM information_schema.tables WHERE table_schema='public' and table_name='%s'"
        cur.execute(sql,__tmp3)
        res = cur.fetchall()
        cur.close()
        conn.close()
        return len(res) > 0
    