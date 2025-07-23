import psycopg2
import settings

class DBUtil():

    @staticmethod
    def getConnection(__tmp4:<FILL>, test:bool=False):
        
        connString = DBUtil.getConnString(__tmp4)
        try:
            __tmp5 = psycopg2.connect(connString)
            print(f"Connection Successful to the database {__tmp4}!")
            if not test:
                return __tmp5
        except ConnectionError:
            print(f"Connection Error! Please check the configuration of '{__tmp4}'")


    @staticmethod
    def getConnString(__tmp4) :
        config = settings.DATABASES.get(__tmp4)
        if config == None:
            raise SystemError(f"Cannot find config for '{__tmp4}") 
        return f"host={config.get('host')} port={config.get('port')} dbname={config.get('db')} user={config.get('user')} password={config.get('password')}"

    @staticmethod
    def __tmp2(__tmp5):
        cur = __tmp5.cursor()
        sql = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' order by 1 asc"
        cur.execute(sql)
        return cur.fetchall()      

    @staticmethod
    def __tmp0(__tmp3, __tmp1) :
        __tmp5 = DBUtil.getConnection(__tmp1)
        cur = __tmp5.cursor
        sql = "SELECT 1 FROM information_schema.tables WHERE table_schema='public' and table_name='%s'"
        cur.execute(sql,__tmp3)
        res = cur.fetchall()
        cur.close()
        __tmp5.close()
        return len(res) > 0
    