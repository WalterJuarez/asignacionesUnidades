import sys
import os
import win32com.client as win32
import ctypes

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableWidgetItem, QLineEdit,
    QCompleter, QComboBox, QMessageBox, QProgressDialog
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QCoreApplication, QDate, QTimer, QThread, Signal
from datetime import datetime

# ─── Importar clases generadas por pyside6-uic ───────────────────────────────
# Los 3 .ui tienen class="MainWindow", por eso se  generan  3 Ui_MainWindow.
# Se importan con alias distintos para evitar colisión
from ui.login_ui import Ui_MainWindow as Ui_Login
from ui.PLC_DieselVillaNueva_ui import Ui_MainWindow as Ui_Sistema
from ui.credenciales_ui import Ui_MainWindow as Ui_Credenciales

from services.pilotos import (
    obtener_pilotos, buscar_pilotos_por_codigo, existe_piloto, crear_piloto
)
from services.unidades import (
    obtener_unidades, buscar_unidades_por_codigo,
    obtener_canales, obtener_consecutivo_canal, existe_unidad, crear_unidad
)
from services.asignacionUnidad import (
    obtener_asignacionUnidad, obtener_unidadAsig, obtener_codigoPiloto,
    obtener_nombrePiloto, obtener_consecutivoUnidad, crear_asignacionUnidad,
    buscarAsigUnidadName, buscar_asigUnidad_por_codigo
)
from services.canalDistri import (
    obtener_canalDistribucion, existe_canal, crear_canalDistribucion
)
from services.reportes import obtener_despachos
from services.usuarios import validar_usuario
from services.cambioCreden import actualizarUsuario
from PySide6.QtWidgets import QFileDialog

def ruta_recurso(nombre):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, nombre)

    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        nombre
    )

# ─── Worker para consultas en segundo plano ──────────────────────────────────
class WorkerConsulta(QThread):
    resultado = Signal(list)

    def __init__(self, funcion, *args):
        super().__init__()
        self.funcion = funcion
        self.args = args

    def run(self):
        try:
            datos = self.funcion(*self.args)
            self.resultado.emit(datos)
        except Exception as e:
            print(f"Error en hilo: {e}")
            self.resultado.emit([])

# ─── Ventana de Credenciales ─────────────────────────────────────────────────
class VentanaCredenciales(QMainWindow, Ui_Credenciales):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon(ruta_recurso("zico.ico")))

