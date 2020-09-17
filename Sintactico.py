class lexema:
    def __init__(self, palabra, tipo):
        self.palabra = palabra
        self.tipo = tipo


class error:
    def __init__(self, palabra, fila, columna):
        self.palabra = palabra
        self.fila = fila
        self.columna = columna


eA = False
eB = False
eC = False
eD = False
eE = False
eF = False
char = []
tokens = []
errores = []
pila = []
pila_sintactico = []
fila = 1
columna = 0
palabra = ""
i = 0
estado = "A"


def primer_analisis():
    global char, tokens, fila, columna, palabra, i, estado, errores, eA, eB, eC, eD, eE, eF, pila, lastPila,pila_sintactico
    char = []
    tokens = []
    errores = []
    fila = 1
    columna = 0
    palabra = ""
    i = 0
    estado = "A"
    eA = False
    eB = False
    eC = False
    eD = False
    eE = False
    eF = False


def errores_buscar():
    global char, tokens, fila, columna, palabra, i, estado, errores, eA, eB, eC, eD, eE, eF, pila, lastPila,pila_sintactico
    errores.append(error(char[i], fila, columna))
    palabra = ""


def vacios():
    global char, tokens, fila, columna, palabra, i, estado, errores, eA, eB, eC, eD, eE, eF, pila, lastPila,pila_sintactico
    tokens.append(lexema(char[i], "espacio"))


def signos_buscar():
    global char, tokens, fila, columna, palabra, i, estado, errores, eA, eB, eC, eD, eE, eF, pila, lastPila,pila_sintactico
    esSigno = False
    # print("buscando signo")
    if char[i] == "(":
        tokens.append(lexema(char[i], "p_a"))
    elif char[i] == ")":
        tokens.append(lexema(char[i], "p_c"))
    elif char[i] == "+":
        tokens.append(lexema(char[i], "signo"))
    elif char[i] == "-":
        tokens.append(lexema(char[i], "signo"))
    elif char[i] == "/":
        tokens.append(lexema(char[i], "signo"))
    elif char[i] == "*":
        tokens.append(lexema(char[i], "signo"))
    else:
        errores.append(error(char[i], fila, columna))
    palabra = ""


def esta_A():
    global char, tokens, fila, columna, palabra, i, estado, errores, eA, eB, eC, eD, eE, eF, pila, lastPila,pila_sintactico
    eA = True
    palabra = ""
    # print(char[i])
    if char[i].isalpha():
        palabra += char[i]
        estado = "B"
    elif char[i].isnumeric():
        palabra += char[i]
        estado = "C"
    elif char[i] == "\n":
        vacios()
        estado = "A"
        fila += 1
    elif char[i].isspace():
        vacios()
        estado = "A"
    elif (
        char[i] == "("
        or char[i] == ")"
        or char[i] == "+"
        or char[i] == "-"
        or char[i] == "*"
        or char[i] == "/"
    ):
        i -= 1
        estado = "D"
    else:
        errores_buscar()


def esta_B():
    global char, tokens, fila, columna, palabra, i, estado, errores, eA, eB, eC, eD, eE, eF, pila, lastPila,pila_sintactico
    eB = True
    if char[i].isalpha() or char[i].isnumeric():
        palabra += char[i]
        estado = "B"
    elif char[i] == "\n" or char[i].isspace():
        tokens.append(lexema(palabra, "variable"))
        vacios()
        estado = "A"
    else:
        tokens.append(lexema(palabra, "variable"))
        i -= 1
        estado = "A"
    pass


def esta_C():
    global char, tokens, fila, columna, palabra, i, estado, errores, eA, eB, eC, eD, eE, eF, pila, lastPila,pila_sintactico
    eC = True
    if char[i].isnumeric():
        palabra += char[i]
        estado = "C"
    elif char[i] == ".":
        palabra += char[i]
        estado = "E"
    elif char[i] == "\n" or char[i].isspace():
        # print("es el fin pero guardo 5")
        tokens.append(lexema(palabra, "numero"))
        vacios()
        palabra = ""
        estado = "A"
    else:
        # print("otra cosa pero guardo " + palabra)
        tokens.append(lexema(palabra, "numero"))
        i -= 1
        palabra = ""
        estado = "A"
    pass


def esta_D():
    global char, tokens, fila, columna, palabra, i, estado, errores, eA, eB, eC, eD, eE, eF, pila, lastPila,pila_sintactico
    eD = True
    signos_buscar()
    estado = "A"
    pass


def esta_E():
    global char, tokens, fila, columna, palabra, i, estado, errores, eA, eB, eC, eD, eE, eF, pila, lastPila,pila_sintactico
    eE = True
    if char[i].isnumeric():
        palabra += char[i]
        estado = "F"
    elif char[i] == "\n" or char[i].isspace():
        palabra += "0"
        tokens.append(lexema(palabra, "numero"))
        vacios()
        palabra = ""
        estado = "A"
    else:
        tokens.append(lexema(palabra, "numero"))
        i -= 1
        palabra = ""
        estado = "A"
    pass


