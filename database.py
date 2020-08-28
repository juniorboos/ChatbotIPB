import sqlite3

conn = sqlite3.connect('tutorial.db')
c = conn.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS periodo(id REAL, nome TEXT, descricao TEXT, cod_escola REAL, ano_lect REAL, semestre REAL, inicio TEXT, fim TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS sala(id REAL, cod_escola REAL, cod_sala REAL, nome TEXT, abrev TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS aula(id REAL, id_periodo REAL, id_sala REAL, activo TEXT, inicio TEXT, fim TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS aula_docente(id_aula REAL, login TEXT)")

def data_entry():
    # c.execute("INSERT INTO docente VALUES('juniorboos', 'Milton Boos Junior','junior_boos@live.com',6)")
    # c.execute("INSERT INTO docente VALUES('lrmen14', 'Lucas Ribeiro Mendes','lrmen14@gmail.com',2)")
    c.execute("INSERT INTO periodo VALUES(1, 'Período 1 SI', 'Primeiro período de Sistemas de Informação', 1, 2020, 2, '2020-09-27', '2020-12-25')")
    c.execute("INSERT INTO sala VALUES(1, 1, 1435, 'Laboratório de Computação Avançada', 'LCA')")
    c.execute("INSERT INTO sala VALUES(2, 1, 1534, 'Laboratório de Robótica', 'LR')")
    c.execute("INSERT INTO aula VALUES(1, 4, 1, 'active', 'Friday 6PM', 'Friday 10PM')")
    c.execute("INSERT INTO aula VALUES(2, 4, 2, 'inactive', 'Monday 6PM', 'Monday 10PM')")
    c.execute("INSERT INTO aula_docente VALUES(1, 'juniorboos')")
    c.execute("INSERT INTO aula_docente VALUES(2, 'juniorboos')")
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
    c.execute('SELECT id_aula FROM aula_docente WHERE login = ?', (data[0],))
    data = c.fetchone()
    print(data[0])
    c.execute('SELECT id_sala, inicio, fim FROM aula WHERE id = ?', (data[0],))
    dataAula = c.fetchone()
    c.execute('SELECT nome FROM sala WHERE id = ?', (dataAula[0],))
    dataSala = c.fetchone()
    res = 'Your class starts at ' + dataAula[1] + ' in the classroom ' + dataSala[0]
    print(res)

read_from_db()
c.close
conn.close()