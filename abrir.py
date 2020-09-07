from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter.scrolledtext as st 
import tkinter.messagebox as ms
import lexicoJavascript
import lexicoHtml
import subprocess
import os

archivo = ""
extension_archivo = ""
rutadot = ""
rutapng = ""
rutanuevo = ""
rutaerrores = ""

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
        lexicoHtml.primer_analisis()
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
        elif extension_archivo == 'html':
            lexicoHtml.lexicoHtml(linea)
    archivo.close()
    archivo = ""
    if extension_archivo == "js":
        pintar_js(codigo,errores_t)
    elif extension_archivo == "html":
        pintar_html(codigo,errores_t)

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
    # crear_dot()
    crear_dot_Js()

def pintar_html(codigo,errores_t):
    if len(lexicoHtml.tokens) != 0:
        for x in lexicoHtml.tokens:
            codigo.insert(INSERT, x.palabra, "\"" + x.tipo + "\"")
            codigo.tag_config("etiqueta", foreground="red") 
            codigo.tag_config("id" ,foreground="green") 
            codigo.tag_config("cadena", foreground="yellow") 
            codigo.tag_config("comentario", foreground="gray") 
            codigo.tag_config("texto", foreground="black") 
    if len(lexicoHtml.errores) != 0:
        errores_t.insert(INSERT, "Error\tFila\tColumna\n" , "normal")
        for x in lexicoHtml.errores:
            errores_t.insert(INSERT, x.palabra + "\t" + str(x.fila) + "\t" + str(x.columna) + "\n", "normal")
            errores_t.tag_config("normal", foreground="white") 
    # lexicoHtml.imprimir()
    # crear_dot()
    crear_dot_Html()

def crear_dot_Js():
    global rutadot, rutapng, rutanuevo,rutaerrores
    rutadot = ""
    rutapng = ""
    if extension_archivo == "js":
        for x in lexicoJavascript.tokens:
            if x.tipo == "comentario":
                comentario_completo = x.palabra
                comentario_completo.replace("pathl","path")
                comentario_completo.replace("pathw","path")
                # print(comentario_completo)
                corte0 = comentario_completo.find("path:") + len("path:")
                parte0 = comentario_completo[corte0:].replace("\\","/")
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
                        rutanuevo = parte1 + "corregido.js"
                        rutaerrores = parte1 + "erroresJs.html"
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
            with open( rutanuevo ,'w') as file:    
                for x in lexicoJavascript.tokens:
                    file.write(x.palabra)
            with open( rutaerrores ,'w') as file:
                file.write("<html>" +"<head>" +"</head>" +"<body style='background-color:#34495E'>")
                file.write("<table border=11 , align='center', bordercolor='orange'>" +"<tr align=center> <th><font color ='white'> Numero </th> <th><font color ='white'> Fila </th> <th><font color ='white'> Columna </th> <th><font color ='white'> Palabra </th> <th><font color ='white'> Error </th></tr>")
                i = 0
                for x in lexicoJavascript.errores:
                    i+=1
                    file.write("\n<tr align=center> <td><font color ='white'> " + str(i) + " </td> <td><font color ='white'> " + str(x.fila) + " </td> <td><font color ='white'> " + str(x.columna) + " </td> <td><font color ='white'> " + x.palabra + " </td> <td><font color ='white'> Signo Error </td></tr>")
    pass

def crear_dot_Html():
    if extension_archivo == "html":
        for x in lexicoHtml.tokens:
            if x.tipo == "comentario":
                comentario_completo = x.palabra
                comentario_completo.replace("pathl","path")
                comentario_completo.replace("pathw","path")
                # print(comentario_completo)
                corte0 = comentario_completo.find("path:") + len("path:")
                parte0 = comentario_completo[corte0:].replace("\\","/")
                # print(parte0)
                corte1 = parte0.find("user/") + len("user/")
                parte1 = parte0[corte1:]
                # corte2 = parte1.find("=")
                # parte2 = parte1[:corte2]
                # print(parte2)
                if parte1 != "":
                    try:
                        rutadot = parte1 + "graficoHtml.dot"
                        rutapng = parte1 + "graficoHtml.png"
                        rutanuevo = parte1 + "corregido.html"
                        rutaerrores = parte1 + "erroresHtml.html"
                        os.makedirs(parte1 , exist_ok=True)
                    except OSError:
                        ms.showinfo(message="Directorio no Creado",title="Error")
                break
        if rutadot != "":
            with open( rutadot ,'w') as file:
                file.write("digraph G {\n")
                file.write("node [shape=circle, color=yellow]\n")
                if lexicoHtml.eA == True:
                    file.write("A\n")
                    pass
                if lexicoHtml.eB == True:
                    file.write("A -> B [label = L]\n")
                    file.write("B -> B [label = \"L|N\"]\n")
                    pass
                if lexicoHtml.eD == True:
                    file.write("C -> D [label = \"L|N|S\"]\n")
                    file.write("D -> D [label = \"L|N|S\"]\n")
                    pass
                if lexicoHtml.eC == True:
                    file.write("A -> C [label = S]\n")
                    pass
                if lexicoHtml.eE == True:
                    file.write("D -> E [label = S]\n")
                    pass
                file.write("}")
            subprocess.call("dot -Tpng " + rutadot + " -o " + rutapng, shell=True)
            with open( rutanuevo ,'w') as file:    
                for x in lexicoHtml.tokens:
                    file.write(x.palabra)
            with open( rutaerrores ,'w') as file:
                file.write("<html>" +"<head>" +"</head>" +"<body style='background-color:#34495E'>")
                file.write("<table border=11 , align='center', bordercolor='orange'>" +"<tr align=center> <th><font color ='white'> Numero </th> <th><font color ='white'> Fila </th> <th><font color ='white'> Columna </th> <th><font color ='white'> Palabra </th> <th><font color ='white'> Error </th></tr>")
                i = 0
                for x in lexicoHtml.errores:
                    i+=1
                    file.write("\n<tr align=center> <td><font color ='white'> " + str(i) + " </td> <td><font color ='white'> " + str(x.fila) + " </td> <td><font color ='white'> " + str(x.columna) + " </td> <td><font color ='white'> " + x.palabra + " </td> <td><font color ='white'> Signo Error </td></tr>")    
    pass

