import random
import mysql.connector
import string
from datetime import date, timedelta

# setup dos dados
nomes_alunos = ["Lucas", "Ana", "Gabriel", "Mariana", "Felipe", "Beatriz", "Pedro", "Isabela", "Rafael", "Larissa"]
nomes_professores = ["Alfredo", "Benedito", "Cândido", "Delmira", "Eustáquio"]
sobrenomes = ["Silva", "Oliveira", "Souza", "Costa", "Lima"]
data_inicial = date(2000, 1, 1)
carga_horaria = [30, 45, 60, 90]
disciplinas = ['Lógica de Programação', 'Algoritmos e Estrutura de Dados', 'POO', 'Redes de Computação']

# Funções para dados aleatórios
def random_nome_aluno():
    return random.choice(nomes_alunos) + ' ' + random.choice(sobrenomes)

def random_nome_professor():
    return random.choice(nomes_professores) + ' ' + random.choice(sobrenomes)

def random_date():
    return str(data_inicial + timedelta(days=int(random.randrange(0, 3000))))

def random_cpf():
    return str(random.randint(10000000000, 99999999999))

def random_matricula():
    return str(random.randint(0, 9999999999))

def random_endereço():
    return f"Rua {random.choice(nomes_professores)}, {random.randint(1, 100)}"

def random_text():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=30))

def random_carga_horaria():
    return random.choice(carga_horaria)

# Conexão com o banco
connection = mysql.connector.connect(user='root', password='Katrou123*', host='127.0.0.1', database='faculdade')
mycursor = connection.cursor()

# # Inserindo alunos
# sql = "INSERT INTO aluno(nome, data_nascimento, matricula, endereço) VALUES (%s, %s, %s, %s)"
# values = [(random_nome_aluno(), random_date(), random_matricula(), random_endereço()) for _ in range(50)]
# mycursor.executemany(sql, values)
# connection.commit()
# print(mycursor.rowcount, "registro(s) de aluno(s) inserido(s)")

# # Inserindo professores
# mycursor.execute('SELECT * FROM departamento')
# departamentos = mycursor.fetchall()
# if not departamentos:
#     raise ValueError("Nenhum departamento encontrado no banco de dados!")

# sql = "INSERT INTO professor(inicio_contrato, nome, cpf, depto_id) VALUES (%s, %s, %s, %s)"
# values = [(random_date(), random_nome_professor(), random_cpf(), random.choice(departamentos)[0]) for _ in range(10)]
# values = list(set(values))
# mycursor.executemany(sql, values)
# connection.commit()
# print(mycursor.rowcount, "registro(s) de professor(es) inserido(s)")

# # Inserindo disciplinas
# sql = "INSERT INTO disciplina(nome, carga_horaria, ementa) VALUES (%s, %s, %s)"
# values = [(disciplina, random_carga_horaria(), random_text()) for disciplina in disciplinas]
# values = list(set(values))
# mycursor.executemany(sql, values)
# connection.commit()
# print(mycursor.rowcount, "registro(s) de disciplina(s) inserido(s)")

# Relacionando professores e disciplinas
mycursor.execute('SELECT * FROM professor')
professores = mycursor.fetchall()
mycursor.execute('SELECT * FROM faculdade.disciplina')
disciplinas = mycursor.fetchall()

sql = "INSERT INTO professor_disciplina(cpf ,nome) VALUES (%s, %s)"
values = [(prof[0], random.choice(disciplinas)[0]) for prof in professores]
values = list(set(values))  # Remove duplicados
mycursor.executemany(sql, values)
connection.commit()
print(mycursor.rowcount, "registro(s) de professor_disciplina(s) inserido(s)")

# Relacionando alunos e disciplinas
mycursor.execute('SELECT * FROM aluno.matricula')
alunos = mycursor.fetchall()

sql = "INSERT INTO aluno_disciplina() VALUES (%s, %s)"
values = [(aluno[0], random.choice(disciplinas)[0]) for aluno in alunos]
values = list(set(values))  # Remove duplicados
mycursor.executemany(sql, values)
connection.commit()
print(mycursor.rowcount, "registro(s) de aluno_disciplina(s) inserido(s)")

connection.close()