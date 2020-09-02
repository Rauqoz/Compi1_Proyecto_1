from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter.scrolledtext as st 
import lexicoJavascript

archivo = ""

def abrir(codigo,errores_t):
    codigo.delete(1.0,END)
    errores_t.delete(1.0,END)
    root = Tk()
    root.withdraw()
    root.update()
    pathString = askopenfilename(filetypes=[("Archivos","*")])
    if pathString:
        global archivo
        archivo = open(pathString, 'r')
        #extension
        split_extension = archivo.name.split(".")
        extension_archivo = split_extension[1]
        lexicoJavascript.extension = extension_archivo
        print("extension del archivo = " + extension_archivo)
        #leer lineas
        lexicoJavascript.primer_analisis()
        # lexicoJavascript.imprimir()
    root.destroy()

def analisis(codigo,errores_t):
    global archivo
    while (True):
        linea = archivo.readline().lower()
        if not linea:
            break
        if lexicoJavascript.extension == "js":
            lexicoJavascript.lexicoJavascript(linea)
    archivo.close()
    archivo = ""
    pintar_js(codigo,errores_t)

def pintar_js(codigo,errores_t):
    if len(lexicoJavascript.tokens) != 0:
        for x in lexicoJavascript.tokens:
            codigo.insert(INSERT, x.palabra, "\"" + x.tipo + "\"")
            codigo.tag_config("reservada", foreground="red") 
            codigo.tag_config("id" ,foreground="green") 
            codigo.tag_config("cadena", foreground="yellow") 
            codigo.tag_config("caracter", foreground="yellow") 
            codigo.tag_config("entero", foreground="blue") 
            codigo.tag_config("decimal", foreground="blue") 
            codigo.tag_config("comentario", foreground="gray") 
            codigo.tag_config("signo", foreground="black") 
            codigo.tag_config("operador", foreground="orange") 
    if len(lexicoJavascript.errores) != 0:
        errores_t.insert(INSERT, "Error\tFila\tColumna\n" , "normal")
        for x in lexicoJavascript.errores:
            errores_t.insert(INSERT, x.palabra + "\t" + str(x.fila) + "\t" + str(x.columna) + "\n", "normal")
            errores_t.tag_config("normal", foreground="white") 