def crear_dot():
    global rutadot, rutapng, rutanuevo,rutaerrores
    rutadot = ""
    rutapng = ""
    if extension_archivo == "js":
        for x in lexicoJavascript.tokens:
            if x.tipo == "comentario":
                comentario_completo = x.palabra
                comentario_completo.replace("pathl","path")
                comentario_completo.replace("pathw","path")
                # print(comentario_completo)
                corte0 = comentario_completo.find("path:") + len("path:")
                parte0 = comentario_completo[corte0:].replace("\\","/")
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
                        rutanuevo = parte1 + "corregido.js"
                        rutaerrores = parte1 + "erroresJs.html"
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
            with open( rutanuevo ,'w') as file:    
                for x in lexicoJavascript.tokens:
                    file.write(x.palabra)
            with open( rutaerrores ,'w') as file:
                file.write("<html>" +"<head>" +"</head>" +"<body style='background-color:#34495E'>")
                file.write("<table border=11 , align='center', bordercolor='orange'>" +"<tr align=center> <th><font color ='white'> Numero </th> <th><font color ='white'> Fila </th> <th><font color ='white'> Columna </th> <th><font color ='white'> Palabra </th> <th><font color ='white'> Error </th></tr>")
                i = 0
                for x in lexicoJavascript.errores:
                    i+=1
                    file.write("\n<tr align=center> <td><font color ='white'> " + str(i) + " </td> <td><font color ='white'> " + str(x.fila) + " </td> <td><font color ='white'> " + str(x.columna) + " </td> <td><font color ='white'> " + x.palabra + " </td> <td><font color ='white'> Signo Error </td></tr>")

    if extension_archivo == "html":
        for x in lexicoHtml.tokens:
            if x.tipo == "comentario":
                comentario_completo = x.palabra
                comentario_completo.replace("pathl","path")
                comentario_completo.replace("pathw","path")
                # print(comentario_completo)
                corte0 = comentario_completo.find("path:") + len("path:")
                parte0 = comentario_completo[corte0:].replace("\\","/")
                # print(parte0)
                corte1 = parte0.find("user/") + len("user/")
                parte1 = parte0[corte1:]
                # corte2 = parte1.find("=")
                # parte2 = parte1[:corte2]
                # print(parte2)
                if parte1 != "":
                    try:
                        rutadot = parte1 + "graficoHtml.dot"
                        rutapng = parte1 + "graficoHtml.png"
                        rutanuevo = parte1 + "corregido.html"
                        rutaerrores = parte1 + "erroresHtml.html"
                        os.makedirs(parte1 , exist_ok=True)
                    except OSError:
                        ms.showinfo(message="Directorio no Creado",title="Error")
                break
        if rutadot != "":
            with open( rutadot ,'w') as file:
                file.write("digraph G {\n")
                file.write("node [shape=circle, color=yellow]\n")
                if lexicoHtml.eA == True:
                    file.write("A\n")
                    pass
                if lexicoHtml.eB == True:
                    file.write("A -> B [label = L]\n")
                    file.write("B -> B [label = \"L|N\"]\n")
                    pass
                if lexicoHtml.eD == True:
                    file.write("C -> D [label = \"L|N|S\"]\n")
                    file.write("D -> D [label = \"L|N|S\"]\n")
                    pass
                if lexicoHtml.eC == True:
                    file.write("A -> C [label = S]\n")
                    pass
                if lexicoHtml.eE == True:
                    file.write("D -> E [label = S]\n")
                    pass
                file.write("}")
            subprocess.call("dot -Tpng " + rutadot + " -o " + rutapng, shell=True)
            with open( rutanuevo ,'w') as file:    
                for x in lexicoHtml.tokens:
                    file.write(x.palabra)
            with open( rutaerrores ,'w') as file:
                file.write("<html>" +"<head>" +"</head>" +"<body style='background-color:#34495E'>")
                file.write("<table border=11 , align='center', bordercolor='orange'>" +"<tr align=center> <th><font color ='white'> Numero </th> <th><font color ='white'> Fila </th> <th><font color ='white'> Columna </th> <th><font color ='white'> Palabra </th> <th><font color ='white'> Error </th></tr>")
                i = 0
                for x in lexicoHtml.errores:
                    i+=1
                    file.write("\n<tr align=center> <td><font color ='white'> " + str(i) + " </td> <td><font color ='white'> " + str(x.fila) + " </td> <td><font color ='white'> " + str(x.columna) + " </td> <td><font color ='white'> " + x.palabra + " </td> <td><font color ='white'> Signo Error </td></tr>")    

