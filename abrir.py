from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter.scrolledtext as st 
import lexicoJavascript
import subprocess

archivo = ""
extension_archivo = ""

def abrir(codigo,errores_t):
    codigo.delete(1.0,END)
    errores_t.delete(1.0,END)
    root = Tk()
    root.withdraw()
    root.update()
    pathString = askopenfilename(filetypes=[("Archivos","*")])
    if pathString:
        global archivo, extension_archivo
        archivo = open(pathString, 'r')
        #extension
        split_extension = archivo.name.split(".")
        extension_archivo = split_extension[1]
        #leer lineas
        lexicoJavascript.primer_analisis()
        # lexicoJavascript.imprimir()
    root.destroy()

def analisis(codigo,errores_t):
    global archivo, extension_archivo
    while (True):
        linea = archivo.readline().lower()
        if not linea:
            break
        if extension_archivo == "js":
            lexicoJavascript.lexicoJavascript(linea)
    archivo.close()
    archivo = ""
    if extension_archivo == "js":
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
   

def crear_dot():
    if extension_archivo == "js":
        itera = 0
        while itera < 2:
            rutaA = lexicoJavascript.tokens[itera].palabra.split(":")
            rutaB = rutaA[1].split("/")
            print(rutaB)
            break
        rutaC = ""
        for x in rutaB:
            if x == "user":
                rutaC += "/"
                rutaC += "rau"
            elif x.isspace():
                pass
            else:
                rutaC += "/"
                rutaC += x
        rutaC+="graficoJs.dot"
        print(rutaC)
        with open(rutaC,'w') as file:
            file.write("digraph G {\n")
            file.write("node [shape=circle, color=yellow]\n")
            if lexicoJavascript.eA == True:
                file.write("A\n")
                pass
            if lexicoJavascript.eB == True:
                file.write("A -> B [label = L]\n")
                file.write("B -> B [label = \"L|N\"]\n")
                pass
            if lexicoJavascript.eD == True:
                file.write("A -> D [label = N]\n")
                file.write("D -> D [label = N]\n")
                pass
            if lexicoJavascript.eG == True:
                file.write("D -> G [label = S]\n")
                pass
            if lexicoJavascript.eH == True and lexicoJavascript.eG == True:
                file.write("G -> H [label = N]\n")
                pass
            if lexicoJavascript.eC == True:
                file.write("A -> C [label = S]\n")
                pass
            if lexicoJavascript.eE == True:
                file.write("C -> E [label = \"L|N\"]\n")
                file.write("E -> E [label = \"L|N\"]\n")
                pass
            if lexicoJavascript.eH == True and lexicoJavascript.eE == True:
                file.write("E -> H [label = S]\n")
                pass
            if lexicoJavascript.eF == True:
                file.write("C -> F [label = S]\n")
                pass
            if lexicoJavascript.eI == True:
                file.write("F -> I [label = \"L|N|S\"]\n")
                file.write("I -> I [label = \"L|N|S\"]\n")
                pass
            if lexicoJavascript.eJ == True:
                file.write("I -> J [label = S]\n")
                pass
            if lexicoJavascript.eH == True and lexicoJavascript.eJ == True:
                file.write("J -> H [label = S]\n")
                pass
            file.write("}")
    # subprocess.call('dot -Tpng graficoJs.dot -o graficoJs.png', shell=True)
