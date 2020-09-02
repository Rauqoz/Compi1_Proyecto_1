class lexema:
    def __init__(self,palabra,tipo):
        self.palabra = palabra
        self.tipo =  tipo

class error:
    def __init__(self,palabra,fila,columna):
        self.palabra = palabra
        self.fila = fila
        self.columna = columna

eA = False
eB = False
eC = False
eD = False
eE = False
eF = False
eG = False
eH = False
eI = False
eJ = False
extension = ""
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
decimal = False
palabrasReservadas = ["var","true","false","if","else","for","break","while","do","continue","return","constructor","class","this","function","math","pow","pathl","pathw"]
signos = ["/","*","=","\"","'",";",".",",","<",">","+","-","(",")","{","}","&","!","|","\\",":"]

def primer_analisis():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea,decimal,eA,eB,eC,eD,eE,eF,eG,eH,eI,eJ
    char = []
    tokens = []
    errores = []
    fila = 1
    columna = 0
    palabra =""
    i = 0
    estado = 'A'
    
def reservadas_buscar():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea,decimal,eA,eB,eC,eD,eE,eF,eG,eH,eI,eJ
    esReservada = False
    for x  in palabrasReservadas:
        if palabra == x:
            # print("agrego reservada")
            esReservada = True
            tokens.append(lexema(palabra,"reservada"))
            palabra = ""
            break
    if not esReservada:
        # print("agrego id")
        tokens.append(lexema(palabra,"id"))
        palabra = ""

def errores_buscar():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea,decimal,eA,eB,eC,eD,eE,eF,eG,eH,eI,eJ
    errores.append(error(char[i],fila,columna))
    palabra = ""

def vacios():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea,decimal,eA,eB,eC,eD,eE,eF,eG,eH,eI,eJ
    tokens.append(lexema(char[i],"espacio"))

def signos_buscar():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea,decimal,eA,eB,eC,eD,eE,eF,eG,eH,eI,eJ
    esSigno = False
    # print("buscando signo")
    for x  in signos:
        if char[i] == x:
            esSigno = True
            if char[i] == '+' or char[i] ==  '-' or char[i] == '*' or char[i] == '/':
                tokens.append(lexema(char[i],"operador"))
            else:
                tokens.append(lexema(char[i],"signo"))
            palabra = ""
            break
    if not esSigno:
        errores.append(error(char[i],fila,columna))
        palabra = ""

def esta_A():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea,decimal,eA,eB,eC,eD,eE,eF,eG,eH,eI,eJ
    # print("estado A")
    eA = True
    if char[i].isalpha():
        # print("letra")
        i-=1
        estado = 'B'
    elif char[i].isnumeric():
        i-=1
        estado = 'D'
        # print("numero")
    elif char[i] == "\n" :
        # print("espacio")
        vacios()
        estado = 'A'
        fila += 1
    elif char[i].isspace():
        vacios()
        estado = 'A'
    elif char[i] == '\'' or char[i] == '\"':
        # print(char[i])
        palabra += char[i]
        estado = 'C'
        cadena_caracter = True
    elif char[i] == '/':
        palabra += char[i]
        estado = 'C'
        comentario = True
    else:
        signos_buscar()
        estado = 'A'

def esta_B():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea,decimal,eA,eB,eC,eD,eE,eF,eG,eH,eI,eJ
    # print("estado B")
    eB = True
    if char[i].isalpha() or char[i].isnumeric():
        palabra += char[i]
        estado = 'B'
    elif char[i] == "\n":
        reservadas_buscar()
        vacios()
        fila += 1
        estado = 'A'
    elif char[i].isspace():
        reservadas_buscar()
        vacios()
        estado = 'A'
    else:
        reservadas_buscar()
        i-= 1
        estado = 'A'

