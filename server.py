from flask import Flask,jsonify, render_template, request, json, redirect,session
import psycopg2
from flask_cors import CORS 

##app = Flask(__name__)


#app = Flask(__name__)
#################################
app = Flask(__name__, static_folder='./FrontEnd/dist', template_folder='./FrontEnd/dist')
#CORS(app)
cors=CORS(app,resources={r"/back/*":{"origins":"*"}})
#################################
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def dender_vue(path):
    return render_template("index.html")
###########################################################

@app.route("/back")
def main():
    return 'Servidor Iniciado'
## Datos de mi conexión
db_name = "biblioteca"
db_user = "postgres"
db_password = "postgres"
db_host = "localhost"
db_port = "5432"
#End Point Listar Usuario
#End Point Validar Usuarios
@app.route('/back/validar-login', methods=['POST'])
def validar_login():
    try:
        data = request.json
        connection  = psycopg2.connect(database=db_name, user=db_user, password=db_password,host=db_host, port=db_port)
        cursor = connection.cursor()
        cursor.execute("select * from login where usuario= %s and clave=%s",
                       (data['usuario'], data['clave']))
        rows = cursor.fetchall()
        resultList = []
        for datos in rows:
            resultList.append({
                'dni': datos[0],
                'usuario': datos[1]
                })
        cursor.close()
        return jsonify(resultList), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/back/persona', methods=['GET'])
def listar_datos():
    try:
        connection  = psycopg2.connect(database=db_name, user=db_user, password=db_password,host=db_host, port=db_port)
        cursor = connection.cursor()
        # Consultar datos en la base de datos
        cursor.execute("SELECT *,(((nombre::text || ' '::text) || apellido_p::text) || ' '::text) || apellido_m::text AS datos FROM persona")
        rows = cursor.fetchall()
        resultList = []
        for datos in rows:
            resultList.append({
                'dni': datos[0],
                'nombre': datos[1],
                'apellido_p': datos[2],
                'apellido_m': datos[3],
                'datos': datos[4]
                })
        cursor.close()
        return jsonify(resultList), 200
        #return jsonify(rows), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#End Point Ingresar Usuarios
