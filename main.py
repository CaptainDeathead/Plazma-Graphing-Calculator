import pygame as pg
from math import *
import random
import tkinter as tk

GRAPH_WIDTH = 800
GRAPH_HEIGHT = 800

pg.init()

screen = pg.display.set_mode((GRAPH_WIDTH, GRAPH_HEIGHT))
pg.display.set_caption("Plazma Graphing Calculator")

def configRoot(equations, colors):
    if len(equations) == 0:
        equations.append("sin(x)")
        colors.append("255, 0, 0")

    root = tk.Tk()
    root.geometry("600x400")
    root.title("Plazma Graphing Calculator Control")

    equationsLbl = tk.Label(root, text="Equations", font=("arial", 20))
    equationsLbl.pack()

    def addEquation():
        equations.append(equationEntry.get())
        colors.append(colorEntry.get())
        equationsList.insert(tk.END, equationEntry.get() + "    Color: " + colorEntry.get())
        equationEntry.delete(0, tk.END)
        colorEntry.delete(0, tk.END)
        equationEntry.focus()

    equationLbl = tk.Label(root, text="Enter Equation:", font=("arial", 15))
    equationLbl.pack()
    equationEntry = tk.Entry(root)
    equationEntry.pack()
    equationEntry.insert(0, equations[-1])
    equationEntry.focus()
    equationEntry.selection_range(0, tk.END)
    colorLbl = tk.Label(root, text="Enter Color:", font=("arial", 15))
    colorLbl.pack()
    colorEntry = tk.Entry(root)
    colorEntry.pack()
    colorEntry.insert(0, colors[-1])
    addEquationButton = tk.Button(root, text="Add Equation", command=lambda: addEquation())
    addEquationButton.pack()

    equationsList = tk.Listbox(root, width=50, height=10)
    equationsList.pack()

    for i, equation in enumerate(equations):
        equationsList.insert(tk.END, equation + "    Color: " + colors[i])

    calculateButton = tk.Button(root, text="Calcualate", command=lambda: window.submitEquation(equations, colors))
    calculateButton.pack()

    def removeEquation():
        equations.pop(equationsList.curselection()[0])
        colors.pop(equationsList.curselection()[0])
        equationsList.delete(equationsList.curselection()[0])

    root.bind('<Return>', lambda event: window.addEquation())
    equationsList.bind('<Button-3>', lambda event: removeEquation())

    return root, equationEntry

class Graph:
    def __init__(self):
        self.zoom = 10
        self.maxZoom = 350
        self.origin = (0,0)

class Window:
    def __init__(self):
        self.equations = ["sin(x)"]
        self.colors = ["255, 0, 0"]
        self.graph = Graph()
        self.font = pg.font.SysFont("arial", 10)
        self.root = None

    def run(self):
        running = True

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                elif event.type == pg.KEYDOWN:
                    if pg.key.get_pressed()[pg.K_q] and self.graph.zoom < self.graph.maxZoom:
                        self.graph.zoom *= 0.9
                    elif pg.key.get_pressed()[pg.K_e]:
                        self.graph.zoom *= 1.1
                    elif pg.key.get_pressed()[pg.K_SPACE]:
                        self.root, entry = configRoot(self.equations, self.colors)
                        self.root.focus_force()
                        entry.focus_force()
                        self.root.mainloop()
                        self.root = None

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 4 and self.graph.zoom < self.graph.maxZoom:
                        self.graph.zoom *= 1.1
                    elif event.button == 5:
                        self.graph.zoom *= 0.9

            pg.display.set_caption(f"Plazma Graphing Calculator    |    Press 'space' for ui    |    Zoom: {round(self.graph.zoom, 1)}x")

            self.drawGraph()
            for i, equation in enumerate(self.equations):
                self.drawEquation(equation, self.colors[i])
            pg.display.flip()
            #pg.time.delay(100000)
            #running = False

    def submitEquation(self, equations, colors):
        self.equations = equations
        self.colors = colors
        self.root.destroy()
        self.root = None

    def drawEquation(self, equation, color):
        equation = equation.replace("^", "**")
        
        originx = self.graph.origin[0] + 400
        originy = self.graph.origin[1] + 400

        try:
            color = tuple(eval(color))
        except:
            color = (255, 255, 255)

        x = int((self.graph.origin[0]-400)/self.graph.zoom)
        #y = int((self.graph.origin[1]-400)/self.graph.zoom)

        points = []

        while x < int((self.graph.origin[0]+400)/self.graph.zoom):
            try:
                y = eval(equation) * self.graph.zoom
            except Exception as e:
                newFont = pg.font.SysFont("arial", 25)
                screen.blit(newFont.render(f"Invalid Equation: {e}", 0, (255, 0, 0)), (50, 300))
                return
            y += 400
            y = GRAPH_HEIGHT - y
            ogx = x
            x *= self.graph.zoom
            x += 400
            if y < GRAPH_HEIGHT and y > 0:
                pg.display.update(screen.set_at((min(GRAPH_WIDTH, int(x)), min(GRAPH_HEIGHT, int(y))), color))
            points.append((x, y))
            #print(x, y)
            x = ogx
            x += 10/self.graph.zoom

        lines = []

        for i, point in enumerate(points):
            if point[1] < GRAPH_HEIGHT and point[1] > 0:
                lines.append((point[0], point[1]))

                try:
                    pg.draw.line(screen, color, (point[0], point[1]), (points[i+1][0], points[i+1][1]), 2)
                except:
                    pass

    def drawGraph(self):
        f = screen.fill((0,0,0))
        originx = self.graph.origin[0] + 400
        originy = self.graph.origin[1] + 400

        pg.draw.line(screen, (170, 170, 170), (0, originy), (GRAPH_WIDTH, originy), 2)
        pg.draw.line(screen, (170, 170, 170), (originx, 0), (originx, GRAPH_HEIGHT), 2)

        x = int((self.graph.origin[0]-400)/self.graph.zoom)
        y = int((self.graph.origin[1]-400)/self.graph.zoom)

        while x < int((self.graph.origin[0]+400)/self.graph.zoom):
            xnum = self.font.render(str(round(x, 2)), 0, (255, 255, 255))
            xnum = screen.blit(xnum, (x*self.graph.zoom+400, originy+5))
            x += 70 / self.graph.zoom

        while y < int((self.graph.origin[1]+400)/self.graph.zoom):
            ynum = self.font.render(str(round(-y, 2)), 0, (255, 255, 255))
            ynum = screen.blit(ynum, (originx+5, y*self.graph.zoom+400))
            y += 70 / self.graph.zoom

if __name__ == "__main__":
    window = Window()
    window.run()