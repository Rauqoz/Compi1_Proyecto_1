cadena = "/******************************************************************* ============================================================== ** ============================================================== ** ============================================================== * * ===================ARCHIVO DE PRUEBA DE JS==================== * * ============================================================== * * ================PATHL -> /home/user/output/js/================ * * ============================================================== * * ============================================================== * * ============================================================== * ******************************************************************/"

encontrar = cadena.find("PATHL ->") + len("PATHL ->")
parte1 = cadena[encontrar:].replace("user","rau")
encontrar2 = parte1.find("=")
print(parte1[:encontrar2])
