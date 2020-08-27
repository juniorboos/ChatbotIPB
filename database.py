import sqlite3

conn = sqlite3.connect('tutorial.db')
c = conn.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS docente(login TEXT, nome TEXT, email TEXT, emp_num REAL)")

def data_entry():
    c.execute("INSERT INTO docente VALUES('juniorboos', 'Milton Boos Junior','junior_boos@live.com',6)")
    c.execute("INSERT INTO docente VALUES('lrmen14', 'Lucas Ribeiro Mendes','lrmen14@gmail.com',2)")
    conn.commit()
    c.close()
    conn.close()
    
# create_table()
# data_entry()

def read_from_db():
    name = 'Milton Boos Junior'
    # sql_select_query = """ SELECT login FROM docente WHERE nome = ?"""
    # c.execute(sql_select_query, (name,))
    # c.execute('SELECT login FROM docente WHERE nome = "Milton Boos Junior"')
    c.execute('SELECT login FROM docente WHERE nome = ?', (name,))
    data = c.fetchone()
    print(data[0])
    for row in data:
        print(row)
    
read_from_db()
c.close
conn.close()