# ─── Ventana principal ───────────────────────────────────────────────────────
class Sistema(QMainWindow, Ui_Sistema):

    def __init__(self):
        super().__init__()
        self.setupUi(self)          # monta todos los widgets en self
        self.setWindowIcon(QIcon(ruta_recurso("zico.ico"))) ## icono
        self._workers = []

        self.dt_desde.setDate(QDate.currentDate())
        self.dt_hasta.setDate(QDate.currentDate())

        # PILOTOS
        self.cargar_pilotos()
        self.txt_buscarCodigo.textChanged.connect(self.buscar_pilotos)
        self.btn_crearPiloto.clicked.connect(self.crear_piloto)

        # UNIDADES
        self.cargar_unidades()
        self.cargar_canales()
        self.txt_buscarCodigoUnidad.textChanged.connect(self.buscar_unidades)
        self.btn_crearUnidad.clicked.connect(self.crear_unidad)

        # ASIGNACION
        self.cargar_unidadAsig()
        self.cargar_codigoPiloto()
        self.cb_codigoEmpleado.currentTextChanged.connect(self.mostrar_nombrePiloto)
        self.btn_crearAsigUnidad.clicked.connect(self.crear_asignacionUnidad)

        # CANAL DISTRIBUCION
        self.cargar_canalDistribucion()
        self.btn_crearCanal.clicked.connect(self.crear_canalDistribucion)

        # REPORTES
        self.btn_generarReporte.clicked.connect(self.ver_reporte)
        self.btn_generarExcel.clicked.connect(self.exportar_despachosExcel)
        self.txt_buscarDespachoUnidad.textChanged.connect(self.buscar_despachoUnidad)
        self.btn_excelUnidad.clicked.connect(self.exportar_despachoUnidadExcel)

        # CREDENCIALES
        self.btn_cambiarCreden.clicked.connect(self.updateCredenciales)

        # Datos de reporte
        self.columnas_reporte = []
        self.datos_reporte = []
        self.datos_filtrados_reporte = []

        # CONFIG TABLA ASIGNACION
        tabla = self.table_mostrarAsigUnidades
        tabla.setColumnCount(5)
        tabla.setHorizontalHeaderLabels([
            "COD EMPLEADO", "PILOTO / RESPONSABLE",
            "UNIDAD", "CANAL DISTRIBUCION", "FECHA ASIGNACION"
        ])
        tabla.setColumnWidth(0, 150)
        tabla.setColumnWidth(1, 390)
        tabla.setColumnWidth(2, 140)
        tabla.setColumnWidth(3, 200)
        tabla.setColumnWidth(4, 190)

        # Timer búsqueda asignación
        self.timer_busqueda_asignacion = QTimer(self)
        self.timer_busqueda_asignacion.setSingleShot(True)
        self.timer_busqueda_asignacion.setInterval(300)
        self.txt_buscarAsigUnidad.textChanged.connect(self.programar_busqueda_asignacion)
        self.timer_busqueda_asignacion.timeout.connect(self.buscar_asignacion)
        self.cargar_asignacionUnidades()

        # Convertir campos a mayúsculas (excepto passwords)
        for campo in self.findChildren(QLineEdit):
            if campo.echoMode() != QLineEdit.Password:
                campo.textChanged.connect(
                    lambda texto, c=campo: self.convertir_mayusculas(c, texto)
                )

    def convertir_mayusculas(self, campo, texto):
        texto_mayuscula = texto.upper()
        if texto == texto_mayuscula:
            return
        posicion = campo.cursorPosition()
        campo.blockSignals(True)
        campo.setText(texto_mayuscula)
        campo.setCursorPosition(posicion)
        campo.blockSignals(False)

    # ── PILOTOS ──────────────────────────────────────────────────────────────
    def cargar_pilotos(self):
        datos = obtener_pilotos()
        self.mostrar_pilotos(datos)

    def mostrar_pilotos(self, datos):
        tabla = self.table_mostrarPilotos
        tabla.setUpdatesEnabled(False)
        tabla.clearContents()
        tabla.setColumnCount(3)
        tabla.setHorizontalHeaderLabels([
            "CODIGO EMPLEADO", "PILOTO", "FECHA DE CREACION"
        ])
        tabla.setColumnWidth(0, 250)
        tabla.setColumnWidth(1, 430)
        tabla.setColumnWidth(2, 320)
        tabla.setRowCount(len(datos))
        for fila, piloto in enumerate(datos):
            for columna, valor in enumerate(piloto):
                tabla.setItem(fila, columna, QTableWidgetItem(str(valor)))
        tabla.setUpdatesEnabled(True)

    def buscar_pilotos(self):
        codigo = self.txt_buscarCodigo.text().strip()
        if codigo == "":
            self.cargar_pilotos()
            return
        datos = buscar_pilotos_por_codigo(codigo)
        self.mostrar_pilotos(datos)

    def crear_piloto(self):
        codigo = self.txt_codigoEmpleado.text().strip()
        nombre = self.txt_nombrePiloto.text().strip()
        if codigo == "" or nombre == "":
            QMessageBox.information(self, "Pilotos", "Los campos no pueden estar vacios.", QMessageBox.Ok)
            return
        piloto_existente = existe_piloto(codigo)
        if piloto_existente:
            QMessageBox.information(
                self, "Pilotos",
                f"El codigo de empleado {codigo} ya esta registrado con el piloto {piloto_existente[1]}.",
                QMessageBox.Ok
            )
            self.txt_codigoEmpleado.clear()
            self.txt_nombrePiloto.clear()
            return
        respuesta = QMessageBox.question(
            self, "Confirmacion",
            f"Esta seguro que desea crear el piloto {nombre}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            try:
                crear_piloto(codigo, nombre)
                QMessageBox.information(self, "Pilotos", "Piloto creado.", QMessageBox.Ok)
                self.txt_codigoEmpleado.clear()
                self.txt_nombrePiloto.clear()
                self.cargar_pilotos()
                self.cargar_codigoPiloto()
            except Exception as error:
                QMessageBox.information(self, "Pilotos", "Error al crear piloto, verifique datos.", QMessageBox.Ok)
                print(f"Error al insertar datos de piloto: {error}")

    # ── UNIDADES ─────────────────────────────────────────────────────────────
    def cargar_unidades(self):
        datos = obtener_unidades()
        self.mostrar_unidades(datos)

    def mostrar_unidades(self, datos):
        tabla = self.table_mostrarUnidades
        tabla.setColumnCount(3)
        tabla.setHorizontalHeaderLabels([
            "UNIDAD / PLACA", "CANAL DE DISTRIBUCION", "FECHA DE CREACION"
        ])
        tabla.setColumnWidth(0, 270)
        tabla.setColumnWidth(1, 430)
        tabla.setColumnWidth(2, 310)
        tabla.setRowCount(len(datos))
        for fila, unidad in enumerate(datos):
            for columna, valor in enumerate(unidad):
                tabla.setItem(fila, columna, QTableWidgetItem(str(valor)))

    def buscar_unidades(self):
        codigo = self.txt_buscarCodigoUnidad.text().strip()
        if codigo == "":
            self.cargar_unidades()
            return
        datos = buscar_unidades_por_codigo(codigo)
        self.mostrar_unidades(datos)

    def cargar_canales(self):
        datos = obtener_canales()
        self.cb_canalDistribucion.clear()
        self.cb_canalDistribucion.addItem("")
        for canal in datos:
            self.cb_canalDistribucion.addItem(canal[0])

    def crear_unidad(self):
        unidad = self.txt_noUnidad.text().strip()
        canal = self.cb_canalDistribucion.currentText().strip()
        if unidad == "" or canal == "":
            QMessageBox.information(self, "Unidades", "Los campos no pueden estar vacios.", QMessageBox.Ok)
            return
        unidad_existente = existe_unidad(unidad)
        if unidad_existente:
            QMessageBox.information(
                self, "Unidades",
                f"El numero de unidad {unidad} ya esta registrado en el canal de distribucion {unidad_existente[1]}.",
                QMessageBox.Ok
            )
            self.txt_noUnidad.clear()
            self.cb_canalDistribucion.setCurrentIndex(0)
            return
        respuesta = QMessageBox.question(
            self, "Confirmacion",
            f"Esta seguro que desea crear la unidad {unidad}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            try:
                consecutivo_canal = obtener_consecutivo_canal(canal)
                if consecutivo_canal is None:
                    QMessageBox.information(self, "Unidades", "No se encontro el canal seleccionado.", QMessageBox.Ok)
                    return
                crear_unidad(unidad, consecutivo_canal)
                QMessageBox.information(self, "Unidades", "Unidad creada.", QMessageBox.Ok)
                self.txt_noUnidad.clear()
                self.cb_canalDistribucion.setCurrentIndex(0)
                self.cargar_unidades()
                self.cargar_unidadAsig()
            except Exception as error:
                QMessageBox.information(self, "Unidades", "Error al crear unidad, verifique datos.", QMessageBox.Ok)
                print(f"Error al insertar datos de unidad: {error}")

    # ── ASIGNACION DE UNIDAD ─────────────────────────────────────────────────
    def cargar_asignacionUnidades(self):
        datos = obtener_asignacionUnidad()
        self.mostrar_asignacionUnidades(datos)

    def mostrar_asignacionUnidades(self, datos):
        tabla = self.table_mostrarAsigUnidades
        tabla.setUpdatesEnabled(False)
        tabla.clearContents()
        tabla.setRowCount(len(datos))
        try:
            for fila, registro in enumerate(datos):
                for columna, valor in enumerate(registro):
                    tabla.setItem(
                        fila, columna,
                        QTableWidgetItem("" if valor is None else str(valor))
                    )
        finally:
            tabla.setUpdatesEnabled(True)

    def programar_busqueda_asignacion(self):
        self.timer_busqueda_asignacion.start()

    def buscar_asignacion(self):
        texto = self.txt_buscarAsigUnidad.text().strip()
        for worker in self._workers:
            try:
                worker.resultado.disconnect()
            except Exception:
                pass
        if texto == "":
            funcion, args = obtener_asignacionUnidad, ()
        elif texto.isdigit():
            funcion, args = buscar_asigUnidad_por_codigo, (texto,)
        else:
            funcion, args = buscarAsigUnidadName, (texto,)
        worker = WorkerConsulta(funcion, *args)
        worker.resultado.connect(self.mostrar_asignacionUnidades)
        worker.finished.connect(lambda: self._workers.remove(worker) if worker in self._workers else None)
        self._workers.append(worker)
        worker.start()

    def cargar_unidadAsig(self):
        datos = obtener_unidadAsig()
        combo = self.cb_unidadAsignar
        combo.clear()
        combo.addItem("")
        for unidad in datos:
            combo.addItem(str(unidad[0]))
        combo.setEditable(True)
        combo.setInsertPolicy(QComboBox.NoInsert)
        self.completer_unidad = QCompleter(combo.model(), combo)
        self.completer_unidad.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer_unidad.setFilterMode(Qt.MatchFlag.MatchContains)
        self.completer_unidad.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        combo.setCompleter(self.completer_unidad)

    def cargar_codigoPiloto(self):
        datos = obtener_codigoPiloto()
        combo = self.cb_codigoEmpleado
        combo.clear()
        combo.addItem("")
        for codigo in datos:
            combo.addItem(str(codigo[0]))
        combo.setEditable(True)
        combo.setInsertPolicy(QComboBox.NoInsert)
        self.completer_piloto = QCompleter(combo.model(), combo)
        self.completer_piloto.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer_piloto.setFilterMode(Qt.MatchFlag.MatchContains)
        self.completer_piloto.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        combo.setCompleter(self.completer_piloto)

    def mostrar_nombrePiloto(self):
        codigo = self.cb_codigoEmpleado.currentText().strip()
        if codigo == "":
            self.lbl_nombrePiloto.setText("")
            return
        nombre = obtener_nombrePiloto(codigo)
        self.lbl_nombrePiloto.setText(nombre)

    def crear_asignacionUnidad(self):
        codigo = self.cb_codigoEmpleado.currentText().strip()
        unidad = self.cb_unidadAsignar.currentText().strip()
        if codigo == "" or unidad == "":
            QMessageBox.information(self, "Asignacion de Unidades", "Los campos no pueden estar vacios.", QMessageBox.Ok)
            return
        respuesta = QMessageBox.question(
            self, "Confirmacion",
            f"Esta seguro que desea asignar la unidad {unidad}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            try:
                consecutivo_unidad = obtener_consecutivoUnidad(unidad)
                if consecutivo_unidad is None:
                    QMessageBox.information(self, "Asignacion de Unidades", "No se encontro la unidad seleccionada.", QMessageBox.Ok)
                    return
                usuario = str(self.usuario_actual[2])
                crear_asignacionUnidad(codigo, consecutivo_unidad, usuario)
                QMessageBox.information(self, "Asignacion de Unidades", "Asignacion creada.", QMessageBox.Ok)
                self.cb_codigoEmpleado.setCurrentIndex(0)
                self.cb_unidadAsignar.setCurrentIndex(0)
                self.lbl_nombrePiloto.setText("")
                self.cargar_asignacionUnidades()
            except Exception as error:
                QMessageBox.information(self, "Asignacion de Unidades", "Error al crear asignacion, verifique datos.", QMessageBox.Ok)
                print(f"Error al crear asignacion: {error}")

    # ── CANAL DE DISTRIBUCION ────────────────────────────────────────────────
    def cargar_canalDistribucion(self):
        datos = obtener_canalDistribucion()
        self.mostrar_canalDistribucion(datos)

    def mostrar_canalDistribucion(self, datos):
        tabla = self.table_mostrarCanal
        tabla.setColumnCount(4)
        tabla.setHorizontalHeaderLabels([
            "No. REGISTRO", "CANAL DE DISTRIBUCION", "DESCRIPCION", "FECHA DE CREACION"
        ])
        tabla.setColumnWidth(0, 180)
        tabla.setColumnWidth(1, 300)
        tabla.setColumnWidth(2, 300)
        tabla.setColumnWidth(3, 190)
        tabla.setRowCount(len(datos))
        for fila, piloto in enumerate(datos):
            for columna, valor in enumerate(piloto):
                tabla.setItem(fila, columna, QTableWidgetItem(str(valor)))

    def crear_canalDistribucion(self):
        canal = self.txt_canalDistribucion.text().strip()
        descripcion = self.txt_descripcionCanal.text().strip()
        try:
            if canal != "" and descripcion != "":
                canal_existente = existe_canal(canal)
                if canal_existente:
                    QMessageBox.information(
                        self, "Canales de distribucion",
                        f"El canal de distribucion {canal} ya se encuentra registrado con el No. de Registro {canal_existente[0]}.",
                        QMessageBox.Ok
                    )
                    self.txt_canalDistribucion.clear()
                    self.txt_descripcionCanal.clear()
                    return
                respuesta = QMessageBox.question(
                    self, "Confirmacion",
                    f"Esta seguro que desea crear el canal de distribucion {canal}?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                if respuesta == QMessageBox.Yes:
                    crear_canalDistribucion(canal, descripcion)
                    QMessageBox.information(self, "Canales de distribucion", "Canal de distribucion creado.", QMessageBox.Ok)
                    self.txt_canalDistribucion.clear()
                    self.txt_descripcionCanal.clear()
                    self.cargar_canalDistribucion()
                    self.cargar_canales()
            elif canal == "" or descripcion == "":
                QMessageBox.information(self, "Canales de distribucion", "Los campos no pueden estar vacios.", QMessageBox.Ok)
        except Exception as error:
            QMessageBox.information(self, "Canales de distribucion", "Error al crear canal de distribucion, verifique datos.", QMessageBox.Ok)
            print(f"Error al insertar datos de canal: {error}")

    # ── REPORTES ─────────────────────────────────────────────────────────────
    def mostrar_carga(self, mensaje="Generando reporte, ESPERE..."):
        progreso = QProgressDialog(mensaje, None, 0, 0, self)
        progreso.setWindowTitle("Procesando")
        progreso.setWindowModality(Qt.WindowModal)
        progreso.setCancelButton(None)
        progreso.setMinimumDuration(0)
        progreso.setAutoClose(False)
        progreso.show()
        QApplication.processEvents()
        return progreso

    def ver_reporte(self):
        progreso = self.mostrar_carga("Generando reporte, ESPERE...")
        try:
            fecha_inicio = self.dt_desde.date().toString("yyyy-MM-dd")
            fecha_fin = self.dt_hasta.date().toString("yyyy-MM-dd")
            self.columnas_reporte, self.datos_reporte = obtener_despachos(fecha_inicio, fecha_fin)
            self.datos_filtrados_reporte = self.datos_reporte
            self.mostrar_reporte(self.columnas_reporte, self.datos_reporte[:500])
        finally:
            progreso.close()
            QApplication.processEvents()
        if self.datos_reporte:
            QMessageBox.information(self, "Reporte", f"Reporte generado con éxito.\nSe encontraron {len(self.datos_reporte)} registros.")
        else:
            QMessageBox.information(self, "Reporte", "No se encontraron registros en las fechas seleccionadas.")

    def valor_decimal(self, valor):
        if isinstance(valor, float) and valor.is_integer():
            return str(int(valor))
        return str(valor)

    def mostrar_reporte(self, columnas, datos):
        tabla = self.table_mostrarDespachosD
        encabezados = [
            "NO.\nDESPACHO", "UNIDAD", "PILOTO /\nRESPONSABLE",
            "GALONES\nDESPACHADOS", "TOTAL\nDESPACHADO", "FECHA\nDESPACHO",
            "CODIGO\nEMPLEADO", "KILOMETRAJE\nACTUAL", "KILOMETRAJE\nANTERIOR", "DIFERENCIA"
        ]
        tabla.setUpdatesEnabled(False)
        tabla.setSortingEnabled(False)
        try:
            tabla.clearContents()
            tabla.setColumnCount(len(encabezados))
            tabla.setHorizontalHeaderLabels(encabezados)
            tabla.setRowCount(len(datos))
            for fila, registro in enumerate(datos):
                for columna, valor in enumerate(registro):
                    tabla.setItem(fila, columna, QTableWidgetItem(self.valor_decimal(valor)))
        finally:
            tabla.setUpdatesEnabled(True)

    def valor_excel(self, valor):
        if isinstance(valor, float) and valor.is_integer():
            return int(valor)
        return valor

    def limpiar_tablaDespacho(self):
        self.table_mostrarDespachosD.clearContents()
        self.table_mostrarDespachosD.setRowCount(0)

    def exportar_despachosExcel(self):
        progreso = self.mostrar_carga("Consultando datos, ESPERE...")
        excel = None
        try:
            fecha_inicio = self.dt_desde.date().toString("yyyy-MM-dd")
            fecha_fin = self.dt_hasta.date().toString("yyyy-MM-dd")
            columnas, datos = obtener_despachos(fecha_inicio, fecha_fin)
            if not datos:
                QMessageBox.information(self, "Reporte", "No hay datos para exportar.")
                return
            progreso.setLabelText("Generando Excel, ESPERE...")
            QApplication.processEvents()
            excel = win32.Dispatch("Excel.Application")
            excel.Visible = False
            excel.ScreenUpdating = False
            excel.DisplayAlerts = False
            libro = excel.Workbooks.Add()
            hoja = libro.Worksheets(1)
            hoja.Name = "Despachos"
            hoja.Range("A1:J1").Merge()
            hoja.Range("A2:J2").Merge()
            hoja.Range("A3:J3").Merge()
            hoja.Range("A4:J4").Merge()
            hoja.Cells(1, 1).Value = "ZETA GAS DE GUATEMALA, S.A. DE C.V."
            hoja.Cells(2, 1).Value = "VILLA NUEVA - DIESEL"
            hoja.Cells(3, 1).Value = "Reporte General de Despachos"
            hoja.Cells(4, 1).NumberFormat = "@"
            hoja.Cells(4, 1).Value = "Reporte Generado: " + datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            hoja.Range("A1:J4").Font.Bold = True
            hoja.Range("A1:J4").Font.Color = 16711680
            hoja.Range("A1:J4").Font.Size = 15
            hoja.Range("A1:J4").HorizontalAlignment = -4108
            encabezados = [
                "No. DESPACHO", "UNIDAD", "PILOTO / RESPONSABLE",
                "GALONES DESPACHADOS", "TOTAL DESPACHADO", "FECHA DESPACHO",
                "COD EMPLEADO", "KILOMETRAJE ACTUAL", "KILOMETRAJE ANTERIOR", "DIFERENCIA"
            ]
            hoja.Range("A5:J5").Value = [encabezados]
            hoja.Range("A5:J5").Font.Bold = True
            hoja.Range("A5:J5").Font.Size = 13
            hoja.Range("A5:J5").HorizontalAlignment = -4108
            datos_excel = []
            for registro in datos:
                fila = list(registro)
                fila[5] = str(fila[5])
                fila = [self.valor_excel(v) for v in fila]
                datos_excel.append(tuple(fila))
            fila_final = 5 + len(datos_excel)
            hoja.Range(hoja.Cells(6, 6), hoja.Cells(fila_final, 6)).NumberFormat = "@"
            hoja.Range(hoja.Cells(6, 1), hoja.Cells(fila_final, 10)).Value = tuple(datos_excel)
            hoja.Range(hoja.Cells(5, 1), hoja.Cells(fila_final, 10)).Borders.LineStyle = 1
            hoja.Columns.AutoFit()
            excel.ScreenUpdating = True
            excel.DisplayAlerts = True
            excel.Visible = True
            excel.UserControl = True
            self.limpiar_tablaDespacho()
            progreso.close()
            QApplication.processEvents()
            QMessageBox.information(self, "Excel", "Reporte generado correctamente.")
        except Exception as error:
            print(f"Error al generar Excel: {error}")
            if excel is not None:
                excel.ScreenUpdating = True
                excel.DisplayAlerts = True
                excel.Visible = True
            QMessageBox.warning(self, "Excel", "No se pudo generar el reporte.")
        finally:
            progreso.close()
            QApplication.processEvents()

    def buscar_despachoUnidad(self):
        unidad = self.txt_buscarDespachoUnidad.text().strip().upper()
        if not self.datos_reporte:
            return
        if unidad == "":
            self.datos_filtrados_reporte = self.datos_reporte
        else:
            self.datos_filtrados_reporte = [
                r for r in self.datos_reporte
                if str(r[1]).upper().startswith(unidad)
            ]
        self.mostrar_reporte(self.columnas_reporte, self.datos_filtrados_reporte[:500])

    def exportar_despachoUnidadExcel(self):
        datos = self.datos_filtrados_reporte
        if not datos:
            QMessageBox.information(self, "Reporte", "No hay datos para exportar.")
            return
        progreso = self.mostrar_carga("Generando Excel por unidad, ESPERE...")
        excel = None
        try:
            excel = win32.Dispatch("Excel.Application")
            excel.Visible = False
            excel.ScreenUpdating = False
            excel.DisplayAlerts = False
            libro = excel.Workbooks.Add()
            hoja = libro.Worksheets(1)
            hoja.Name = "Despachos por Unidad"
            hoja.Range("A1:J1").Merge()
            hoja.Range("A2:J2").Merge()
            hoja.Range("A3:J3").Merge()
            hoja.Range("A4:J4").Merge()
            hoja.Cells(1, 1).Value = "ZETA GAS DE GUATEMALA, S.A. DE C.V."
            hoja.Cells(2, 1).Value = "VILLA NUEVA - DIESEL"
            hoja.Cells(3, 1).Value = "Despachos por unidad"
            hoja.Cells(4, 1).NumberFormat = "@"
            hoja.Cells(4, 1).Value = "Reporte Generado: " + datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            hoja.Range("A1:J4").Font.Bold = True
            hoja.Range("A1:J4").Font.Color = 16711680
            hoja.Range("A1:J4").Font.Size = 15
            hoja.Range("A1:J4").HorizontalAlignment = -4108
            encabezados = [
                "No. DESPACHO", "UNIDAD", "PILOTO / RESPONSABLE",
                "GALONES DESPACHADOS", "TOTAL DESPACHADO", "FECHA DESPACHO",
                "COD EMPLEADO", "KILOMETRAJE ACTUAL", "KILOMETRAJE ANTERIOR", "DIFERENCIA"
            ]
            hoja.Range("A5:J5").Value = [encabezados]
            hoja.Range("A5:J5").Font.Bold = True
            hoja.Range("A5:J5").Font.Size = 13
            hoja.Range("A5:J5").HorizontalAlignment = -4108
            datos_excel = []
            for registro in datos:
                fila = list(registro)
                fila[5] = str(fila[5])
                fila = [self.valor_excel(v) for v in fila]
                datos_excel.append(tuple(fila))
            fila_final = 5 + len(datos_excel)
            hoja.Range(hoja.Cells(6, 6), hoja.Cells(fila_final, 6)).NumberFormat = "@"
            hoja.Range(hoja.Cells(6, 1), hoja.Cells(fila_final, 10)).Value = tuple(datos_excel)
            hoja.Range(hoja.Cells(5, 1), hoja.Cells(fila_final, 10)).Borders.LineStyle = 1
            hoja.Columns.AutoFit()
            excel.ScreenUpdating = True
            excel.DisplayAlerts = True
            excel.Visible = True
            excel.UserControl = True
            self.txt_buscarDespachoUnidad.clear()
            progreso.close()
            QApplication.processEvents()
            QMessageBox.information(self, "Excel", f"Reporte generado correctamente.\nSe exportaron {len(datos)} registros.")
        except Exception as error:
            print(f"Error al generar Excel por unidad: {error}")
            if excel is not None:
                excel.ScreenUpdating = True
                excel.DisplayAlerts = True
                excel.Visible = True
            QMessageBox.warning(self, "Excel", "No se pudo generar el reporte.")
        finally:
            progreso.close()
            QApplication.processEvents()

    # ── CREDENCIALES ─────────────────────────────────────────────────────────
    def updateCredenciales(self):
        print("BOTÓN CREDENCIALES PRESIONADO")
        self.mainWinCredenciales = VentanaCredenciales(self)
        self.mainWinCredenciales.txt_nameUser.setText(str(self.usuario_actual[0]))
        self.mainWinCredenciales.txt_apellidoUser.setText(str(self.usuario_actual[1]))
        self.mainWinCredenciales.txt_user.setText(str(self.usuario_actual[2]))
        self.mainWinCredenciales.txt_passwordNew.setEchoMode(QLineEdit.Password)
        self.mainWinCredenciales.txt_passwordNew1.setEchoMode(QLineEdit.Password)
        self.mainWinCredenciales.btn_verPass.setText("👁")
        self.mainWinCredenciales.btn_verPass.clicked.connect(self.mostrar_ocultar_passwords)
        self.mainWinCredenciales.txt_nameUser.setFocus()
        self.mainWinCredenciales.btn_aceptarCreden.clicked.connect(self.guardarCredenciales)
        self.mainWinCredenciales.show()

    def mostrar_ocultar_passwords(self):

        password1 = self.mainWinCredenciales.txt_passwordNew
        password2 = self.mainWinCredenciales.txt_passwordNew1
        boton = self.mainWinCredenciales.btn_verPass
        ocultas = password1.echoMode() == QLineEdit.Password
        if ocultas:
            password1.setEchoMode(QLineEdit.Normal)
            password2.setEchoMode(QLineEdit.Normal)
            boton.setText("🙈")
        else:
            password1.setEchoMode(QLineEdit.Password)
            password2.setEchoMode(QLineEdit.Password)
            boton.setText("👁")

    def guardarCredenciales(self):
        nombre = self.mainWinCredenciales.txt_nameUser.text().strip()
        apellido = self.mainWinCredenciales.txt_apellidoUser.text().strip()
        usuario = self.mainWinCredenciales.txt_user.text().strip()
        contra = self.mainWinCredenciales.txt_passwordNew.text().strip()
        contra2 = self.mainWinCredenciales.txt_passwordNew1.text().strip()
        if nombre == "" or apellido == "" or usuario == "" or contra == "" or contra2 == "":
            QMessageBox.information(self.mainWinCredenciales, "Credenciales", "Los campos no pueden estar vacios.")
            return
        if contra != contra2:
            QMessageBox.warning(self.mainWinCredenciales, "Error en contraseña", "Las contraseñas ingresadas no coinciden.")
            self.mainWinCredenciales.txt_passwordNew.clear()
            self.mainWinCredenciales.txt_passwordNew1.clear()
            self.mainWinCredenciales.txt_passwordNew.setFocus()
            return
        respuesta = QMessageBox.question(
            self.mainWinCredenciales, "Confirmación",
            "¿Está seguro que desea guardar los cambios?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            usuario_actual = str(self.usuario_actual[2])
            if actualizarUsuario(nombre, apellido, usuario, contra, usuario_actual) == 1:
                QMessageBox.information(
                    self.mainWinCredenciales, "Éxito",
                    "Actualizado con éxito, vuelva a ingresar al sistema."
                )
                self.mainWinCredenciales.close()
                self.close()


# ─── Login ───────────────────────────────────────────────────────────────────
class Login(QMainWindow, Ui_Login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(ruta_recurso("zico.ico")))
        self.btn_ingresar.clicked.connect(self.validar_acceso)
        self.txt_contra.returnPressed.connect(self.validar_acceso)
        self.txt_usuario.returnPressed.connect(self.validar_acceso)
        self.lbl_recuperar.setOpenExternalLinks(False)
        self.lbl_recuperar.linkActivated.connect(self.mostrar_recuperacion)

    def mostrar_recuperacion(self, link):
        QMessageBox.information(
            self, "Recuperación",
            "Contacte al administrador del sistema para que le ayude a recuperar su usuario y contraseña."
        )

    def validar_acceso(self):
        usuario = self.txt_usuario.text().strip()
        contra = self.txt_contra.text().strip()
        if usuario == "" or contra == "":
            QMessageBox.information(self, "Login", "Los campos no pueden estar vacios")
            return
        datos_usuario = validar_usuario(usuario, contra)
        if datos_usuario is None:
            QMessageBox.warning(self, "Login", "Usuario o contraseña incorrectos")
        elif str(datos_usuario[3]) == "1":
            self.close()
            self.ventana_principal = Sistema()
            self.ventana_principal.usuario_actual = datos_usuario
            self.ventana_principal.show()
        elif str(datos_usuario[3]) == "0":
            QMessageBox.information(self, "Permisos", "Solicite permisos con el usuario administrador")
        else:
            QMessageBox.warning(self, "Permisos", "Permiso de usuario no reconocido")
        self.txt_usuario.clear()
        self.txt_contra.clear()
        self.txt_usuario.setFocus()


# ─── Arranque ────────────────────────────────────────────────────────────────
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
    "Zeta.DieselVillaNueva"
)

app = QApplication(sys.argv)
icono = QIcon(ruta_recurso("zico.ico"))
app.setWindowIcon(icono)

login = Login()
login.setWindowIcon(icono)
login.show()

sys.exit(app.exec())