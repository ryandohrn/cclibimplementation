import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import numpy as np
import pickle
from tkinter import *
import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import sys

tryp=False

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.createWidgets()

    def createWidgets(self):
        fig = plt.figure(figsize=plt.figaspect(1.75))
        fig2 = plt.figure(figsize=plt.figaspect(1.5))
        axev = fig.add_subplot(2,1,1)
        axev.set_ylabel('eV')
        axev.axes.get_xaxis().set_ticks([])
        axev.axes.get_xaxis().set_ticklabels([])
        axnm = fig.add_subplot(2,1,2)
        axnm.set_ylabel('nm')
        axnm.set_xlabel('Structure #')
        #axnm.axes.get_xaxis().set_ticks([])
        #axnm.axes.get_xaxis().set_ticklabels([])
        axf = fig2.add_subplot(1,1,1)
        axf.set_ylabel('f')
        axf.set_xlabel('Structure #')

        options = dict(sticky=NSEW, padx=3, pady=4)

        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(1, weight=1)

        framea = tk.Frame(root, height=510, width=770)
        framea.grid(row=0, column=0, **options)

        frameb = tk.Frame(root, height=510, width=770)
        frameb.grid(row=0, column=1, **options)

        frame1 = tk.Frame(root, height=510, width=770)
        frame1.grid(row=1, column=0, **options)

        frame2 = tk.Frame(root, height=510, width=770)
        frame2.grid(row=1, column=1, **options)

#        frame1 = tk.Frame(frame)
#        frame1.grid(row=2, column=1, sticky='nsew')
#        frame1.columnconfigure(0, weight=1)
#        frame1.rowconfigure(0, weight=1)
#        frame2 = tk.Frame(frame)
#        frame2.grid(row=2, column=2, sticky='nsew')
#        frame2.columnconfigure(0, weight=1)
#        frame2.rowconfigure(0, weight=1)
#        frameb = tk.Frame(frame)
#        frameb.grid(row=1, column=2, sticky='nsew')
#        frameb.columnconfigure(0, weight=1)
#        frameb.rowconfigure(0, weight=1)

        canvas=FigureCanvasTkAgg(fig, master=frame1)
#        canvas.get_tk_widget().grid(row=3, column=1, **options)
#        canvas.get_tk_widget().grid_columnconfigure(0, weight=1)
#        canvas.get_tk_widget().grid_rowconfigure(0, weight=1)
        canvas.show()
        canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        canvas2=FigureCanvasTkAgg(fig2, master=frame2)
#        canvas2.get_tk_widget().grid(row=3, column=2, **options)
#        canvas2.get_tk_widget().grid_columnconfigure(0, weight=1)
#        canvas2.get_tk_widget().grid_rowconfigure(0, weight=1)
        canvas2.show()
        canvas2.get_tk_widget().pack(side='top', fill='both', expand=1)
#        self.fcanvas = tk.Frame()
#        self.fcanvas.pack(side="top", fill="both", expand=True)
#        self.fcanvas.grid_columnconfigure(0, weight=1)
#        self.fcanvas.grid_rowconfigure(0, weight=1)
#        self.fcanvas2 = tk.Frame()
#        self.fcanvas2.pack(side="bottom", fill="both", expand=True)
#        self.fcanvas2.grid_columnconfigure(0, weight=1)
#        self.fcanvas2.grid_rowconfigure(0, weight=1)

