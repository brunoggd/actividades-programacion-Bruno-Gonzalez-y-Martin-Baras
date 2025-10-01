import mysql.connector 
from mysql.connector import Error

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class SistemaBaseDeDatos(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión de Base de Datos MySQL")
        self.setGeometry(100, 100, 900, 400)

        #CSS
        self.setStyleSheet("""
            QMainWindow {background-color: #FF8F8F;
                font-family: Aptos;}
                           
            QLabel {color: Black;
                font-family: Aptos;
                font-size: 20px;
                font-weight: bold;}
                           
            QTextEdit {background-color:white;
                    border: 8px solid white;
                    border-radius: 16px;
                    padding: 4px 4px;
                    color:black;
                    font-size: 16px}
                           
            QPushButton {background-color: #D95252;
                color: Black;
                border: 2px solid black;
                padding: 4px 8px;
                border-radius: 8px;
                font-family: Aptos;
                font-size: 16px;}""")

        self.resultado_conexion=''
        self.resultado_crear_tabla_usuarios=''
        self.resultado_consultar_usuario=''
        self.resultado_busqueda_usuario_por_mail=''
        self.resultado_final=''
        self.resultado_avanzar_usuario=''

        self.salto_de_pagina=0
        self.paginas=10

        contenedor_lienso=QWidget()
        contenedor_botones=QWidget()

        layout_lienso=QVBoxLayout()
        layout_lienso.setAlignment(Qt.AlignCenter)

        self.layout_botones=QVBoxLayout()
        self.layout_botones.setAlignment(Qt.AlignCenter)

        etiqueta=QLabel("Sistema Gestor de Base de Datos")

        self.lienso=QTextEdit()
        self.lienso.setReadOnly(True)
        
        self.boton_ejecutar=QPushButton("EJECUTAR")
        self.boton_ejecutar.clicked.connect(self.main)

        self.boton_verificar_conexion=QPushButton("VERIFICAR CONEXION")
        self.boton_verificar_conexion.clicked.connect(self.informacion_database)

        self.boton_agregar_usuario=QPushButton("AGREGAR USUARIO")
        self.boton_agregar_usuario.clicked.connect(self.insertar_usuario)

        self.boton_consultar_tabla=QPushButton("CONSULTAR TABLA")
        self.boton_consultar_tabla.clicked.connect(self.consultar_usuarios)

        self.boton_eliminar_usuario=QPushButton("ELIMINAR USUARIO")
        self.boton_eliminar_usuario.clicked.connect(self.eliminar_usuario)

        boton_avanzar=QPushButton("Siguiente")
        boton_avanzar.clicked.connect(self.avanzar_paginas)

        boton_retroceder=QPushButton("Anterior")
        boton_retroceder.clicked.connect(self.retroceder_paginas)

        self.boton_finalizar_conexion=QPushButton("FINALIZAR")
        self.boton_finalizar_conexion.clicked.connect(self.finalizar_conexion)
        self.boton_finalizar_conexion.hide()

        self.etiqueta_busqueda_mail=QLabel("Buscar por mail:")
        self.busqueda_mail=QLineEdit()
        
        self.boton_buscar_por_mail=QPushButton("BUSCAR POR MAIL")
        self.boton_buscar_por_mail.clicked.connect(lambda: self.buscar_usuario_por_email())

        layout_lienso.addWidget(etiqueta,alignment=Qt.AlignCenter)
        layout_lienso.addWidget(self.lienso)
        layout_lienso.addWidget(boton_retroceder)
        layout_lienso.addWidget(boton_avanzar)

        #AGREGAR USUARIO
        etiqueta_nombre=QLabel("Nombre:")
        self.inputbox_nombre=QLineEdit()
        etiqueta_email=QLabel("Email:")
        self.inputbox_email=QLineEdit()
        etiqueta_edad=QLabel("Edad:")
        self.inputbox_edad=QLineEdit()

        #ELIMINAR USUARIO
        etiqueta_eliminar_usuario=QLabel("Ingresar ID para eliminar")
        self.inputbox_id_eliminar=QLineEdit()

        #AGREGAR WIDGETS A LAYOUT
        self.layout_botones.addWidget(self.boton_ejecutar)
        self.layout_botones.addWidget(self.boton_verificar_conexion)
        self.layout_botones.addWidget(self.boton_consultar_tabla)
        self.layout_botones.addWidget(self.etiqueta_busqueda_mail)
        self.layout_botones.addWidget(self.busqueda_mail)
        self.layout_botones.addWidget(self.boton_buscar_por_mail)

        #AGREGAR WIDGETS AGREGAR USUARIO A LAYOUT
        self.layout_botones.addWidget(etiqueta_nombre, alignment=Qt.AlignLeft)
        self.layout_botones.addWidget(self.inputbox_nombre)
        self.layout_botones.addWidget(etiqueta_email, alignment=Qt.AlignLeft)
        self.layout_botones.addWidget(self.inputbox_email)
        self.layout_botones.addWidget(etiqueta_edad, alignment=Qt.AlignLeft)
        self.layout_botones.addWidget(self.inputbox_edad)
        self.layout_botones.addWidget(self.boton_agregar_usuario)

        #AGREGAR WIDGETS ELIMINAR USUARIO A LAYOUT
        self.layout_botones.addWidget(etiqueta_eliminar_usuario)
        self.layout_botones.addWidget(self.inputbox_id_eliminar)
        self.layout_botones.addWidget(self.boton_eliminar_usuario)

        #DEFINIR CONTENEDORES DE WIDGETS
        contenedor_lienso.setLayout(layout_lienso)
        contenedor_botones.setLayout(self.layout_botones)

        self.layout_botones.addWidget(self.boton_finalizar_conexion)

        splitter=QSplitter(Qt.Horizontal)
        splitter.addWidget(contenedor_lienso)
        splitter.addWidget(contenedor_botones)
        self.setCentralWidget(splitter)
        splitter.handle(1).setEnabled(False)  #splitter inmutable

    def avanzar_paginas(self):
        conexion=self.conectar_mysql()
        try:
            cursor=conexion.cursor()

            consulta=f"SELECT * FROM usuarios ORDER BY id LIMIT {self.paginas} OFFSET {self.salto_de_pagina};"
            self.salto_de_pagina += self.paginas

            cursor.execute(consulta)
            
            usuarios=cursor.fetchall()

            self.resultado_avanzar_usuario="Lista de usuarios:\n"
            self.resultado_avanzar_usuario +="-" * 80 + '\n'
            self.resultado_avanzar_usuario +=f"{'ID':<5} {'Nombre':<20} {'Email':<30} {'Edad':<5} {'Fecha de creación'}\n"
            self.resultado_avanzar_usuario +="-" * 80 + '\n'

            for usuario in usuarios:
                id_usuario,nombre,email,edad,fecha=usuario
                self.resultado_avanzar_usuario += f"\n{id_usuario:<5} {nombre:<20} {email:<30} {edad or 'N/A':<5} {fecha}\n"
            self.lienso.setText(self.resultado_avanzar_usuario)
            
            self.resultado_avanzar_usuario += f"\nTotal de usuarios: {len(usuarios)}"

        except Error as e:
            self.resultado_avanzar_usuario=f"Error al consultar usuarios: {e}"
            return None

    def retroceder_paginas(self):
        conexion=self.conectar_mysql()
        try:
            cursor=conexion.cursor()

            consulta=f"SELECT * FROM usuarios ORDER BY id LIMIT {self.paginas} OFFSET {self.salto_de_pagina};"
            self.salto_de_pagina -= self.paginas

            cursor.execute(consulta)
            
            usuarios=cursor.fetchall()

            self.resultado_avanzar_usuario="Lista de usuarios:\n"
            self.resultado_avanzar_usuario +="-" * 80 + '\n'
            self.resultado_avanzar_usuario +=f"{'ID':<5} {'Nombre':<20} {'Email':<30} {'Edad':<5} {'Fecha de creación'}\n"
            self.resultado_avanzar_usuario +="-" * 80 + '\n'

            for usuario in usuarios:
                id_usuario,nombre,email,edad,fecha=usuario
                self.resultado_avanzar_usuario += f"\n{id_usuario:<5} {nombre:<20} {email:<30} {edad or 'N/A':<5} {fecha}\n"
            self.lienso.setText(self.resultado_avanzar_usuario)
            
            self.resultado_avanzar_usuario += f"\nTotal de usuarios: {len(usuarios)}"

        except Error as e:
            self.resultado_avanzar_usuario=f"Error al consultar usuarios: {e}"
            return None

    def conectar_mysql(self):
        try:
            conexion=mysql.connector.connect(
                host='localhost',
                database='EjemploBD',
                user='root',
                password='brunogonzalez10'
            )

            return conexion

        except Error as e:
            self.resultado_conexion=f"Error al conectar a MySQL: {e}"
            QMessageBox.warning(self,"Error",self.resultado_conexion)
            return None
    
    def informacion_database(self):
        conexion = self.conectar_mysql()
        if conexion.is_connected():
            info_servidor=conexion.get_server_info()

            cursor=conexion.cursor()
            cursor.execute("SELECT DATABASE();")
            bd_actual=cursor.fetchone()
            self.resultado_conexion=f"""Conexión exitosa a MySQL
Información del servidor: MySQL {info_servidor}
Base de datos actual: {bd_actual[0]}"""
            QMessageBox.information(self,"Exito",self.resultado_conexion)

    def crear_tabla_usuarios(self):
        conexion = self.conectar_mysql()
        try:
            cursor=conexion.cursor()

            crear_tabla=""" 
                        CREATE TABLE IF NOT EXISTS usuarios (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            nombre VARCHAR(100) NOT NULL,
                            email VARCHAR(100) UNIQUE NOT NULL,
                            edad INT NOT NULL,
                            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )"""

            
            cursor.execute(crear_tabla)
            self.resultado_crear_tabla_usuarios="Tabla 'Usuarios' creada o verificada correctamente"
            QMessageBox.information(self, "Exito", self.resultado_crear_tabla_usuarios)

        except Error as e:
            self.resultado_crear_tabla_usuarios=f"Error al crear tabla: {e}"
            QMessageBox.information(self, "Error", self.resultado_crear_tabla_usuarios)
        finally:
            if conexion.is_connected():
                conexion.close()
            
    def insertar_usuario(self):
        conexion = self.conectar_mysql()

        nombre=self.inputbox_nombre.text().strip()
        email=self.inputbox_email.text().strip()
        edad=self.inputbox_edad.text().strip()
        
        if not nombre or not email or not edad:
            QMessageBox.warning(self, "Error", "No deje campos vacios")
        else:
            try:
                cursor=conexion.cursor()

                insertar_sql="INSERT INTO usuarios (nombre,email,edad) VALUES (%s,%s,%s)"
                datos_usuario=(nombre,email,edad)

                cursor.execute(insertar_sql,datos_usuario)
                conexion.commit()

                self.resultado_insertar_usuario=f"Usuario '{nombre}' insertado correctamente (ID: {cursor.lastrowid})"
                QMessageBox.information(self, "Exito", self.resultado_insertar_usuario)
            
            except Error as e:
                self.resultado_insertar_usuario=f"Error al insertar usuario: {e}"
                QMessageBox.warning(self, "Error", self.resultado_insertar_usuario)

            finally:
                if conexion.is_connected():
                    conexion.close()

    def eliminar_usuario(self):
        conexion = self.conectar_mysql()

        id=self.inputbox_id_eliminar.text().strip()

        if not id:
            QMessageBox.warning(self, "Error", "No deje campos vacios")
        else:
            try:
                cursor=conexion.cursor()

                eliminar_sql="DELETE FROM usuarios WHERE id=%s;"

                cursor.execute(eliminar_sql, (id,))

                self.resultado_eliminar_usuario=f"Eliminacion sastifactoria"
                QMessageBox.information(self, "Exito", self.resultado_eliminar_usuario)

                conexion.commit()
            
            except Error as e:
                self.resultado_eliminar_usuario=f"Error al eliminar usuario: {e}"
                QMessageBox.warning(self, "Error", self.resultado_eliminar_usuario)

            finally:
                if conexion.is_connected():
                    conexion.close()


    def consultar_usuarios(self):     
        conexion = self.conectar_mysql()
        try:
            cursor=conexion.cursor()

            consulta_sql="SELECT id,nombre,email,edad,fecha_creacion FROM usuarios"
            cursor.execute(consulta_sql)

            usuarios=cursor.fetchall()

            self.resultado_consultar_usuario="Lista de usuarios:\n"
            self.resultado_consultar_usuario +="-" * 80 + '\n'
            self.resultado_consultar_usuario +=f"{'ID':<5} {'Nombre':<20} {'Email':<30} {'Edad':<5} {'Fecha de creación'}\n"
            self.resultado_consultar_usuario +="-" * 80 + '\n'

            for usuario in usuarios:
                id_usuario,nombre,email,edad,fecha=usuario
                self.resultado_consultar_usuario += f"\n{id_usuario:<5} {nombre:<20} {email:<30} {edad or 'N/A':<5} {fecha}\n"
            self.lienso.setText(self.resultado_consultar_usuario)

            
            self.resultado_consultar_usuario += f"\nTotal de usuarios: {len(usuarios)}"

        except Error as e:
            self.resultado_consultar_usuario=f"Error al consultar usuarios: {e}"
            return None

    def buscar_usuario_por_email(self):
        conexion = self.conectar_mysql()
        try:
            if not self.busqueda_mail.text().strip():
                self.lienso.setText("Ingrese un mail")
            else:
                cursor=conexion.cursor()

                buscar_sql="SELECT * FROM usuarios WHERE email = %s"
                cursor.execute(buscar_sql,(self.busqueda_mail.text().strip(),))

                usuario=cursor.fetchone()

                if usuario:
                    self.resultado_busqueda_usuario_por_mail=f"""Usuario encontrado:
    ID: {usuario[0]}
    Nombre: {usuario[1]}
    Email: {usuario[2]}
    Edad: {usuario[3] or 'N/A'}
    Fecha de creación: {usuario[4]}"""
                    self.lienso.setText(self.resultado_busqueda_usuario_por_mail)
                else:
                    self.resultado_busqueda_usuario_por_mail=f"No se encontró usuario con email: {self.busqueda_mail.text().strip()}"
                    self.lienso.setText(self.resultado_busqueda_usuario_por_mail)
        
        except Error as e:
            self.resultado_busqueda_usuario_por_mail=f"Error al buscar usuario: {e}"
            self.lienso.setText(self.resultado_busqueda_usuario_por_mail)

    def main(self):
        conexion = self.conectar_mysql()

        if conexion:
            try:
                self.crear_tabla_usuarios()

                #self.insertar_usuario(conexion,"Juan Pérez","juan.perez@email.com",25)
                #self.insertar_usuario(conexion,"María González","maria.gonzalez@email.com",30)
                #self.insertar_usuario(conexion,"Carlos Rodríguez","carlos.rodriguez@email.com",25)

                self.consultar_usuarios()

                self.lienso.setText(self.resultado_final)

                self.boton_finalizar_conexion.show()
            
            except Exception as e:
                resultado=f"Error en operaciones: {e}"
                self.lienso.setText(resultado)

        else:
            resultado="\nNo se pudo establecer conexión con MySQL\n"
            resultado += "\nVerifique:"
            resultado += "\n> Que MySQL esté ejecutándose"
            resultado += "\n> Las credenciales de conexión"
            resultado += "\n> Que exista la base de datos 'EjemploBD'"
            self.resultado_final += resultado
            self.lienso.setText(self.resultado_final)

    def finalizar_conexion(self,conexion):
        self.boton_finalizar_conexion.hide()
        if conexion:  
            conexion.close()         
        QMessageBox.information(self,"Exito", "Conexión cerrada correctamente")         
        self.close()        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sistema = SistemaBaseDeDatos()
    sistema.show()
    sys.exit(app.exec_())
    