@app.route('/back/persona', methods=['POST'])
def insertar_datos():
    try:
        data = request.json
        connection  = psycopg2.connect(database=db_name, user=db_user, password=db_password,host=db_host, port=db_port)
        cursor = connection.cursor()

        # Insertar datos en la base de datos
        cursor.execute("INSERT INTO persona (dni, nombre,apellido_p,apellido_m) VALUES (%s, %s,%s,%s)",
                       (data['dni'], data['nombre'],data['apellido_p'],data['apellido_m']))
        connection.commit()
        cursor.close()
        return jsonify({"message": "Datos insertados correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
  
#End Point Editar Usuarios    
@app.route('/back/persona', methods=['PUT'])
def actualizar_datos():
    try:
        data = request.json
        connection  = psycopg2.connect(database=db_name, user=db_user, password=db_password,host=db_host, port=db_port)
        cursor = connection.cursor()

        # Actualizar datos en la base de datos
        cursor.execute("UPDATE persona SET nombre = %s, apellido_p = %s,apellido_m = %s WHERE dni = %s",
                       (data['nombre'],data['apellido_p'],data['apellido_m'],data['dni']))

        connection.commit()
        cursor.close()

        return jsonify({"message": f"Datos actualizados para el usuario {data['dni']}"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#End Point Eliminar Persona   
@app.route('/back/persona/<int:dni>', methods=['DELETE'])
def eliminarPersona(dni):
    try:
       #data = request.json
        connection  = psycopg2.connect(database=db_name, user=db_user, password=db_password,host=db_host, port=db_port)
        cursor = connection.cursor()

        # Actualizar datos en la base de datos
        cursor.execute("DELETE FROM  persona WHERE dni = %s ",
                       (dni,))

        connection.commit()
        cursor.close()

        return jsonify({"message": "Registro eliminado"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
#################################################################
#End Point Listar Roles
@app.route('/back/rol', methods=['GET'])
def listar_roles():
    try:
        connection  = psycopg2.connect(database=db_name, user=db_user, password=db_password,host=db_host, port=db_port)
        cursor = connection.cursor()
        # Consultar datos en la base de datos
        cursor.execute("SELECT * FROM rol")
        rows = cursor.fetchall()
        resultList = []
        for datos in rows:
            resultList.append({
                'cod_rol': datos[0],
                'nombre': datos[1]
                })
        cursor.close()
        return jsonify(resultList), 200
        #return jsonify(rows), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#End Point Ingresar Roles
@app.route('/back/rol', methods=['POST'])
def insertarRoles():
    try:
        data = request.json
        connection  = psycopg2.connect(database=db_name, user=db_user, password=db_password,host=db_host, port=db_port)
        cursor = connection.cursor()

        # Insertar datos en la base de datos
        cursor.execute("INSERT INTO rol (nombre) VALUES ( %s )",
                       (data['nombre'],))
        connection.commit()
        cursor.close()
        return jsonify({"message": "Datos insertados correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#End Point Editar Roles    
@app.route('/back/rol', methods=['PUT'])
def actualizarRoles():
    try:
        data = request.json
        connection  = psycopg2.connect(database=db_name, user=db_user, password=db_password,host=db_host, port=db_port)
        cursor = connection.cursor()

        # Actualizar datos en la base de datos
        cursor.execute("UPDATE rol SET nombre = %s  WHERE cod_rol = %s",
                       (data['nombre'],data['cod_rol']))

        connection.commit()
        cursor.close()

        return jsonify({"message": f"Datos actualizados para el registro {data['cod_rol']}"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#End Point Eliminar Rol   
@app.route('/back/rol/<int:cod_rol>', methods=['DELETE'])
def eliminarRol(cod_rol):
    try:
       #data = request.json
        connection  = psycopg2.connect(database=db_name, user=db_user, password=db_password,host=db_host, port=db_port)
        cursor = connection.cursor()

        # Actualizar datos en la base de datos
        cursor.execute("DELETE FROM  rol WHERE cod_rol = %s ",
                       (cod_rol,))

        connection.commit()
        cursor.close()

        return jsonify({"message": "Registro eliminado"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
#######################################################################################
    
#End Point Listar Libro
@app.route('/back/libro', methods=['GET'])
def listar_libro():
    try:
        connection  = psycopg2.connect(database=db_name, user=db_user, password=db_password,host=db_host, port=db_port)
        cursor = connection.cursor()
        # Consultar datos en la base de datos
        cursor.execute("SELECT * FROM libro")
        rows = cursor.fetchall()
        resultList = []
        for datos in rows:
            resultList.append({
                'cod_libro': datos[0],
                'titulo': datos[1],
                'materia': datos[2],
                'autor': datos[3],
                'descripcion': datos[4],
                'stock': datos[5]
                })
        cursor.close()
        return jsonify(resultList), 200
        #return jsonify(rows), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#End Point Ingresar Libro
@app.route('/back/libro', methods=['POST'])
def insertar_libro():
    try:
        data = request.json
        connection  = psycopg2.connect(database=db_name, user=db_user, password=db_password,host=db_host, port=db_port)
        cursor = connection.cursor()

        # Insertar datos en la base de datos
        cursor.execute("INSERT INTO libro (titulo, materia, autor, descripcion, stock) VALUES (%s, %s, %s, %s, %s)",
                       (data['titulo'], data['materia'], data['autor'], data['descripcion'], data['stock']))
        connection.commit()
        cursor.close()
        return jsonify({"message": "Datos insertados correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#End Point Editar Libro   
@app.route('/back/libro', methods=['PUT'])
def actualizarLibro():
    try:
        data = request.json
        connection  = psycopg2.connect(database=db_name, user=db_user, password=db_password,host=db_host, port=db_port)
        cursor = connection.cursor()

        # Actualizar datos en la base de datos
        cursor.execute("UPDATE libro SET titulo = %s, materia = %s, autor = %s, descripcion = %s, stock = %s  WHERE cod_libro = %s",
                       (data['titulo'], data['materia'], data['autor'], data['descripcion'], data['stock'], data['cod_libro']))

        connection.commit()
        cursor.close()

        return jsonify({"message": f"Datos actualizados para el registro {data['cod_libro']}"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#End Point Eliminar Libro   
@app.route('/back/libro/<int:cod_libro>', methods=['DELETE'])
def eliminarLibro(cod_libro):
    try:
       #data = request.json
        connection  = psycopg2.connect(database=db_name, user=db_user, password=db_password,host=db_host, port=db_port)
        cursor = connection.cursor()

        # Actualizar datos en la base de datos
        cursor.execute("DELETE FROM  libro WHERE cod_libro = %s ",
                       (cod_libro,))

        connection.commit()
        cursor.close()

        return jsonify({"message": "Registro eliminado"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
#####################################################################################################
 #End Point Listar Login
@app.route('/back/login', methods=['GET'])
def listar_login():
    try:
        connection  = psycopg2.connect(database=db_name, user=db_user, password=db_password,host=db_host, port=db_port)
        cursor = connection.cursor()
        # Consultar datos en la base de datos
        cursor.execute("SELECT dni,usuario,clave,datos as persona FROM lista_usuarios")
        rows = cursor.fetchall()
        resultList = []
        for datos in rows:
            resultList.append({
                'dni': datos[0],
                'usuario': datos[1],
                'clave': datos[2],
                'persona': datos[3]                
                })
        cursor.close()
        return jsonify(resultList), 200
        #return jsonify(rows), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#End Point Ingresar Login
@app.route('/back/login', methods=['POST'])
def insertar_login():
    try:
        data = request.json
        connection  = psycopg2.connect(database=db_name, user=db_user, password=db_password,host=db_host, port=db_port)
        cursor = connection.cursor()

        # Insertar datos en la base de datos
        cursor.execute("INSERT INTO login (dni, usuario, clave) VALUES (%s, %s, %s)",
                       (data['dni'], data['usuario'], data['clave']))
        connection.commit()
        cursor.close()
        return jsonify({"message": "Datos insertados correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#End Point Editar Login  
@app.route('/back/login', methods=['PUT'])
def actualizarLogin():
    try:
        data = request.json
        connection  = psycopg2.connect(database=db_name, user=db_user, password=db_password,host=db_host, port=db_port)
        cursor = connection.cursor()

        # Actualizar datos en la base de datos
        cursor.execute("UPDATE login SET usuario = %s, clave = %s WHERE dni = %s",
                       (data['usuario'], data['clave'], data['dni']))

        connection.commit()
        cursor.close()

        return jsonify({"message": f"Datos actualizados para el registro {data['dni']}"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#End Point Eliminar Login   
@app.route('/back/login/<int:dni>', methods=['DELETE'])
def eliminarLogin(dni):
    try:
       #data = request.json
        connection  = psycopg2.connect(database=db_name, user=db_user, password=db_password,host=db_host, port=db_port)
        cursor = connection.cursor()

        # Actualizar datos en la base de datos
        cursor.execute("DELETE FROM  login WHERE dni = %s ",
                       (dni,))

        connection.commit()
        cursor.close()

        return jsonify({"message": "Registro eliminado"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
############################################################################

# End Point Listar Libro por Titulo
@app.route('/back/libro/titulo/<string:titulo>', methods=['GET'])
def listar_libro_por_titulo(titulo):
    try:
        connection = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        cursor = connection.cursor()

        # Consultar datos en la base de datos por título
        cursor.execute("SELECT * FROM libro WHERE titulo ILIKE %s", ('%' + titulo + '%',))
        rows = cursor.fetchall()
        resultList = []
        for datos in rows:
            resultList.append({
                'cod_libro': datos[0],
                'titulo': datos[1],
                'materia': datos[2],
                'autor': datos[3],
                'descripcion': datos[4],
                'stock': datos[5]
            })
        cursor.close()
        return jsonify(resultList), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# End Point Listar Libro por Materia
@app.route('/back/libro/materia/<string:materia>', methods=['GET'])
def listar_libro_por_materia(materia):
    try:
        connection = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        cursor = connection.cursor()

        # Consultar datos en la base de datos por materia
        cursor.execute("SELECT * FROM libro WHERE materia ILIKE %s", ('%' + materia + '%',))
        rows = cursor.fetchall()
        resultList = []
        for datos in rows:
            resultList.append({
                'cod_libro': datos[0],
                'titulo': datos[1],
                'materia': datos[2],
                'autor': datos[3],
                'descripcion': datos[4],
                'stock': datos[5]
            })
        cursor.close()
        return jsonify(resultList), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# End Point Listar Libro por Autor
@app.route('/back/libro/autor/<string:autor>', methods=['GET'])
def listar_libro_por_autor(autor):
    try:
        connection = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        cursor = connection.cursor()

        # Consultar datos en la base de datos por autor
        cursor.execute("SELECT * FROM libro WHERE autor ILIKE %s", ('%' + autor + '%',))
        rows = cursor.fetchall()
        resultList = []
        for datos in rows:
            resultList.append({
                'cod_libro': datos[0],
                'titulo': datos[1],
                'materia': datos[2],
                'autor': datos[3],
                'descripcion': datos[4],
                'stock': datos[5]
            })
        cursor.close()
        return jsonify(resultList), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

###############################################################333
# End Point Listar Persona_Rol
@app.route('/back/persona_rol', methods=['GET'])
def listar_persona_rol():
    try:
        connection = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        cursor = connection.cursor()

        # Consultar datos en la base de datos
        cursor.execute("SELECT * FROM persona_rol")
        rows = cursor.fetchall()
        resultList = []
        for datos in rows:
            resultList.append({
                'dni': datos[0],
                'cod_rol': datos[1]
            })
        cursor.close()
        return jsonify(resultList), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# End Point Ingresar Persona_Rol
@app.route('/back/persona_rol', methods=['POST'])
def insertar_persona_rol():
    try:
        data = request.json
        connection = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        cursor = connection.cursor()

        # Insertar datos en la base de datos
        cursor.execute("INSERT INTO persona_rol (dni, cod_rol) VALUES (%s, %s)",
                       (data['dni'], data['cod_rol']))
        connection.commit()
        cursor.close()
        return jsonify({"message": "Datos insertados correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# End Point Editar Persona_Rol
@app.route('/back/persona_rol', methods=['PUT'])
def actualizar_persona_rol():
    try:
        data = request.json
        connection = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        cursor = connection.cursor()

        # Actualizar datos en la base de datos
        cursor.execute("UPDATE persona_rol SET cod_rol = %s WHERE dni = %s",
                       (data['cod_rol'], data['dni']))

        connection.commit()
        cursor.close()

        return jsonify({"message": f"Datos actualizados para el usuario {data['dni']}"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# End Point Eliminar Persona_Rol
@app.route('/back/persona_rol/<int:dni>', methods=['DELETE'])
def eliminar_persona_rol(dni):
    try:
        connection = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        cursor = connection.cursor()

        # Eliminar datos en la base de datos
        cursor.execute("DELETE FROM persona_rol WHERE dni = %s",
                       (dni,))

        connection.commit()
        cursor.close()

        return jsonify({"message": "Registro eliminado"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
###########################################################################3
# End Point Listar Prestamo Detalle
@app.route('/back/prestamo_det/<int:cod_prestamo>', methods=['GET'])
def listar_prestamo_det(cod_prestamo):
    try:
        connection = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        cursor = connection.cursor()

        # Consultar datos en la base de datos
        cursor.execute("""
            SELECT p.cod_prestamo_det, p.cod_prestamo, p.cod_libro, l.titulo as libro, p.prestado 
            FROM prestamo_det p
            JOIN libro l ON l.cod_libro = p.cod_libro 
            WHERE prestado and cod_prestamo = %s
        """, (cod_prestamo,))
        rows = cursor.fetchall()
        resultList = []
        for datos in rows:
            resultList.append({
                'cod_prestamo_det': datos[0],
                'cod_prestamo': datos[1],
                'cod_libro': datos[2],
                'libro': datos[3],
                'prestado': datos[4]
            })
        cursor.close()
        return jsonify(resultList), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# End Point Ingresar Prestamo Detalle
@app.route('/back/prestamo_det', methods=['POST'])
def insertar_prestamo_det():
    try:
        data = request.json
        connection = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        cursor = connection.cursor()

        # Insertar datos en la base de datos
        cursor.execute("INSERT INTO prestamo_det (cod_prestamo, cod_libro, prestado) VALUES (%s, %s, %s)",
                       (data['cod_prestamo'], data['cod_libro'], data['prestado']))
        connection.commit()
        cursor.close()
        return jsonify({"message": "Datos insertados correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# End Point Editar Prestamo Detalle
@app.route('/back/prestamo_det', methods=['PUT'])
def actualizar_prestamo_det():
    try:
        data = request.json
        connection = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        cursor = connection.cursor()

        # Actualizar datos en la base de datos
        cursor.execute("UPDATE prestamo_det SET prestado = %s WHERE cod_prestamo_det = %s",
                       (data['prestado'], data['cod_prestamo_det']))

        connection.commit()
        cursor.close()

        return jsonify({"message": f"Datos actualizados para el detalle de préstamo {data['cod_prestamo_det']}"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# End Point Eliminar Prestamo Detalle
@app.route('/back/prestamo_det/<int:cod_prestamo_det>', methods=['DELETE'])
def eliminar_prestamo_det(cod_prestamo_det):
    try:
        connection = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        cursor = connection.cursor()

        # Eliminar datos en la base de datos
        cursor.execute("UPDATE  prestamo_det SET prestado=false WHERE cod_prestamo_det = %s",
                       (cod_prestamo_det,))

        connection.commit()
        cursor.close()

        return jsonify({"message": "Detalle de préstamo eliminado"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
#######################################################################3    

    ##EndPoints Prestamo_Cab
@app.route('/back/prestamo_cab', methods=['GET'])
def listar_cabecera_prestamos():
    try:
        connection = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        cursor = connection.cursor()

        cursor.execute("select * from fn_prestamos() ")
        rows = cursor.fetchall()
        resultList = []
        for datos in rows:
            resultList.append({
                'cod_prestamo': datos[0],
                'dni': datos[1],
                'cod_bibliotecario': datos[2],
                'fecha_entrega': datos[3],
                'fecha_devolucion': datos[4],
                'cliente': datos[5],
                'bibliotecario': datos[6]
            })
        cursor.close()
        return jsonify(resultList), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/back/ranking-prestado', methods=['GET'])
def listar_Libros_prestados():
    try:
        connection = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        cursor = connection.cursor()

        cursor.execute("select usuario,libro,count(usuario) cantidad from lista_prestamos where prestado group by usuario,libro order by usuario ")
        rows = cursor.fetchall()
        resultList = []
        for datos in rows:
            resultList.append({
                'usuario': datos[0],
                'libro': datos[1],
                'cantidad': datos[2]
            })
        cursor.close()
        return jsonify(resultList), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/back/ranking-devuelto', methods=['GET'])
def listar_Libros_devueltos():
    try:
        connection = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        cursor = connection.cursor()

        cursor.execute("select usuario,libro,1 as cantidad from lista_prestamos where not prestado ")
        rows = cursor.fetchall()
        resultList = []
        for datos in rows:
            resultList.append({
                'usuario': datos[0],
                'libro': datos[1],
                'cantidad': datos[2]
            })
        cursor.close()
        return jsonify(resultList), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
####################################################
##Endpoint Eliminar

@app.route('/back/prestamo_cab/<int:cod_prestamo>', methods=['DELETE'])
def eliminar_prestamo_cab(cod_prestamo):
    try:
        connection = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        cursor = connection.cursor()
        # Eliminar datos en la base de datos
        cursor.execute("DELETE FROM prestamo_cab WHERE cod_prestamo = %s",
                       (cod_prestamo,))

        connection.commit()
        cursor.close()

        return jsonify({"message": "Se Eliminó el Registro"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

####################################
    ##EndPoint Guardar
@app.route('/back/prestamo_cab', methods=['POST'])
def insertar_prestamo_cab():
    try:
        data = request.json
        connection = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        cursor = connection.cursor()

       # Insertar datos en la base de datos y obtener la fila insertada
        cursor.execute("INSERT INTO prestamo_cab (dni, cod_bibliotecario, fecha_entrega, fecha_devolucion) VALUES (%s, %s, %s, %s) RETURNING *",
                       (data['dni'], data['cod_bibliotecario'], data['fecha_entrega'], data['fecha_devolucion']))
        # Obtener la fila insertada
        prestamo_cabecera = cursor.fetchone()
        # Obtener los nombres de las columnas
        column_names = [desc[0] for desc in cursor.description]
        connection.commit()
        cursor.close()

        # Crear el objeto con el nombre de las cabeceras y la fila insertada
        prestamo_cabecera_dict = {}
        for i, column_name in enumerate(column_names):
            prestamo_cabecera_dict[column_name] = prestamo_cabecera[i]

        # Devolver el objeto con el nombre de las cabeceras y la fila insertada
        return jsonify({"prestamo_cabecera": prestamo_cabecera_dict}), 200

    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
####################################
#EndPoint  Editar - prestamo_Cab    
@app.route('/back/prestamo_cab', methods=['PUT'])
def actualizar_prestamo_cab():
    try:
        data = request.json
        connection = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        cursor = connection.cursor()

        # Actualizar datos en la base de datos
        cursor.execute("UPDATE prestamo_cab SET fecha_entrega = %s , fecha_devolucion = %s WHERE cod_prestamo = %s",
                       (data['fecha_entrega'], data['fecha_devolucion'], data['cod_prestamo']))

        connection.commit()
        cursor.close()

        return jsonify({"message": "Datos actualizados para el prestamo {data['cod_prestamo']}"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500




################################

#Asigando la ruta al archivo main
if __name__ == "__main__":
    app.run(debug=True)
