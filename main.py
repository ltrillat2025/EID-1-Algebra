import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
import sympy as sp
from procedures import *
from functions import *

##---------- SETTING UP THE WINDOW ----------##

mpl.rcParams['toolbar'] = 'None' #Hides the default toolbar
window, function_area = plt.subplots(figsize=(1700/100, 960/100), dpi=100) #Creates the window and the function area window
function_area.set_position([0.06, 0.15, 0.55, 0.8]) #Adjust the window's placement

## -- Setting up the GUI axes/positions -- ##
GUI_axes= {
    "funcion" : plt.axes([0.14, 0.05, 0.15, 0.03]), "punto" : plt.axes([0.34, 0.05, 0.09, 0.03]),
     "zoom-in" : plt.axes([0.47, 0.05, 0.05, 0.03]),
    "zoom-out" : plt.axes([0.55, 0.05, 0.05, 0.03])
}

## -- Two Input boxes -- ##
function_input = TextBox(GUI_axes["funcion"],label="Función: ")
evaluate_input = TextBox(GUI_axes["punto"],label="X= ")

## -- Zoom In and Out buttons -- ##
zoomIn_button = Button(GUI_axes["zoom-in"], label="zoom-in")
zoomOut_button = Button(GUI_axes["zoom-out"], label="zoom-out")

## -- Creates the console that shows the entire procedure -- ## 
console = window.text(
    0.63, 0.945,  
    "a",
    va='top',
    ha='left',
    fontdict={'family':'monospace', 'size':12, 'weight':'bold', 'color':'darkblue'},
    wrap=True,
    multialignment='left',
    bbox={'facecolor':'white', 'alpha':0.8, 'edgecolor':'black'}
)
initialText = 'Para graficar una función, el formato es el siguente \n -Exponencial: "x**2" \n -Multiplicacion y División: "x*2" y "x/2" \n -Suma "x+2"\n\nPara operar polinomios, importante utilizar paréntesis \n Ejemplo (x**2+10*x+30)/(x+15) \n\nFunciones aceptadas: Polinómicas y Racionales\n\n\n'


##---------- USER INTERACTION ----------##

zoom = 100
displayFunction = None #Stores the current function
displayPoint = None #Stores the current X point

## -- Creating the Function for Each button/submit
def FunctionSubmit(texto):
    global zoom, displayFunction, initialText

    ##Clears up the area
    function_area.cla()

    #Shows the (0,0) Lines for reference
    function_area.axhline(0, color='black', linewidth=1)  
    function_area.axvline(0, color='black', linewidth=1)  

    #Resets the zoom
    function_area.set_xlim(-zoom, zoom)
    function_area.set_ylim(-zoom, zoom)

    #Creates the function
    try:
        displayFunction = function(expr=texto, area=function_area)
    except:
        pass

    # Draws the grid again
    function_area.grid(True)
    function_area.figure.canvas.draw()

    # Shows the procedures (calling procedures.py)
    try:
        console.set_text(initialText + fullExplanation(displayFunction.expression))
    except:
        pass

    plt.show()

def EvaluateSubmit(texto):
    global displayFunction, displayPoint

    ## Clears up the area
    function_area.cla()

    ## Finds the expression
    x = sp.symbols('x')
    expr = sp.sympify(displayFunction.expression)

    ## Stores X and Y values
    try:
        point_x = float(texto)
        point_y = expr.subs(x, point_x).evalf()
    except:
        pass

    ## Re-Displays the function
    # (This isn't optimal, but I didn't find any other way)
    FunctionSubmit(expr)

    ## Displays the point evaluated
    try:
        displayPoint = function_area.plot([point_x], [point_y], 'ro', label=f"({point_x},{round(float(point_y),2)})")
        function_area.legend()
    except:
        pass

def ZoomIn(event):
    global zoom
    # If greater than minimum zoom level, decrease the range of visibility #
    if zoom > 5:
        zoom-=5
    
    # Adjust the window to the zoom level #
    function_area.set_xlim(-zoom, zoom)
    function_area.set_ylim(-zoom, zoom)
    plt.show()

def ZoomOut(event):
    global zoom
    # If less than maximum zool level, increase the range of visibility #
    if zoom < 1000:
        zoom += 5
    function_area.set_xlim(-zoom, zoom)
    function_area.set_ylim(-zoom, zoom)
    plt.show()

# -- Assigning each function to each button/submit -- #
function_input.on_submit(FunctionSubmit)
evaluate_input.on_submit(EvaluateSubmit)
zoomIn_button.on_clicked(ZoomIn)
zoomOut_button.on_clicked(ZoomOut)

# -- Initial Display -- #
console.set_text(initialText)
function_area.set_xlim(-zoom, zoom)
function_area.set_ylim(-zoom, zoom)
function_area.axhline(0, color='black', linewidth=1)  
function_area.axvline(0, color='black', linewidth=1)  
function_area.grid(True)
function_area.figure.canvas.draw()
plt.legend()
plt.show()