def esta_C():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea,decimal,eA,eB,eC,eD,eE,eF,eG,eH,eI,eJ
    # print("estado C")
    eC = True
    if cadena_caracter == True:
        if char[i] != '\'' and char[i] != '\"':
            # print("b")
            palabra += char[i]
            estado = 'E'
        if char[i] == '\'' or char[i] == '\"':
            # print("a")
            i-=1
            signos_buscar()
            i+=1
            signos_buscar()
            estado = 'A'
            palabra = ""
            cadena_caracter = False
    elif char[i] == '*' :
        multilinea = True
        palabra += char[i]
        estado = 'F'
    elif char[i] == '/':
        palabra += char[i]
        estado = 'F'
    elif char[i].isspace():
        i-=1
        signos_buscar()
        estado = 'A'
        comentario = False
    else:
        i-=1
        errores_buscar()
        estado = 'A'
        comentario = False

def esta_D():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea,decimal,eA,eB,eC,eD,eE,eF,eG,eH,eI,eJ
    eD = True
    if char[i].isnumeric():
        palabra += char[i]
    elif char[i] == '.':
        palabra += char[i]
        estado = 'G'
        decimal = True
    else:
        tokens.append(lexema(palabra,"entero"))
        i-=1
        palabra = ""
        estado = 'A'

    pass

def esta_E():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea,decimal,eA,eB,eC,eD,eE,eF,eG,eH,eI,eJ
    eE = True
    if char[i] == '\'' or char[i] == '\"':
        i-=1
        estado = 'H'
    else:
        palabra += char[i]

def esta_F():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea,decimal,eA,eB,eC,eD,eE,eF,eG,eH,eI,eJ
    eF = True
    palabra += char[i]
    estado = 'I'
    pass

def esta_G():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea,decimal,eA,eB,eC,eD,eE,eF,eG,eH,eI,eJ
    eG = True
    palabra += char[i]
    estado = 'H'
    pass

def esta_H():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea,decimal,eA,eB,eC,eD,eE,eF,eG,eH,eI,eJ
    eH = True
    if char[i] == '\'':
        palabra += char[i]
        tokens.append(lexema(palabra,"caracter"))
        palabra = ""
        estado = 'A'
        cadena_caracter = False
    elif char[i] == "\"":
        palabra += char[i]
        tokens.append(lexema(palabra,"cadena"))
        palabra = ""
        estado = 'A'
        cadena_caracter = False
    elif comentario == True:
        tokens.append(lexema(palabra,"comentario"))
        vacios()
        palabra = ""
        estado = 'A'
        multilinea = False
    elif decimal == True and char[i].isnumeric():
        palabra += char[i]
    elif decimal == True and (char[i] == "\n"):
        tokens.append(lexema(palabra,"decimal"))
        palabra = ""
        estado = 'A'
        fila += 1
        decimal = False
    elif decimal == True and char[i].isspace():
        tokens.append(lexema(palabra,"decimal"))
        palabra = ""
        estado = 'A'
        decimal = False
    pass

def esta_I():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea,decimal,eA,eB,eC,eD,eE,eF,eG,eH,eI,eJ
    eI = True
    if char[i] == '*' and char[i+1] == '/':
        palabra += char[i]
        estado = 'J'
    elif char[i] == "\n" and multilinea == False:
        tokens.append(lexema(palabra,"comentario"))
        vacios()
        comentario = False
        palabra = ""
        estado = 'A'
        fila += 1
    else:
        palabra += char[i]
    pass

def esta_J():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea,decimal,eA,eB,eC,eD,eE,eF,eG,eH,eI,eJ
    eJ = True
    if char[i] == '/':
        palabra += char[i]
        estado = 'H'
    pass

def lexicoJavascript(linea):
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea,decimal,eA,eB,eC,eD,eE,eF,eG,eH,eI,eJ
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
        elif estado == 'F':
            esta_F()
            pass
        elif estado == 'G':
            esta_G()
            pass
        elif estado == 'H':
            esta_H()
            pass
        elif estado == 'I':
            esta_I()
            pass
        elif estado == 'J':
            esta_J()
            pass
        columna +=1
        i+=1


def imprimir():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,multilinea,decimal,eA,eB,eC,eD,eE,eF,eG,eH,eI,eJ
    print (" - - - Tokens - - -")
    if len(tokens) != 0:
        for x in tokens:
            print(x.palabra + " - " + x.tipo)
    print(" - - - Errores - - -")
    if len(errores) != 0:
        for x in errores:
            print(x.palabra + " - Fila " + str(x.fila) + " - Columna " + str(x.columna))

