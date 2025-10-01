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
        self.crear_interfaz()
        #CSS
        self.setStyleSheet("""
            QMainWindow {background-color: #29BAAD;
                font-family: Aptos;}
                           
            QLabel {color: Black;
                font-family: Aptos;
                font-size: 16px;
                font-weight: bold;
                border: None;}
                           
            QTextEdit {background-color:white;
                    border: 8px solid white;
                    border-radius: 16px;
                    padding: 4px 4px;
                    color:black;
                    font-size: 16px}
                           
            QPushButton {background-color: #51D6D0;
                color: Black;
                border: 2px solid #8FF2EC;
                padding: 4px 8px;
                border-radius: 8px;
                font-family: Aptos;
                font-size: 16px;}
        
            QGroupBox {border: None;}
                           
            QSplitter::handle {background-color: #039687;}
                           
            QStatusBar {background-color: #039687;}""")

        self.resultado_conexion=''
        self.resultado_crear_tabla_usuarios=''
        self.resultado_consultar_usuario=''
        self.resultado_busqueda_usuario_por_mail=''
        self.resultado_final=''
        self.resultado_avanzar_usuario=''
        self.flag=True
        
    def crear_interfaz(self):
        self.paginas_salteadas=0
        self.limite_paginas=10
        self.indice_pagina=1

        contenedor_lienso=QWidget()
        contenedor_botones=QWidget()

        layout_lienso=QVBoxLayout()
        layout_lienso.setAlignment(Qt.AlignCenter)

        self.layout_botones=QVBoxLayout()
        self.layout_botones.setAlignment(Qt.AlignCenter)

        self.lienso=QTextEdit()
        self.lienso.setReadOnly(True)
        
        self.boton_verificar_conexion=QPushButton("VERIFICAR CONEXION")
        self.boton_verificar_conexion.clicked.connect(self.informacion_database)

        self.boton_agregar_usuario=QPushButton("AGREGAR USUARIO")
        self.boton_agregar_usuario.clicked.connect(self.gestionar_boton_agregar_usuario)

        self.boton_consultar_tabla=QPushButton("CONSULTAR TABLA")
        self.boton_consultar_tabla.clicked.connect(self.consultar_toda_la_tabla)

        self.boton_eliminar_usuario=QPushButton("ELIMINAR USUARIO")
        self.boton_eliminar_usuario.clicked.connect(self.gestionar_boton_eliminar_usuario)

        self.boton_avanzar=QPushButton("Siguiente")
        self.boton_avanzar.clicked.connect(self.avanzar_paginas)
        self.boton_avanzar.hide()

        self.boton_retroceder=QPushButton("Anterior")
        self.boton_retroceder.clicked.connect(self.retroceder_paginas)
        self.boton_retroceder.hide()

        self.boton_finalizar_conexion=QPushButton("FINALIZAR")
        self.boton_finalizar_conexion.clicked.connect(self.finalizar_conexion)
        self.boton_finalizar_conexion.hide()

        self.etiqueta_busqueda_mail=QLabel("Buscar por mail:")
        self.etiqueta_busqueda_mail.setStyleSheet("border: None;")
        self.busqueda_mail=QLineEdit()

        self.etiqueta_busqueda_mail.hide()
        self.busqueda_mail.hide()
        
        self.boton_buscar_por_mail=QPushButton("BUSCAR POR MAIL")
        self.boton_buscar_por_mail.clicked.connect(self.gestionar_boton_buscar_usuario_por_mail)

        grupo_botones_avanzar_y_retroceder=QGroupBox()
        layout_grupo_botones=QHBoxLayout()
        layout_grupo_botones.addWidget(self.boton_retroceder)
        layout_grupo_botones.addWidget(self.boton_avanzar)
        grupo_botones_avanzar_y_retroceder.setLayout(layout_grupo_botones)

        layout_lienso.addWidget(self.lienso)
        layout_lienso.addWidget(grupo_botones_avanzar_y_retroceder)

        #AGREGAR USUARIO
        self.etiqueta_nombre=QLabel("Nombre:")
        self.etiqueta_nombre.setStyleSheet("border: None;")
        self.inputbox_nombre=QLineEdit()
        self.etiqueta_email=QLabel("Email:")
        self.etiqueta_email.setStyleSheet("border: None;")
        self.inputbox_email=QLineEdit()
        self.etiqueta_edad=QLabel("Edad:")
        self.etiqueta_edad.setStyleSheet("border: None;")
        self.inputbox_edad=QLineEdit()

        self.etiqueta_nombre.hide()
        self.etiqueta_email.hide()
        self.etiqueta_edad.hide()

        self.inputbox_nombre.hide()
        self.inputbox_email.hide()
        self.inputbox_edad.hide()

        #ELIMINAR USUARIO
        self.etiqueta_eliminar_usuario=QLabel("Ingresar ID para eliminar")
        self.etiqueta_eliminar_usuario.setStyleSheet("border: None;")
        self.inputbox_id_eliminar=QLineEdit()

        self.etiqueta_eliminar_usuario.hide()
        self.inputbox_id_eliminar.hide()

        #AGREGAR WIDGETS A LAYOUT
        self.layout_botones.addWidget(self.boton_verificar_conexion,alignment=Qt.AlignCenter)
        self.layout_botones.addWidget(self.boton_consultar_tabla,alignment=Qt.AlignCenter)
        self.layout_botones.addWidget(self.etiqueta_busqueda_mail)
        self.layout_botones.addWidget(self.busqueda_mail)
        self.layout_botones.addWidget(self.boton_buscar_por_mail,alignment=Qt.AlignCenter)

        #AGREGAR WIDGETS AGREGAR USUARIO A LAYOUT
        self.layout_botones.addWidget(self.etiqueta_nombre, alignment=Qt.AlignLeft)
        self.layout_botones.addWidget(self.inputbox_nombre)
        self.layout_botones.addWidget(self.etiqueta_email, alignment=Qt.AlignLeft)
        self.layout_botones.addWidget(self.inputbox_email)
        self.layout_botones.addWidget(self.etiqueta_edad, alignment=Qt.AlignLeft)
        self.layout_botones.addWidget(self.inputbox_edad)
        self.layout_botones.addWidget(self.boton_agregar_usuario,alignment=Qt.AlignCenter)

        #AGREGAR WIDGETS ELIMINAR USUARIO A LAYOUT
        self.layout_botones.addWidget(self.etiqueta_eliminar_usuario)
        self.layout_botones.addWidget(self.inputbox_id_eliminar)
        self.layout_botones.addWidget(self.boton_eliminar_usuario,alignment=Qt.AlignCenter)

        grupo_botones_principales=QGroupBox()
        grupo_botones_principales.setStyleSheet("""border: 2px solid #8FF2EC;
                                                    border-radius: 16px;
                                                    padding: 16px;""")
        grupo_botones_principales.setLayout(self.layout_botones)
        layout_principal=QVBoxLayout()
        layout_principal.addWidget(grupo_botones_principales)

        #DEFINIR CONTENEDORES DE WIDGETS
        contenedor_lienso.setLayout(layout_lienso)
        contenedor_botones.setLayout(layout_principal)

        self.layout_botones.addWidget(self.boton_finalizar_conexion,alignment=Qt.AlignCenter)

        self.splitter=QSplitter(Qt.Horizontal)
        self.splitter.addWidget(contenedor_lienso)
        self.splitter.addWidget(contenedor_botones)
        self.setCentralWidget(self.splitter)

        self.splitter.setSizes([600,200])

        self.statusBar().showMessage(f"Gestor en funcionamiento")
        return self.splitter

    def gestionar_boton_agregar_usuario(self):
        contenedor_lienso=QWidget()
        layout_lienso=QVBoxLayout()
        layout_lienso.setAlignment(Qt.AlignCenter)

        self.lienso=QTextEdit()
        self.lienso.setReadOnly(True)
        self.lienso.setText(self.resultado_consultar_usuario)

        layout_lienso.addWidget(self.lienso)
        contenedor_lienso.setLayout(layout_lienso)

        contenedor_boton_usuario=QWidget()
        layout=QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.etiqueta_nombre=QLabel("Nombre:")
        self.etiqueta_nombre.setStyleSheet("border: None;")
        self.inputbox_nombre=QLineEdit()
        self.etiqueta_email=QLabel("Email:")
        self.etiqueta_email.setStyleSheet("border: None;")
        self.inputbox_email=QLineEdit()
        self.etiqueta_edad=QLabel("Edad:")
        self.etiqueta_edad.setStyleSheet("border: None;")
        self.inputbox_edad=QLineEdit()

        self.boton_agregar_usuario=QPushButton("AGREGAR USUARIO")
        self.boton_agregar_usuario.clicked.connect(self.insertar_usuario)

        boton_volver=QPushButton("Volver")
        boton_volver.clicked.connect(self.crear_interfaz)

        layout.addWidget(self.etiqueta_nombre)
        layout.addWidget(self.inputbox_nombre)
        layout.addWidget(self.etiqueta_email)
        layout.addWidget(self.inputbox_email)
        layout.addWidget(self.etiqueta_edad)
        layout.addWidget(self.inputbox_edad)
        layout.addWidget(self.boton_agregar_usuario,alignment=Qt.AlignCenter)
        layout.addWidget(boton_volver,alignment=Qt.AlignCenter)

        contenedor_boton_usuario.setLayout(layout)
        self.splitter=QSplitter(Qt.Horizontal)

        self.splitter.addWidget(contenedor_lienso)
        self.splitter.addWidget(contenedor_boton_usuario)

        self.splitter.setSizes([600,200])
        
        self.setCentralWidget(self.splitter)
        return self.splitter,self.resultado_consultar_usuario

    def gestionar_boton_buscar_usuario_por_mail(self):
        contenedor_lienso=QWidget()
        layout_lienso=QVBoxLayout()
        layout_lienso.setAlignment(Qt.AlignCenter)

        self.lienso=QTextEdit()
        self.lienso.setReadOnly(True)
        self.lienso.setText(self.resultado_consultar_usuario)

        layout_lienso.addWidget(self.lienso)
        contenedor_lienso.setLayout(layout_lienso)
        
        contenedor_boton_buscar_usuario_por_mail=QWidget()
        layout=QVBoxLayout()

        self.etiqueta_busqueda_mail=QLabel("Buscar por mail:")
        self.etiqueta_busqueda_mail.setStyleSheet("border: None;")
        self.busqueda_mail=QLineEdit()

        self.boton_buscar_por_mail=QPushButton("BUSCAR POR MAIL")
        self.boton_buscar_por_mail.clicked.connect(lambda: self.buscar_usuario_por_email())
        boton_volver=QPushButton("Volver")
        boton_volver.clicked.connect(self.crear_interfaz)

        layout.addWidget(self.etiqueta_busqueda_mail)
        layout.addWidget(self.busqueda_mail)
        layout.addWidget(self.boton_buscar_por_mail,alignment=Qt.AlignCenter)
        layout.addWidget(boton_volver,alignment=Qt.AlignCenter)
        contenedor_boton_buscar_usuario_por_mail.setLayout(layout)

        self.splitter=QSplitter(Qt.Horizontal)
        self.splitter.addWidget(contenedor_lienso)
        self.splitter.addWidget(contenedor_boton_buscar_usuario_por_mail)

        self.splitter.setSizes([600,200])

        self.setCentralWidget(self.splitter)
        return self.splitter,self.resultado_consultar_usuario

    def gestionar_boton_eliminar_usuario(self):
        contenedor_lienso=QWidget()
        layout_lienso=QVBoxLayout()
        layout_lienso.setAlignment(Qt.AlignCenter)

        self.lienso=QTextEdit()
        self.lienso.setReadOnly(True)
        self.lienso.setText(self.resultado_consultar_usuario)

        layout_lienso.addWidget(self.lienso)
        contenedor_lienso.setLayout(layout_lienso)

        self.contenedor_boton_eliminar_usuario=QWidget()
        layout=QVBoxLayout()

        self.etiqueta_eliminar_usuario=QLabel("Ingresar ID para eliminar")
        self.etiqueta_eliminar_usuario.setStyleSheet("border: None;")
        self.inputbox_id_eliminar=QLineEdit()

        boton_volver=QPushButton("Volver")
        boton_volver.clicked.connect(self.crear_interfaz)

        self.boton_eliminar_usuario=QPushButton("ELIMINAR USUARIO")
        self.boton_eliminar_usuario.clicked.connect(self.eliminar_usuario)

        layout.addWidget(self.etiqueta_eliminar_usuario)
        layout.addWidget(self.inputbox_id_eliminar)
        layout.addWidget(self.boton_eliminar_usuario,alignment=Qt.AlignCenter)
        layout.addWidget(boton_volver,alignment=Qt.AlignCenter)
        self.contenedor_boton_eliminar_usuario.setLayout(layout)

        self.splitter=QSplitter(Qt.Horizontal)
        self.splitter.addWidget(contenedor_lienso)
        
        self.splitter.addWidget(self.contenedor_boton_eliminar_usuario)

        self.splitter.setSizes([600,200])

        self.setCentralWidget(self.splitter)

        return self.splitter,self.resultado_consultar_usuario
        
    def avanzar_paginas(self):
        try:
            # Si se presiona el boton "Avanzar" por primera vez, hara que se muestre el primer registro del 1 hasta el limite"
            if self.flag==True: #Bucle de una sola vez, luego no se usa mas
                while self.flag==True:
                    consulta=f"SELECT * FROM usuarios ORDER BY id LIMIT {self.limite_paginas} OFFSET {self.paginas_salteadas};"
                    self.consultar_usuarios(consulta)
                    self.statusBar().showMessage(f"Página: {self.indice_pagina}")
                    self.flag=False
            # En caso de que ya se haya presionado "Avanzar" por primera vez, se empezara a ejecutar este codigo cada vez que se presione "Avanzar"
            else:
                self.paginas_salteadas += self.limite_paginas
                self.indice_pagina += 1

                consulta=f"SELECT * FROM usuarios ORDER BY id LIMIT {self.limite_paginas} OFFSET {self.paginas_salteadas};"     
                self.consultar_usuarios(consulta)
                self.statusBar().showMessage(f"Página: {self.indice_pagina}")
        except Error as e:
            self.resultado_avanzar_paginas=f"Error al consultar usuarios: {e}"
            return None

    def retroceder_paginas(self):
        self.flag=False # MOSTRAR ESTO A BRUNITO
        try:
            if self.indice_pagina <= 1:
                self.indice_pagina = 1
                self.paginas_salteadas = 0
            else:    
                self.paginas_salteadas -= self.limite_paginas
                self.indice_pagina -= 1

            consulta=f"SELECT * FROM usuarios ORDER BY id LIMIT {self.limite_paginas} OFFSET {self.paginas_salteadas};"
            self.consultar_usuarios(consulta)
            self.statusBar().showMessage(f"Página: {self.indice_pagina}")

        except Error as e:
            self.resultado_retroceder_paginas=f"Error al consultar usuarios: {e}"
            return None

    def conectar_mysql(self):
        try:
            conexion=mysql.connector.connect(
                host='localhost',
                database='EjemploBD',
                user='root',
                password='root'
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

        self.etiqueta_nombre.show()
        self.etiqueta_email.show()
        self.etiqueta_edad.show()

        self.inputbox_nombre.show()
        self.inputbox_email.show()
        self.inputbox_edad.show()

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

        self.etiqueta_eliminar_usuario.show()
        self.inputbox_id_eliminar.show()

        id=self.inputbox_id_eliminar.text().strip()

        if not id:
            QMessageBox.warning(self, "Error", "No deje campos vacios")
        else:
            try:
                cursor=conexion.cursor()

                consulta="DELETE FROM usuarios WHERE id=%s;"

                cursor.execute(consulta, (id,))

                conexion.commit()
            
                self.resultado_eliminar_usuario=f"Eliminacion sastifactoria"
                QMessageBox.information(self, "Exito", self.resultado_eliminar_usuario)
                
            except Error as e:
                self.resultado_eliminar_usuario=f"Error al eliminar usuario: {e}"
                QMessageBox.warning(self, "Error", self.resultado_eliminar_usuario)

            finally:
                if conexion.is_connected():
                    conexion.close()

    def consultar_toda_la_tabla(self):
        #reinicio de posiciones para retroceder y avanzar, cada vez que se utiliza funcion consultar_toda_la_tabla()
        self.paginas_salteadas=0
        self.limite_paginas=10
        self.indice_pagina=1
        #Sentencia consultar todos los campos de la tabla usuarios
        consulta=f"SELECT * FROM usuarios;"
        self.consultar_usuarios(consulta)

    def consultar_usuarios(self, consulta):     
        conexion = self.conectar_mysql()
        self.boton_avanzar.show()
        self.boton_retroceder.show()
        try:
            cursor=conexion.cursor()
            cursor.execute(consulta)
            usuarios=cursor.fetchall()

            self.resultado_consultar_usuario="Lista de usuarios:\n"
            self.resultado_consultar_usuario +="-" * 80 + '\n'
            self.resultado_consultar_usuario +=f"{'ID':<5} {'Nombre':<20} {'Email':<30} {'Edad':<5} {'Fecha de creación'}\n"
            self.resultado_consultar_usuario +="-" * 80 + '\n'

            for usuario in usuarios:
                id_usuario,nombre,email,edad,fecha=usuario
                self.resultado_consultar_usuario += f"\n{id_usuario:<5} {nombre:<20} {email:<30} {edad or 'N/A':<5} {fecha}\n"
            #self.resultado_consultar_usuario += f"\nTotal de usuarios: {len(usuarios)}"
            self.lienso.setText(self.resultado_consultar_usuario)
            self.statusBar().showMessage(f"\nTotal de usuarios: {len(usuarios)}")
           
        except Error as e:
            self.resultado_consultar_usuario=f"Error al consultar usuarios: {e}"
            return None

    def buscar_usuario_por_email(self):
        conexion = self.conectar_mysql()
        self.etiqueta_busqueda_mail.show()
        self.busqueda_mail.show()
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

                #self.insertar_usuario(conexion,2,"Juan Pérez","juan.perez@email.com",25)
                #self.insertar_usuario(conexion,2,"María González","maria.gonzalez@email.com",30)
                #self.insertar_usuario(conexion,2,"Carlos Rodríguez","carlos.rodriguez@email.com",25)

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
    