def esta_F():
    global char, tokens, fila, columna, palabra, i, estado, errores, eA, eB, eC, eD, eE, eF, pila, lastPila,pila_sintactico
    eF = True
    if char[i].isnumeric():
        palabra += char[i]
        estado = "F"
    elif char[i] == "\n" or char[i].isspace():
        tokens.append(lexema(palabra, "numero"))
        vacios()
        palabra = ""
        estado = "A"
    else:
        tokens.append(lexema(palabra, "numero"))
        i -= 1
        palabra = ""
        estado = "A"
    pass


def lexicoRmt(linea):
    global char, tokens, fila, columna, palabra, i, estado, errores, eA, eB, eC, eD, eE, eF, pila, lastPila,pila_sintactico

    char = list(linea)
    tamaño = len(char)
    columna = 0
    i = 0
    # print(tamaño)
    while i < tamaño:
        if tamaño == 0 or i == tamaño:
            break

        if estado == "A":
            esta_A()
        elif estado == "B":
            esta_B()
            pass
        elif estado == "C":
            esta_C()
            pass
        elif estado == "D":
            esta_D()
            pass
        elif estado == "E":
            esta_E()
            pass
        elif estado == "F":
            esta_F()
            pass
        columna += 1
        i += 1


def imprimir():
    global char, tokens, fila, columna, palabra, i, estado, errores, eA, eB, eC, eD, eE, eF, pila, lastPila,pila_sintactico
    print(" - - - Tokens - - -")
    if len(tokens) != 0:
        for x in tokens:
            print(x.palabra + " - " + x.tipo)
    print(" - - - Errores - - -")
    if len(errores) != 0:
        for x in errores:
            print(x.palabra + " - Fila " + str(x.fila) + " - Columna " + str(x.columna))


def lastPila():
    # print(pila[len(pila) - 1])
    return pila[len(pila) - 1]


def sintacticoRmt():
    global char, tokens, fila, columna, palabra, i, estado, errores, eA, eB, eC, eD, eE, eF, pila, lastPila,pila_sintactico
    pila.clear()
    contadorTokens = 0
    pila.append("START")
    linea_sintaxis = ""
    while len(pila) != 0:

        if lastPila() == "START":
            print("Cambio START")
            pila.pop()
            if tokens[contadorTokens].tipo == "numero":
                print("es numero o variable")
                pila.append("OP")
                pila.append("V")
            elif tokens[contadorTokens].tipo == "variable":
                print("es numero o variable")
                pila.append("OP")
                pila.append("V")
            elif tokens[contadorTokens].tipo == "p_a":
                pila.append("OP")
                pila.append("p_c")
                pila.append("OP")
                pila.append("V")
                pila.append("p_a")

        elif lastPila() == "V":
            print("Cambio V")
            pila.pop()
            if tokens[contadorTokens].tipo == "numero":
                pila.append("numero")
            elif tokens[contadorTokens].tipo == "variable":
                pila.append("variable")

        elif lastPila() == "OP":
            print("Cambio OP")
            pila.pop()
            if tokens[contadorTokens].tipo == "signo":
                pila.append("OP")
                pila.append("V")
                pila.append("signo")
            else:
                pila.append("MOP")

        elif lastPila() == "MOP":
            print("Cambio MOP")
            pila.pop()
            if tokens[contadorTokens].tipo == "signo":
                pila.append("OP")
                pila.append("p_c")
                pila.append("OP")
                pila.append("V")
                pila.append("p_a")
                pila.append("signo")
        elif lastPila() == "#":
            print("Cambio #")
            pila.pop()
            break
        else:
            if lastPila() == tokens[contadorTokens].tipo:
                linea_sintaxis += tokens[contadorTokens].palabra
                pila.pop()
                contadorTokens += 1
            elif tokens[contadorTokens].tipo == "espacio":
                pila.clear()
                pila_sintactico.append(lexema(linea_sintaxis, "Correcta"))
                pila.append("#")
                pila.append("START")
                contadorTokens += 1
            else:
                while True:
                    linea_sintaxis += tokens[contadorTokens].palabra
                    contadorTokens += 1
                    if tokens[contadorTokens].tipo == "espacio":
                        pila_sintactico.append(lexema(linea_sintaxis, "Incorrecta"))
                        contadorTokens += 1
                        break
                    pass
                pass
                print(str(contadorTokens) + " pila len " + str(len(pila)))
                if contadorTokens != len(pila):
                    pila.clear()
                    pila.append("#")
                    pila.append("START")

        pass
    pass
    print("Termino Sintactico")

def imprimirSintac():
    global char, tokens, fila, columna, palabra, i, estado, errores, eA, eB, eC, eD, eE, eF, pila, lastPila,pila_sintactico
    print(" - - - Tokens - - -")
    if len(pila_sintactico) != 0:
        for x in pila_sintactico:
            print(x.palabra + " - " + x.tipo)