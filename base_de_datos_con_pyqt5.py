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
        
        conexion=mysql.connector.connect(
                host='localhost',
                database='EjemploBD',
                user='root',
                password='brunogonzalez10'
            )

        self.resultado_conexion=''
        self.resultado_crear_tabla_usuarios=''
        self.resultado_insertar_usuario=''
        self.resultado_consultar_usuario=''
        self.resultado_busqueda_usuario_por_mail=''
        self.resultado_final=''

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

        boton_verificar_conexion=QPushButton("VERIFICAR CONEXION")
        boton_verificar_conexion.clicked.connect(self.conectar_mysql)

        self.boton_finalizar_conexion=QPushButton("FINALIZAR")
        self.boton_finalizar_conexion.clicked.connect(self.finalizar_conexion)
        self.boton_finalizar_conexion.hide()

        self.etiqueta_busqueda_mail=QLabel("Buscar por mail:")
        self.busqueda_mail=QLineEdit()
        
        boton_buscar_por_mail=QPushButton("BUSCAR POR MAIL")
        boton_buscar_por_mail.clicked.connect(lambda: self.buscar_usuario_por_email(conexion))

        layout_lienso.addWidget(etiqueta,alignment=Qt.AlignCenter)
        layout_lienso.addWidget(self.lienso)

        self.layout_botones.addWidget(self.boton_ejecutar)
        self.layout_botones.addWidget(boton_verificar_conexion)
        self.layout_botones.addWidget(boton_buscar_por_mail)
        self.layout_botones.addWidget(self.etiqueta_busqueda_mail)
        self.layout_botones.addWidget(self.busqueda_mail)
        self.layout_botones.addWidget(self.boton_finalizar_conexion,alignment=Qt.AlignCenter)

        contenedor_lienso.setLayout(layout_lienso)
        contenedor_botones.setLayout(self.layout_botones)

        splitter=QSplitter(Qt.Horizontal)
        splitter.addWidget(contenedor_lienso)
        splitter.addWidget(contenedor_botones)
        self.setCentralWidget(splitter)

    def conectar_mysql(self):
        try:
            conexion=mysql.connector.connect(
                host='localhost',
                database='EjemploBD',
                user='root',
                password='brunogonzalez10'
            )

            if conexion.is_connected():
                info_servidor=conexion.get_server_info()

                cursor=conexion.cursor()
                cursor.execute("SELECT DATABASE();")
                bd_actual=cursor.fetchone()
                self.resultado_conexion=f"""Conexión exitosa a MySQl
Información del servidor: MySQL {info_servidor}
Base de datos actual: {bd_actual[0]}"""

                QMessageBox.information(self,"Conexión establecida",self.resultado_conexion)

                return conexion
            
        except Error as e:
            self.resultado_conexion=f"Error al conectar a MySQL: {e}"
            QMessageBox.information(self,"Error",self.resultado_conexion)
            return None
        
    def crear_tabla_usuarios(self,conexion):
        try:
            cursor=conexion.cursor()

            crear_tabla=""" 
                        CREATE TABLE IF NOT EXISTS usuarios (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            nombre VARCHAR(100) NOT NULL,
                            email VARCHAR(100) UNIQUE NOT NULL,
                            edad INT,
                            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )"""

            
            cursor.execute(crear_tabla)
            self.resultado_crear_tabla_usuarios="\nTabla 'Usuarios' creada o verificada correctamente"

        except Error as e:
            self.resultado_crear_tabla_usuarios=f"Error al crear tabla: {e}"

    def insertar_usuario(self,conexion,nombre,email,edad):
        try:
            cursor=conexion.cursor()

            insertar_sql="INSERT INTO usuarios (nombre,email,edad) VALUES (%s,%s,%s)"
            datos_usuario=(nombre,email,edad)

            cursor.execute(insertar_sql,datos_usuario)
            conexion.commit()

            self.resultado_insertar_usuario=f"Usuario '{nombre}' insertado correctamente (ID: {cursor.lastrowid})"
        
        except Error as e:
            self.resultado_insertar_usuario=f"\nError al insertar usuario: {e}"

    def consultar_usuarios(self,conexion):
        try:
            cursor=conexion.cursor()

            consulta_sql="SELECT id,nombre,email,edad,fecha_creacion FROM usuarios"
            cursor.execute(consulta_sql)

            usuarios=cursor.fetchall()

            self.resultado_consultar_usuario="\nLista de usuarios:\n"
            self.resultado_consultar_usuario +="-" * 80 + '\n'
            self.resultado_consultar_usuario +=f"{'ID':<5} {'Nombre':<20} {'Email':<30} {'Edad':<5} {'Fecha Creación'}\n"
            self.resultado_consultar_usuario +="-" * 80 + '\n'

            for usuario in usuarios:
                id_usuario,nombre,email,edad,fecha=usuario
                self.resultado_consultar_usuario += f"\n{id_usuario:<5} {nombre:<20} {email:<30} {edad or 'N/A':<5} {fecha}\n"

            self.resultado_consultar_usuario += f"\nTotal de usuarios: {len(usuarios)}"

        except Error as e:
            self.resultado_consultar_usuario=f"Error al consultar usuarios: {e}"

    def buscar_usuario_por_email(self,conexion):
        try:
            cursor=conexion.cursor()

            buscar_sql="SELECT * FROM usuarios WHERE email = %s"
            cursor.execute(buscar_sql,(self.busqueda_mail.text(),))

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
                self.resultado_busqueda_usuario_por_mail=f"No se encontró usuario con email: {self.busqueda_mail.text()}"
                self.lienso.setText(self.resultado_busqueda_usuario_por_mail)
        
        except Error as e:
            self.resultado_busqueda_usuario_por_mail=f"Error al buscar usuario: {e}"
            self.lienso.setText(self.resultado_busqueda_usuario_por_mail)

    def main(self):
        self.boton_ejecutar.hide()
        conexion=mysql.connector.connect(
                host='localhost',
                database='EjemploBD',
                user='root',
                password='brunogonzalez10'
            )

        if conexion:
            try:
                self.crear_tabla_usuarios(conexion)

                self.insertar_usuario(conexion,"Juan Pérez","juan.perez@email.com",25)
                self.insertar_usuario(conexion,"María González","maria.gonzalez@email.com",30)
                self.insertar_usuario(conexion,"Carlos Rodríguez","carlos.rodriguez@email.com",25)

                self.consultar_usuarios(conexion)

                #self.buscar_usuario_por_email(conexion,"juan.perez@email.com")
                self.resultado_final=self.resultado_crear_tabla_usuarios + self.resultado_insertar_usuario + self.resultado_consultar_usuario
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
        conexion=mysql.connector.connect(
                host='localhost',
                database='EjemploBD',
                user='root',
                password='brunogonzalez10'
            )
        if conexion.is_connected():
            conexion.close()
            resultado="\nConexión cerrada correctamente.\n"
            self.lienso.setText(resultado)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sistema = SistemaBaseDeDatos()
    sistema.show()
    sys.exit(app.exec_())