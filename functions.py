import matplotlib.pyplot as plt
import sympy as sp
from functions import *

class function:

    # -- Determine if the given function is rational or not -- #
    def isRational(self, expr):

        # Sympy parsing
        x = sp.symbols('x')
        numerator, denominator = sp.fraction(expr)

        # Find the zeros
        zeros = sp.solve(denominator, x)

        # Filter the ones where the denominator gets to 0
        asymp = [z for z in zeros if numerator.subs(x, z) != 0]

        # Return True or False depending on the case
        return len(asymp) > 0

    # -- Constructor-- #
    def __init__(self, area, expr=None, range_=300, step=0.2):
        self.area = area
        self.range = range_
        self.step = step
        self.expression = expr
        self.line = None
         
        #If the expression is passed correctly, then plot the function
        if expr is not None:
            self.plotFunction()

    # -- Logic to display the function -- #
    def plotFunction(self):

        # Parsing with the sympy syntax
        x = sp.symbols('x')
        expr = sp.sympify(self.expression)

        # For some reason, this is 10x times faster than sympify, so it's important for performance
        f_py = sp.lambdify(x, expr, 'math')

        # Checks if the given function is rational or not to change the logic's behaviour 
        # In case it's rational, it needs to have more accurate coordenates to display the asymptote,
        # EX: If the asympote is in x = 2. 
        # Then the program has to display points on coordenates getting close to x = 2, like x = 1.99999999.
        if self.isRational(expr):
            self.range = 200
            self.step = 0.005

        # -- GET X VALUES -- # 
        # # Equidistant points that go from -range to range, with (step) many divisions
        points = int(2*self.range / self.step) + 1
        x_vals = [round(-self.range + i * self.step, 4) for i in range(points)]

        # -- GET Y VALUES -- #
        # Evaluates F(X) with each X value, and adds it to the list. Unless it's None.
        y_vals = []
        for xv in x_vals:
            try:
                y_vals.append(f_py(xv))
            except (ZeroDivisionError, ValueError):
                y_vals.append(None)

        # Plots the function
        self.line, = self.area.plot(x_vals, y_vals, label=self.expression, lw=2.5)

        # -- INTERSECTIONS -- # 
        
        # -- Y -- #
        # Polinomic and rational functions only have one Y intersection, so it's easier 
        # evaluate the expression on X = 0
        y_intersec = f_py(0)
        try:
            self.area.plot([0], [y_intersec], 'o', label=f"Intersección Y:(0,{round(y_intersec, 4)})", color='green')
        except:
            pass

        # -- X -- #
        
        x_intersec = sp.solve(expr, x)
        x_points = []
        for intersec in x_intersec:
            intersec_eval = intersec.evalf()
            if intersec_eval.is_real:
                x_points.append(float(intersec_eval))

        # Plots all the intersections
        for i in x_points:
            self.area.plot([i], [0], 'o', label=f"Intersección X: ({round(i,4)},0)", color='green')

        self.area.legend()

