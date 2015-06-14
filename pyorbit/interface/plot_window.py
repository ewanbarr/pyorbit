import Tkinter as tk
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

RESID_DTYPE = [
    ("idx","int32"),
    ("residual","float32"),
    ("error","float32"),
    ("epoch","float32"),
    ("phase","float32")
    ]

class PlotWindow(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        self.parent = parent
        self.fig = mpl.figure.Figure()
        self.axes = self.setup_axes()
        self.canvas = FigureCanvasTkAgg(self.fig,self.parent)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas,self.parent)
        self.toolbar.update()
        self.toolbar.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.show()

    def setup_axes(self):
        ax = self.fig.add_subplot(111)
        return [ax]

    def draw(self):
        self.canvas.draw()


class Residual(object):
    def __init__(self,ax,idx,res,epoch,phase,err):
        self.ax = ax
        self.idx = idx
        self.residual = res
        self.epoch = epoch
        self.phase = phase
        self.error = err
        self.params = {
            "marker":"o",
            "ls":"",
            "picker":5,
            "c":"b"
            }
        self.selected = False
        self.plot()

    def plot(self):
        self.artist = self.ax.errorbar(self.residual,self.epoch,yerr=self.error,**self.params)
        self.artist._parent = self
        
    def __del__(self):
        self.artist.remove()

    def onclick(self):
        if self.selected:
            self.artist.set_markerfacecolor("blue")
            self.selected = False
        else:
            self.artist.set_markerfacecolor("red")
            self.selected = True
    


class ResidualsPlot(PlotWindow):
    def __init__(self,parent):
        PlotWindow.__init__(self,parent)
        self.data = None
        self.mask = None
        self.x_axis = "epoch"
        self.ax = self.axes[0]
        self.fig.canvas.mpl_connect('pick_event', self.onpick)
        self.residuals = []

    def get_data(self):
        start,end = self.ax.get_xlim()
        bottom,top = self.ax.get_ylim()
        ar = self.data[self.mask]
        idx = np.where((ar[self.x_axis]>start) & 
                       (ar[self.x_axis]<end) &
                       (ar["residual"]>bottom) &
                       (ar["residual"]>top))
        return ar[idx]
    
    def set_data(self,residual,error,epoch,phase):
        idxs = np.arange(residual.size)
        self.data = np.array(zip(idxs,residual,error,epoch,phase),dtype=RESID_DTYPE)
        self.mask = np.ones(self.data.size).astype("bool")
    
    def plot(self):
        ar = self.data[self.mask]
        for residual in self.residuals:
            del residual
        for row in ar:
            res = Residual(self.ax,ar["idx"],ar["residual"],ar["epoch"],ar["phase"],ar["error"])
            self.residuals.append(res)
            
    def onpick(self,event):
        print event.artist
        print event.ind
        self.residuals[event.ind].onclick()
        self.draw()

if __name__ == "__main__":
    root = tk.Tk()
    viewer = ResidualsPlot(root)
    viewer.pack()
    a = np.arange(10)
    viewer.set_data(a,a,a,a)
    viewer.plot()    
    viewer.draw()
    root.mainloop()
