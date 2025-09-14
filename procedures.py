import sympy as sp

x, y = sp.symbols('x y')

def y_intersection(expr):
    # Parsing the expresion and getting the Y when X equals 0
    expr = sp.sympify(expr)
    y_val = expr.subs(x, 0).evalf()
    # Explaining and storing into text to return
    text = f"Intersección con el Eje Y: \n F(0) = {expr} \n Y = {str(expr).replace('x','(0)')} \n Y = {round(float(y_val), 3)}\n \n"
    return text
    
def x_intersection(expr):
    x = sp.symbols('x')
    expr = sp.sympify(expr)
    x_intersec = sp.solve(expr, x)

    x_points = []
    for root in x_intersec:
        root_eval = root.evalf()
        if root_eval.is_real:  # solo raíces reales
            x_points.append(float(root_eval))

    text = ""
    if x_points:
        for i in x_points:
            text += f"Intersección con el Eje X: \n f(x) = 0 \n 0 = {expr} \n x = {round(i, 2)}\n\n"
    else:
        text += "No hay intersecciones reales con el Eje X.\n"
    
    return text

def domain(expr):

    # Parsing the expresion and separating numerator and denominator (if there is one)
    expr = sp.sympify(expr)
    numer, denom = sp.fraction(expr)
    text = ""

    # Find all the zeroes on the denominator, which is equivalent to dividing by zero
    zeros = sp.solve(denom, x)

    # If there are zeroes, show them
    if zeros:
        text += f"DOMINIO: Todos los Reales excepto x = {', '.join([str(round(float(z.evalf()), 2)) for z in zeros])}\n"
        text += f"Porque {str(denom).replace("x",f"({zeros[0]})")} = 0 \n \n"

    # If not, end the text
    else:
        text+= "DOMINIO: Todos los Reales \n\n"
    
    text += f"Calculo del dominio:\n1.-Si el denominador es igual a 1, entonces la función es polinomica y por definicion, el dominio son todos los reales\n2-En caso contrario, se calcula que valores de x llevan a una indefinición \n"

    return text

def range_(expr):
    expr = sp.sympify(expr)
    x = sp.symbols('x')
    numer, denom = sp.fraction(expr)
    text = ""

    # Find vertical asymptotes
    asymp = sp.solve(denom, x)
    real_asymp = [z.evalf() for z in asymp if z.is_real]

    # Limits on +/- infinite
    try:
        lim_pos_inf = sp.limit(expr, x, sp.oo)
        lim_neg_inf = sp.limit(expr, x, -sp.oo)
    except:
        lim_pos_inf, lim_neg_inf = None, None

    # Show the range
    text += "\nRECORRIDO: \n"
    if real_asymp:
        text += f"Función con asíntotas en x = {', '.join([str(round(a,2)) for a in real_asymp])}\n"

    text += f"Límite cuando x → ∞: {lim_pos_inf}\n"
    text += f"Límite cuando x → -∞: {lim_neg_inf}\n\n"

    # Explaining the procedure
    text += "Cálculo del recorrido:\n"
    text += "1.- Identificar asíntotas verticales (valores que hacen el denominador 0)\n"
    text += "2.- Calcular los límites en ±∞ para determinar el comportamiento extremo\n"
    text += "3.- Analizar intervalos entre asíntotas para determinar todos los valores posibles de y\n"

    return text


def fullExplanation(expr):
    return "Procedimiento completo: \n \n" + y_intersection(expr) + x_intersection(expr) + domain(expr) + range_(expr)
