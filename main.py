from tkinter import *
import tkinter.scrolledtext as st 
import tkinter.messagebox as ms
import abrir

root = Tk()
root.config(bg="gray")
root.title("ML WEB")
root.geometry('940x415')

# btn = Button(root, text="Click Me", command=clicked)
# btn.grid(column=2, row=0)

def salir():
    ms.showinfo(message="saliendo",title="Orale")
    root.destroy()

tag1 = "palabra_Reservada"
#Text Area
codigo = st.ScrolledText(root,width = 70,height = 25 , bg = "light blue") 
codigo.grid(column = 0,row =1, pady = 20, padx = 10) 
# Texto y Colores
# codigo.insert(INSERT, "Ehila \n", "'" + tag1 + "'")
# codigo.tag_config("'" + tag1 + "'", foreground='orange') 

#Text Area
errores = st.ScrolledText(root,width = 50,height = 25,bg = "black") 
errores.grid(column = 1,row =1, pady = 20, padx = 10) 

# Making the text read only 
# codigo.configure(state ='disabled')  
# errores.configure(state ='disabled')  

def _abrir():
    abrir.abrir(codigo,errores)
    if abrir.archivo != "":
        ms.showinfo(message="Archivo Cargado",title="Analisis Listo")

def _analisis():
    if abrir.archivo != "":
        abrir.analisis(codigo,errores)
    else:
        ms.showinfo(message="Primer Abre un Archivo",title="Advertencia")

menubar = Menu(root,bg="black",fg="white")
root.config(menu=menubar)
#Menu
# menubar.add_command(label="Nuevo")
menubar.add_command(label="Abrir",command=_abrir)
# menubar.add_command(label="Guardar")
menubar.add_command(label="Ejecutar Analisis",command=_analisis)
# menubar.add_command(label="Reportes")
menubar.add_command(label="Salir",command=salir)

root.mainloop()
