import mysql.connector
import random

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySQL0104",
    database="inazumadb",
    consume_results=True
)

cursor = conexion.cursor()

def asignar_grupos():
    cursor.execute("SELECT * FROM team WHERE participa = 1")
    participantes = cursor.fetchall()

    groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    for g in groups:
        for i in range(4):
            team = random.choice(participantes)
            cursor.execute("UPDATE team SET idgroup = '" + g + "' WHERE idteam = " + str(team[0]))
            participantes.remove(team)

    conexion.commit()

def crearPartidosFaseGrupos():
    cursor.execute("DELETE FROM inazumadb.match")

    groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    for g in groups:
        cursor.execute("SELECT * FROM team WHERE idgroup = '" + g + "'")
        members = cursor.fetchall()

        partidos = [[members[0][0], members[1][0]],
                    [members[2][0], members[3][0]],
                    [members[0][0], members[3][0]],
                    [members[1][0], members[2][0]],
                    [members[1][0], members[3][0]],
                    [members[0][0], members[2][0]]]

        for p in partidos:
            cursor.execute("INSERT INTO inazumadb.match (idteam1, idteam2) VALUES (" + str(p[0]) + ", " + str(p[1]) + ")")

    conexion.commit()

def crearPartidosFaseFinal():
    cursor.execute("DELETE FROM inazumadb.match")

    groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    members = []

    for g in groups:
        cursor.execute("SELECT idteam FROM team WHERE idgroup = '" + g + "' order by points")
        resultados = cursor.fetchmany(2)
        members.append([resultados[0][0], resultados[1][0]])
    
    print(members)

    partidos = []
    for i in range(4):
        partidos.append([members[i*2][0], members[i*2+1][1]])
        partidos.append([members[i*2][1], members[i*2+1][0]])

    print(partidos)

    conexion.commit()

asignar_grupos()
crearPartidosFaseGrupos()
