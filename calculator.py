# Libraries
from ast import Global
from distutils import command
from functools import partial
from pydoc import text
import tkinter as tk
from tkinter import *
import tkinter as ttk
from tkinter import messagebox
from setuptools import Command
#########
# APP CHARACTERISTICS
app = tk.Tk()
app.geometry('277x393')
app.title("Calculadora")
app.resizable(width=False, height=False)
app.iconbitmap("calc.ico")
app.configure(bg="#d3cfd0")

# GLOBAL VARIABLES
lastchar = ""
contadorDigits = 0
clearDisplayNextClick = False
operacionsCalc = ["C","<","/","*","-","+","=",".","(",")"]

#FUNCTIONS
def afegirdigit(d):
    global lastchar
    global contadorDigits
    contadorDigits += 1
    global clearDisplayNextClick
    if clearDisplayNextClick == True:
        clearDisplay()
        clearDisplayNextClick = False
    lastchar = d
    EntDisplay.configure(state='normal')
    EntDisplay.insert("end", d)
    EntDisplay.configure(state='readonly')

def afegirOperacioToEntry(op):
    EntDisplay.configure(state='normal')
    EntDisplay.insert("end", op)
    EntDisplay.configure(state='readonly')

def getLastCharDisplay():
    return EntDisplay.get()[-1]

def afegirOperacio(op): 
        global contadorDigits
        global lastchar
        global clearDisplayNextClick
        if clearDisplayNextClick == True:   
            clearDisplay()
            clearDisplayNextClick = False
        if lastchar in numerosCalc:
            contadorDigits+=1

        if op == ")":                           # CONTROLAR PARA CERRAR LOS ) DEPENDIENDO DE LOS ( QUE HAYA Y NO PASARSE.
            countobert = 0
            for item in EntDisplay.get():
                if item == "(":
                    countobert+=1
            counttancat = 0
            for item in EntDisplay.get():
                if item == ")":
                    counttancat += 1
            if counttancat<countobert and (getLastCharDisplay() not in operacionsCalc): # controlar que no me hagan esto (2+)
                    afegirOperacioToEntry(op)
            
            elif counttancat<countobert and getLastCharDisplay() == ")":        # poder cerrar mas de un parentesis a la vez
                afegirOperacioToEntry(op)
            
        else:
            if contadorDigits > 0:
                if (getLastCharDisplay() != "(" and getLastCharDisplay() != ")") and op == "(" and getLastCharDisplay() not in numerosCalc and getLastCharDisplay() != ".":
                    afegirOperacioToEntry(op)
                
                if op == "-" and getLastCharDisplay() == "(":       
                        afegirOperacioToEntry(op)

                if contadorDigits != 0 and clearDisplayNextClick == False and getLastCharDisplay() not in operacionsCalc or getLastCharDisplay() == ")": #Si el contador digitos no es 0 (para que no me añadan caracteres no validos al principio), y no reciba la centinella que tiene que borrar todo el entdisplay (solo se usara cuando des click a un digito despues de darle al igual), y que el ultimo carácter no sea igual a ningun operador, entonces cuando borremos hayan cuantos hayan cuando borremos y el utlimo sea un operador no nos dejará añadir, no nos dara error substring index porque tenemos un checkeo de contadordigits > 0 entonces siempre habra un valor en la posicio ultima
                    if op != ")" and getLastCharDisplay() == ")" and op != "(" and op != ".":
                        afegirOperacioToEntry(op)
                    elif op == "(" and (getLastCharDisplay() in numerosCalc or getLastCharDisplay() == ")"): #No permetir esta situacion: 25( si o si tiene k haber operador 25*(    y tampcoo permetir esto ()
                        pass
                    
                    elif op == "." and getLastCharDisplay() == ")": #No permetir poner . después de un )
                        pass
                    
                    else:
                        afegirOperacioToEntry(op)

        if (op == "-" or op == "(") and contadorDigits == 0:   #Esto es para que el caracter - se pueda al principio, no podremos ponerlo 2 veces seguidas ya que el if anterior a este lo limita
            afegirOperacioToEntry(op)
            contadorDigits += 1
        lastchar = op   #Cambiamos el valor al ultimo caracter

def popDisplay():
    global lastchar
    lastchar = "DELETED"    #Cambiamos el ultimo caracter para k no haga conflicto con las comprobaciones de arriba
    global clearDisplayNextClick
    if clearDisplayNextClick == True:   #Si despues de darle al "=" le damos a cualquier boton llama a la funcion de limpiar pantalla
        clearDisplay()
        clearDisplayNextClick = False
    EntDisplay.configure(state='normal')
    EntDisplay.delete(len(EntDisplay.get())-1)  #Borramos ultimo digito
    EntDisplay.configure(state='readonly')
    global contadorDigits
    contadorDigits = len(EntDisplay.get())  #Se hace esto para controlar los digitos que llevamos porque arriba si no ponemos esto, si hago esta oeracion 2- y luego borro el - y se queda el 2 no puedo volver a introducir ni -+*/

