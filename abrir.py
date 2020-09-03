from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter.scrolledtext as st 
import tkinter.messagebox as ms
import lexicoJavascript
import subprocess
import os

archivo = ""
extension_archivo = ""
rutadot = ""
rutapng = ""

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
    crear_dot()

def crear_dot():
    global rutadot, rutapng
    rutadot = ""
    rutapng = ""
    if extension_archivo == "js":
        for x in lexicoJavascript.tokens:
            if x.tipo == "comentario":
                comentario_completo = x.palabra
                # print(comentario_completo)
                corte0 = comentario_completo.find("pathl:") + len("pathl:")
                parte0 = comentario_completo[corte0:]
                # print(parte0)
                corte1 = parte0.find("user/") + len("user/")
                parte1 = parte0[corte1:]
                # corte2 = parte1.find("=")
                # parte2 = parte1[:corte2]
                # print(parte2)
                if parte1 != "":
                    try:
                        rutadot = parte1 + "graficoJs.dot"
                        rutapng = parte1 + "graficoJs.png"
                        os.makedirs(parte1 , exist_ok=True)
                    except OSError:
                        ms.showinfo(message="Directorio no Creado",title="Error")
                break
        if rutadot != "":
            with open( rutadot ,'w') as file:
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
            subprocess.call("dot -Tpng " + rutadot + " -o " + rutapng, shell=True)
