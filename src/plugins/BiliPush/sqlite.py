import sqlite3


# 建立数据库，dynamic 表
def init_dynamic_table(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql = '''CREATE TABLE IF NOT EXISTS `biliDynamic` (
        `up_uid` int NOT NULL PRIMARY KEY, 
        `up_name` VARCHAR(100) NOT NULL, 
        `dynamic_id_str` VARCHAR(30) NOT NULL, 
        `timestamp` int NOT NULL, 
        `orig_dynamic_id_str` VARCHAR(30));'''
    cursor.execute(sql)

    conn.commit()
    conn.close()


# 清空 dynamic 表
def empty_dynamic_table(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql = '''DELETE FROM biliDynamic;'''
    cursor.execute(sql)

    conn.commit()
    conn.close()


# 向 dynamic 表插入数据
def insert_to_dynamic_table(db_path: str, up_uid: int, up_name: str, dynamic_id_str: str,
                            timestamp: int, orig_dynamic_id_str: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if orig_dynamic_id_str is None:
        orig_dynamic_id_str = 'null'

    sql = f'''INSERT INTO biliDynamic VALUES ({up_uid}, '{up_name}', '{dynamic_id_str}', 
        {timestamp}, {orig_dynamic_id_str});'''
    cursor.execute(sql)

    conn.commit()
    conn.close()


# 查询记录的 dynamic_id_str
def get_dynamic_id_str(db_path: str, up_uid: int) -> str:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql = f'''SELECT * FROM biliDynamic WHERE up_uid = {up_uid};'''
    exec_res = cursor.execute(sql)
    dynamic_id_str = next(iter(exec_res))[2]

    conn.commit()
    conn.close()

    return dynamic_id_str


# 更新 dynamic_id_str
def update_dynamic_id_str(db_path: str, up_uid: int, dynamic_id_str: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql = f'''UPDATE biliDynamic SET dynamic_id_str = '{dynamic_id_str}' WHERE 
    up_uid = {up_uid};'''
    cursor.execute(sql)

    conn.commit()
    conn.close()