def calcular():
        global lastchar
        try:    #Intentamos calcular la operacion con eval y meterlo al entdisplay
            global clearDisplayNextClick
            clearDisplayNextClick = True
            operacio = EntDisplay.get()
            res = eval(EntDisplay.get())
            res = float(res)
            res = round(res, 8)
            res = str(res)
            if str(res)[-2:] == ".0": # Esto es por si me ponen 2 nums y el resultado da 0 que no haga 0.0 porque antes esta el float
                res = str(res)[0:-2]
            clearDisplay()
            showOperation(operacio)
            EntDisplay.configure(state='normal')
            EntDisplay.insert(0, res)
            EntDisplay.configure(state='readonly')
            global contadorDigits
            contadorDigits = 0
        except ZeroDivisionError:   #Si dividimos por 0 mostrará ese mensajito por pantalla
            clearDisplay()
            EntDisplay.configure(state='normal')
            EntDisplay.insert(0, "Zero Division Error")
            EntDisplay.configure(state='readonly')
        except:         #Si no pone lo que nos gusta como mucho podra hacer 2- y darle al igual pues printará 2- y al darle a cualquier boton de nuevo se reinicia el display
            clearDisplay()
            EntDisplay.configure(state='normal')
            EntDisplay.insert(0, "Syntax Error")
            EntDisplay.configure(state='readonly')
            pass
        finally:
            lastchar = "IGUAL"
 
def clearDisplay():
    global lastchar
    EntDisplay.configure(state='normal')    #Borrar el contenido entero del entdisplay, lo llamamos con el boton "C" o despues de darle a un boton despues de darle al igual
    EntDisplay.delete(0, END)
    EntDisplay.configure(state='readonly')
    if len(EntDisplay.get()) == 0:      #Se hace esto para controlar los digitos que llevamos porque arriba si no ponemos esto, si hago esta oeracion 2- y luego borro el - y se queda el 2 no puedo volver a introducir ni -+*/
        global contadorDigits
        contadorDigits = 0
    clearShowOperation()
    lastchar = "CLEAR"

def showOperation(res):
    EntEval.configure(text=res+"=")

def clearShowOperation():
    EntEval.configure(text="")

def makeButtonWithParameters(buttonNameParameter, functionParameter, functionParameterParameter, rowParameter, columnParameter):
    global operacionsCalc
    bg = "#67a1cf"
    fg = 'white'
    if buttonNameParameter in operacionsCalc:
        bg = '#828282'
        fg = 'black'
    ttk.Button(app, text=str(buttonNameParameter), command=partial(functionParameter, (functionParameterParameter)),width=3, height=1, font=(
        "Courier", 24), borderwidth=2, relief="groove", anchor=CENTER, bg=bg, fg=fg,).grid(row=rowParameter, column=columnParameter,padx=(2, 0), pady=(2, 0))

def makeButtonNoParameters(buttonNameParameter,functionParameter,rowParameter,columnParameter):
    ttk.Button(app, text=str(buttonNameParameter), command=partial(functionParameter),width=3, height=1, font=(
            "Courier", 24), borderwidth=2, relief="groove", anchor=CENTER,bg='#828282').grid(row=rowParameter, column=columnParameter,padx=(2, 0), pady=(2, 0))


# ENTRYS
EntEval = tk.Label(app, font=('Arial 12'),justify= RIGHT)
EntEval.grid(row=0, column=0,columnspan=46,sticky=tk.NE)
EntEval.configure(background="#d3cfd0",foreground="#373737")

EntDisplay = tk.Entry(app, state="readonly", font=('Arial 25'),justify= RIGHT,width=15)
EntDisplay.grid(row=1, column=0,columnspan=46,sticky=tk.NE)
EntDisplay.configure(background="gray",foreground="black")

# BUTTONS
numerosCalc = ["7", "8", "9", "4", "5", "6", "1", "2", "3", "0"]
x = 4  # Row
y = 0  # Column
# BUCLE PARA GENERAR DIGITOS
for button in numerosCalc:
    if button == "0":
        makeButtonWithParameters(button,afegirdigit,button,7,1)
    else:
        makeButtonWithParameters(button,afegirdigit,button,x,y)    
    y+=1
    if y == 3:
        y = 0
        x +=1

# BUCLE PARA GENERAR OTROS BOTONES PARA CALCULADORA

x = 3  # Row
y = 0 # Column
for item in operacionsCalc:
    if item == "=":  # Si es igual llama a calcular
        makeButtonNoParameters(item,calcular,x,y)
    elif item == "C": # Si es borrar pantalla llama a clear diplay para borrar pantlla
        makeButtonNoParameters(item,clearDisplay,x,y)
    elif item == "<":   # Si es borrar digito llama a popdisplay para borrar ultimo digito
        makeButtonNoParameters(item,popDisplay,x,y)    
    elif item == ".":
        makeButtonWithParameters(item,afegirOperacio,item,7,0)  
    elif item == "(":
        makeButtonWithParameters(item,afegirOperacio,item,7,2)
    elif item == ")":
        makeButtonWithParameters(item,afegirOperacio,item,x-2,y)
    else:      #Si no es ninguno de estos entonces es un operand k llaman todos a la misma funcion
        makeButtonWithParameters(item,afegirOperacio,item,x,y)

    if y != 4:
        y+=1
    
    if y == 4:
        y =3
        x+=1
        
app.mainloop()
