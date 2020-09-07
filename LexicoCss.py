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
palabrasReservadas = ["color","font-weight","background-color", "background-image","border", "Opacity", "background","text-align", "font-family","font-style","font-weight","font-size", "font", "padding-left", "padding-right", "padding-bottom","padding-top", "padding", "display","line-height", "width", "height","margin-top","margin-right", "margin-bottom","margin-left", "margin", "border-style","display","position", "bottom","top", "right", "left","float", "clear", "max-width","min-width","max-height", "min-height"]
signos = ['{','}',':',';','#',',','.','-','%','(',')']


def primer_analisis():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,eA,eB,eC,eD,eE,eF,eG,eH,eI
    char = []
    tokens = []
    errores = []
    fila = 1
    columna = 0
    palabra =""
    i = 0
    estado = 'A'
    eA = False
    eB = False
    eC = False
    eD = False
    eE = False
    eF = False
    eG = False
    eH = False
    eI = False


def reservadas_buscar():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,eA,eB,eC,eD,eE,eF,eG,eH,eI
    esReservada = False
    for x  in palabrasReservadas:
        if palabra == x:
            # print("agrego reservada")
            esReservada = True
            tokens.append(lexema(palabra,"propiedad"))
            palabra = ""
            break
    if not esReservada:
        # print("agrego id")
        tokens.append(lexema(palabra,"id"))
        palabra = ""

def errores_buscar():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,eA,eB,eC,eD,eE,eF,eG,eH,eI
    errores.append(error(char[i],fila,columna))
    palabra = ""

def vacios():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,eA,eB,eC,eD,eE,eF,eG,eH,eI
    tokens.append(lexema(char[i],"espacio"))

def signos_buscar():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,eA,eB,eC,eD,eE,eF,eG,eH,eI
    esSigno = False
    # print("buscando signo")
    for x  in signos:
        if char[i] == x:
            # print("es signo " + char[i])
            esSigno = True
            tokens.append(lexema(char[i],"signo"))
            palabra = ""
            break
    if not esSigno:
        # print("no es signo "+ char[i])
        errores.append(error(char[i],fila,columna))
        palabra = ""

def esta_A():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,eA,eB,eC,eD,eE,eF,eG,eH,eI
    eA = True
    palabra = ""
    # print(char[i])
    if char[i].isalpha():
        palabra += char[i]
        estado = 'B'
    elif char[i].isnumeric():
        palabra += char[i]
        estado = 'C'
    elif char[i] == "\n":
        vacios()
        estado = 'A'
        fila += 1
    elif char[i].isspace():
        vacios()
        estado = 'A'
    elif char[i] == '\"':
        cadena_caracter = True
        palabra += char[i]
        estado = 'D'
    elif char[i] == '/':
        palabra += char[i]
        estado = 'D'
    else:
        signos_buscar()
        palabra = ""
        estado = 'A'

def esta_B():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,eA,eB,eC,eD,eE,eF,eG,eH,eI
    eB = True
    if char[i].isalpha() or char[i].isnumeric() or char[i] == "-":
        palabra += char[i]
    elif char[i].isspace() or char[i] == "\n":
        reservadas_buscar()
        vacios()
        estado = 'A'
    else:
        reservadas_buscar()
        signos_buscar()
        estado = 'A'
    
def esta_C():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,eA,eB,eC,eD,eE,eF,eG,eH,eI
    eC = True
    if char[i].isnumeric():
        palabra += char[i]
    elif char[i].isalpha():
        palabra += char[i]
        estado = 'E'
    elif char[i] == '.':
        palabra += char[i]
        estado = 'F'
    elif char[i].isspace() or char[i] == "\n":
        tokens.append(lexema(palabra,"valor"))
        vacios()
        estado = 'A'
    else:
        tokens.append(lexema(palabra,"valor"))
        signos_buscar()
        estado = 'A'
    
def esta_D():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,eA,eB,eC,eD,eE,eF,eG,eH,eI
    eD = True
    if cadena_caracter:
        palabra += char[i]
        estado = 'G'
    elif char[i] == '*':
        palabra += char[i]
        comentario = True
        estado = 'G'
    elif char[i].isspace() or char[i] == "\n":
        signos_buscar()
        vacios()
        estado = 'A'
    else:
        signos_buscar()
        estado = 'A'

def esta_E():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,eA,eB,eC,eD,eE,eF,eG,eH,eI
    eE = True
    if char[i].isalpha() or char[i].isnumeric():
        palabra += char[i]
    elif char[i].isspace() or char[i] == "\n":
        tokens.append(lexema(palabra,"valor"))
        vacios()
        estado = 'A'
    else:
        tokens.append(lexema(palabra,"valor"))
        signos_buscar()
        estado = 'A'
   
def esta_F():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,eA,eB,eC,eD,eE,eF,eG,eH,eI
    eF = True
    if char[i].isnumeric():
        palabra += char[i]
        estado = 'H'
    elif char[i].isspace() or char[i] == "\n":
        palabra += "0"
        tokens.append(lexema(palabra,"valor"))
        vacios()
        estado = 'A'
    else:
        palabra += "0"
        tokens.append(lexema(palabra,"valor"))
        if char[i].isalpha():
            i-=1
        else:
            signos_buscar()
        estado = 'A'
  
def esta_G():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,eA,eB,eC,eD,eE,eF,eG,eH,eI
    eG = True
    if cadena_caracter:
        if char[i].isalpha() or char[i].isnumeric() or char[i].isspace() or char[i] == '\n':
            palabra += char[i]
        else:
            i-=1
            estado = 'I'
    elif comentario:
        if char[i].isalpha() or char[i].isnumeric() or char[i].isspace() or char[i] == '\n':
            palabra += char[i]
        else:
            i-=1
            estado = 'I'

def esta_H():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,eA,eB,eC,eD,eE,eF,eG,eH,eI
    eH = True
    if char[i].isnumeric():
        palabra += char[i]
    elif char[i].isspace() or char[i] == "\n":
        tokens.append(lexema(palabra,"valor"))
        vacios()
        estado = 'A'
    else:
        tokens.append(lexema(palabra,"valor"))
        if char[i].isalpha():
            i-=1
        else:
            signos_buscar()
        estado = 'A'
  
def esta_I():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,eA,eB,eC,eD,eE,eF,eG,eH,eI
    eI = True


    if cadena_caracter:
        if char[i] == '\"':
            palabra += char[i]
            tokens.append(lexema(palabra,"cadena"))
            cadena_caracter = False
            estado = 'A'
        else:
            palabra += char[i]
            estado = 'G'
    elif comentario:
        if char[i - 1] == '*' and char[i] == '/':
            palabra += char[i]
            tokens.append(lexema(palabra,"comentario"))
            comentario = False
            estado = 'A'
        else:
            palabra += char[i]
            estado = 'G'
        

def lexicoCss(linea):
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,eA,eB,eC,eD,eE,eF,eG,eH,eI
    
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
        columna +=1
        i+=1

def imprimir():
    global char,tokens,fila,columna,palabra,i,estado,palabrasReservadas,errores,signos,cadena_caracter,comentario,eA,eB,eC,eD,eE,eF,eG,eH,eI
    print (" - - - Tokens - - -")
    if len(tokens) != 0:
        for x in tokens:
            print(x.palabra + " - " + x.tipo)
    print(" - - - Errores - - -")
    if len(errores) != 0:
        for x in errores:
            print(x.palabra + " - Fila " + str(x.fila) + " - Columna " + str(x.columna))