#        canvas.get_tk_widget().grid(in_=self.fcanvas, sticky=NSEW)
#        canvas2.get_tk_widget().grid(in_=self.fcanvas2, sticky=NSEW)

        n=0
        for dataset in datalist:
            n+=1

        self.w = tk.Scale(master=framea, from_=1, to=n-1, orient=HORIZONTAL, command=lambda v:self.plotev(canvas, canvas2, axev, axnm, axf, self.w.get(),True, False))
        self.w.grid(row=0, column=0, **options)
        sval = self.w.get()

        self.plotev(canvas, canvas2, axev, axnm, axf, 1, False, True)
        self.plotbutton = tk.Button(master=frameb, text="show molecule structure", command=lambda :self.ploto(self.w.get()))
        self.plotbutton.grid(row=0, column=1, **options)
        #self.plottoggle = tk.Button(master=root, text="hide structure line", command=lambda:self.plotev(canvas, canvas2, axev, axnm, axf, self.w.get(), False, False))
        #self.plottoggle.grid(row=2, column=2)

    def plotline(self, canvas, canvas2, axev, axnm, axf, sval, toggle):

        if toggle==True:
            line = axev.plot([sval, sval], [ye1[sval], ye6[sval]])
            line = axnm.plot([sval, sval], [yn1[sval], yn6[sval]])
            line = axf.plot([sval, sval], [yf1[sval], yf6[sval]])
        else:
            print ('oopsies')

    def plotev(self, canvas, canvas2, axev, axnm, axf, sval, toggle, start):

        xs = []
        ye1 = []
        ye2 = []
        ye3 = []
        ye4 = []
        ye5 = []
        ye6 = []
        yn1 = []
        yn2 = []
        yn3 = []
        yn4 = []
        yn5 = []
        yn6 = []
        yf1 = []
        yf2 = []
        yf3 = []
        yf4 = []
        yf5 = []
        yf6 = []
        n = 0
        for dataset in datalist:
            n+=1
            xs.append(n)
            for group in dataset[1]:
                if group[2]=='1':
                    ye1.append(group[4])
                    yn1.append(group[6])
                    yf1.append(group[8])
                elif group[2]=='2':
                    ye2.append(group[4])
                    yn2.append(group[6])
                    yf2.append(group[8])
                elif group[2]=='3':
                    ye3.append(group[4])
                    yn3.append(group[6])
                    yf3.append(group[8])
                elif group[2]=='4':
                    ye4.append(group[4])
                    yn4.append(group[6])
                    yf4.append(group[8])
                elif group[2]=='5':
                    ye5.append(group[4])
                    yn5.append(group[6])
                    yf5.append(group[8])
                elif group[2]=='6':
                    ye6.append(group[4])
                    yn6.append(group[6])
                    yf6.append(group[8])
        if start==True:

            axev.plot(xs, ye1, c='#b92638')
            axev.plot(xs, ye2, c='#bd8700')
            axev.plot(xs, ye3, c='#329932')
            axev.plot(xs, ye4, c='#00b3b3')
            axev.plot(xs, ye5, c='#4d4dff')
            axev.plot(xs, ye6, c='#ba55d3')
            axev.plot(xs, ye6, c='#ba55d3')
            axnm.plot(xs, yn1, c='#b92638')
            axnm.plot(xs, yn2, c='#bd8700')
            axnm.plot(xs, yn3, c='#329932')
            axnm.plot(xs, yn4, c='#00b3b3')
            axnm.plot(xs, yn5, c='#4d4dff')
            axnm.plot(xs, yn6, c='#ba55d3')
            axnm.plot(xs, yn6, c='#ba55d3')
            axf.plot(xs, yf1, c='#b92638')
            axf.plot(xs, yf2, c='#bd8700')
            axf.plot(xs, yf3, c='#329932')
            axf.plot(xs, yf4, c='#00b3b3')
            axf.plot(xs, yf5, c='#4d4dff')
            axf.plot(xs, yf6, c='#ba55d3')
            axf.plot(xs, yf6, c='#ba55d3')
        elif toggle==True:
            try:
                axev.lines.pop()
                axnm.lines.pop()
                axf.lines.pop()
            except:
                pass
            try:
                line = axev.plot([sval, sval], [ye1[sval], ye6[sval]])
                line = axnm.plot([sval, sval], [yn1[sval], yn6[sval]])
                line = axf.plot([sval, sval], [0,0.126])
            except:
                print ('fuck')
        else:
            pass
        canvas.draw()
        canvas2.draw()
    def plotnm(self, canvas, ax, sval, toggle):
        sval-=1
        try:
            ax.lines.pop()
        except:
            pass
        plt.ylabel('nm')
        plt.xlabel('Structure #')
        xs = []
        y1 = []
        y2 = []
        y3 = []
        y4 = []
        y5 = []
        y6 = []
        n = 0
        for dataset in datalist:
            n+=1
            xs.append(n)
            for group in dataset[1]:
                if group[2]=='1':
                    y1.append(group[6])
                elif group[2]=='2':
                    y2.append(group[6])
                elif group[2]=='3':
                    y3.append(group[6])
                elif group[2]=='4':
                    y4.append(group[6])
                elif group[2]=='5':
                    y5.append(group[6])
                elif group[2]=='6':
                    y6.append(group[6])
        ax.plot(xs, y1, c='#b92638')
        ax.plot(xs, y2, c='#bd8700')
        ax.plot(xs, y3, c='#329932')
        ax.plot(xs, y4, c='#00b3b3')
        ax.plot(xs, y5, c='#4d4dff')
        ax.plot(xs, y6, c='#ba55d3')

        if toggle==True:
            line = ax.plot([sval, sval], [y1[sval], y6[sval]])
        else:
            pass

        canvas.draw()

    def ploto(self, struc):
        fig3 = plt.figure(figsize=plt.figaspect(1))
        ax3 = fig3.add_subplot(1,1,1, projection='3d')
        ax3.set_axis_off()
        groupval = []
        g = 0
        xcvals = []
        ycvals = []
        zcvals = []
        xhvals = []
        yhvals = []
        zhvals = []
        xnvals = []
        ynvals = []
        znvals = []
        xovals = []
        yovals = []
        zovals = []
        ele = []
        col = []

        for dataset in datalist:
            g+=1
            groupval.append(g)
            atoms = 0
            xco = []
            yco = []
            zco = []
            xho = []
            yho = []
            zho = []
            xno = []
            yno = []
            zno = []
            xoo = []
            yoo = []
            zoo = []
            for group in dataset[0]:
                atoms+=1
                if group[1]=='1':
                    xho.append(float(group[3]))
                    yho.append(float(group[4]))
                    zho.append(float(group[5]))
                    ele.append("H")
                    col.append("#00b3b3")
                elif group[1]=='6':
                    xco.append(float(group[3]))
                    yco.append(float(group[4]))
                    zco.append(float(group[5]))
                    ele.append("C")
                    col.append("#329932")
                elif group[1]=='7':
                    xno.append(float(group[3]))
                    yno.append(float(group[4]))
                    zno.append(float(group[5]))
                    ele.append("N")
                    col.append("#4d4dff")
                else:
                    xoo.append(float(group[3]))
                    yoo.append(float(group[4]))
                    zoo.append(float(group[5]))
                    ele.append("O")
                    col.append("#4d4ddd")
            xhvals.append(xho)
            yhvals.append(yho)
            zhvals.append(zho)
            xcvals.append(xco)
            ycvals.append(yco)
            zcvals.append(zco)
            xnvals.append(xno)
            ynvals.append(yno)
            znvals.append(zno)
            xovals.append(xoo)
            yovals.append(yoo)
            zovals.append(zoo)
        if atoms>=18:
            tryp = True
        elif atoms<=17:
            tryp = False
        sval = struc - 1
        xco=xcvals[sval]
        yco=ycvals[sval]
        zco=zcvals[sval]
        xho=xhvals[sval]
        yho=yhvals[sval]
        zho=zhvals[sval]
        xno=xnvals[sval]
        yno=ynvals[sval]
        zno=znvals[sval]

        x1=[]
        y1=[]
        z1=[]

        ax3.scatter(xcvals[sval],ycvals[sval],zcvals[sval], marker='o', s=130, facecolor="#329932", label='C')
        ax3.scatter(xhvals[sval],yhvals[sval],zhvals[sval], marker='o', s=130, facecolor="#00b3b3", label='H')
        ax3.scatter(xnvals[sval],ynvals[sval],znvals[sval], marker='o', s=130, facecolor="#4d4dff", label='N')


        if tryp==True:
            xoo=xovals[sval]
            yoo=yovals[sval]
            zoo=zovals[sval]
            print ("X: ", xcvals[sval], xhvals[sval], xnvals[sval], xovals[sval])
            print ("Y: ", ycvals[sval], yhvals[sval], ynvals[sval], yovals[sval])
            print ("Z: ", zcvals[sval], zhvals[sval], znvals[sval], zovals[sval])
            x1 = [xco[1],xco[2],xco[3],xho[1],xco[3],xco[4],xho[2],xco[4],xco[5],xho[3],xco[5],xco[0],xho[0],xco[0],xco[1],xno[0],xho[11],xno[0],xco[7],xho[4],xco[7],xco[6],xco[2],xco[6],xco[8],xho[5],xco[8],xho[6],xco[8],xco[9],xno[1],xho[9],xno[1],xho[10],xno[1],xco[9],xho[7],xco[9],xco[10],xho[8]]
            y1 = [yco[1],yco[2],yco[3],yho[1],yco[3],yco[4],yho[2],yco[4],yco[5],yho[3],yco[5],yco[0],yho[0],yco[0],yco[1],yno[0],yho[11],yno[0],yco[7],yho[4],yco[7],yco[6],yco[2],yco[6],yco[8],yho[5],yco[8],yho[6],yco[8],yco[9],yno[1],yho[9],yno[1],yho[10],yno[1],yco[9],yho[7],yco[9],yco[10],yho[8]]
            z1 = [zco[1],zco[2],zco[3],zho[1],zco[3],zco[4],zho[2],zco[4],zco[5],zho[3],zco[5],zco[0],zho[0],zco[0],zco[1],zno[0],zho[11],zno[0],zco[7],zho[4],zco[7],zco[6],zco[2],zco[6],zco[8],zho[5],zco[8],zho[6],zco[8],zco[9],zno[1],zho[9],zno[1],zho[10],zno[1],zco[9],zho[7],zco[9],zco[10],zho[8]]

        elif tryp==False:
            x1 = [xco[5],xco[2],xco[1],xho[2],xco[1],xco[0],xho[1],xco[0],xco[3],xho[3],xco[3],xco[4],xho[4],xco[4],xco[5],xno[0],xho[0],xno[0],xco[7],xho[6],xco[7],xco[6],xho[5],xco[6],xco[2]]
            y1 = [yco[5],yco[2],yco[1],yho[2],yco[1],yco[0],yho[1],yco[0],yco[3],yho[3],yco[3],yco[4],yho[4],yco[4],yco[5],yno[0],yho[0],yno[0],yco[7],yho[6],yco[7],yco[6],yho[5],yco[6],yco[2]]
            z1 = [zco[5],zco[2],zco[1],zho[2],zco[1],zco[0],zho[1],zco[0],zco[3],zho[3],zco[3],zco[4],zho[4],zco[4],zco[5],zno[0],zho[0],zno[0],zco[7],zho[6],zco[7],zco[6],zho[5],zco[6],zco[2]]
            print ("X: ", xcvals[sval], xhvals[sval], xnvals[sval])
            print ("Y: ", ycvals[sval], yhvals[sval], ynvals[sval])
            print ("Z: ", zcvals[sval], zhvals[sval], znvals[sval])

        ax3.plot(x1,y1,z1)
        ax3.legend()
        fig3.show()
        return 13

infilename = filedialog.askopenfilename()
infile = open(infilename, "rb+")
datalist = pickle.load(infile)

root=tk.Tk()
app=Application(master=root)

app.mainloop()
