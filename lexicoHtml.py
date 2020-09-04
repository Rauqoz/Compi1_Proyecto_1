class lexema:
    def __init__(self,palabra,tipo):
        self.palabra = palabra
        self.tipo =  tipo

class error:
    def __init__(self,palabra,fila,columna):
        self.palabra = palabra
        self.fila = fila
        self.columna = columna


char = []
tokens = []
errores = []
fila = 1
columna = 0
palabra =""
i = 0
estado = 'A'
cadena_caracter = False
comentario = False
multilinea = False
palabrasReservadas = ["html","head","title","body","h1","h2","h3","h4","h5","h6","p","img","a","ul","li","table","th","tr","td","caption","colgroup","col","thead","tbody","tfoot"]
signos = ["<",">","/","=","\"",]

def primer_analisis():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea
    char = []
    tokens = []
    errores = []
    fila = 1
    columna = 0
    palabra =""
    i = 0
    estado = 'A'

def reservadas_buscar():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea
    esReservada = False
    for x  in palabrasReservadas:
        if palabra == x:
            # print("agrego reservada")
            esReservada = True
            tokens.append(lexema(palabra,"etiqueta"))
            palabra = ""
            break
    if not esReservada:
        # print("agrego id")
        tokens.append(lexema(palabra,"id"))
        palabra = ""

def errores_buscar():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea
    errores.append(error(char[i],fila,columna))
    palabra = ""

def vacios():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea
    tokens.append(lexema(char[i],"espacio"))

def signos_buscar():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea
    esSigno = False
    # print("buscando signo")
    for x  in signos:
        if char[i] == x:
            esSigno = True
            tokens.append(lexema(char[i],"signo"))
            palabra = ""
            break
    if not esSigno:
        errores.append(error(char[i],fila,columna))
        palabra = ""

def esta_A():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea
    if char[i].isalpha():
        i-=1
        estado = 'B'
    elif char[i] == "\n" :
        vacios()
        estado = 'A'
        fila += 1
    elif char[i].isspace():
        vacios()
        estado = 'A'
    elif char[i] == '>':
        signos_buscar()
        estado = 'C'
        comentario = True
    elif char[i] == '<' or char[i] == '=':
        signos_buscar()
    elif char[i] == '/' and char[i-1] == '<':
        signos_buscar()
    elif char[i] == '\"':
        palabra += char[i]
        estado = 'C'
        cadena_caracter = True
    else:
        errores_buscar()
        estado = 'A'

def esta_B():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea
    if char[i].isalpha() or char[i].isnumeric():
        palabra += char[i]
    elif char[i] == "\n" :
        reservadas_buscar()
        vacios()
        estado = 'A'
        fila += 1
    elif char[i].isspace():
        reservadas_buscar()
        vacios()
        estado = 'A'
    elif char[i] == '=' or char[i] == '>' :
        reservadas_buscar()
        i-=1
        estado = 'A'
    else:
        reservadas_buscar()
        errores_buscar()
        estado = 'A'

def esta_C():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea
    palabra += char[i]
    estado = 'D'
    pass

def esta_D():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea
    if char[i] == '\"' and cadena_caracter == True:
        palabra += char[i]
        estado = 'E'
    elif char[i] == '<' and comentario == True:
        tokens.append(lexema(palabra,"texto"))
        i-=1
        estado = 'A'
    else:
        palabra += char[i]

def esta_E():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea
    if cadena_caracter == True:
        tokens.append(lexema(palabra,"cadena"))
        i-=1
        estado = 'A'
    pass


def lexicoHtml(linea):
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea
    
    char = list(linea)
    tamaño = len(char)
    columna = 0
    i = 0
    while i<tamaño:
        if tamaño == 0:
            break
        
        if estado == 'A':
           esta_A()
        elif estado == 'B':
            esta_B()
            pass
        elif estado == 'C':
            esta_C()
            pass
        elif estado == 'D':
            esta_D()
            pass
        elif estado == 'E':
            esta_E()
            pass
        columna +=1
        i+=1

def imprimir():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea
    print (" - - - Tokens - - -")
    if len(tokens) != 0:
        for x in tokens:
            print(x.palabra + " - " + x.tipo)
    print(" - - - Errores - - -")
    if len(errores) != 0:
        for x in errores:
            print(x.palabra + " - Fila " + str(x.fila) + " - Columna " + str(x.columna))

