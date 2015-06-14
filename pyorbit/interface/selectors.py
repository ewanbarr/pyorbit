import Tkinter as tk
import numpy as np
from pyorbit.core.utils import rad2arcmin,arcmin2rad

class Selector(tk.Frame):
    def __init__(self,parent,text,units,to_units,from_units,default=0.0):
        tk.Frame.__init__(self,parent)
        self.parent = parent
        self._select_var = tk.BooleanVar()
        self._select_var.set(False)
        self._select = tk.Checkbutton(self,onvalue=True,offvalue=False,variable=self._select_var)
        self._label = tk.Label(self,text=text,width=10,justify=tk.RIGHT)
        self._units = tk.Label(self,text=units,width=7,justify=tk.LEFT)
        self._entry_var = tk.StringVar()
        self._entry_var.set(str(default))
        validator = self.register(self.validator)
        self._entry = tk.Entry(self,textvariable=self._entry_var, validate='all',
                               validatecommand=(validator,'%P'), width=15)
        self._label.pack(side=tk.LEFT,fill=tk.BOTH)
        self._entry.pack(side=tk.LEFT,fill=tk.BOTH)
        self._units.pack(side=tk.LEFT,fill=tk.BOTH)
        self._select.pack(side=tk.LEFT,fill=tk.BOTH)
        self.to_units = to_units
        self.from_units = from_units

    def _set_bg(self,c):
        try:
            self._entry.config(background=c)
        except:
            pass

    def validator(self,val):
        try:
            float(val+"0")
            self._set_bg('white')
            return True
        except:
            self._set_bg('red')
            self.bell()
            self.after(250,lambda:self._set_bg('white'))
            return False

    def is_selected(self):
        return self._select_var.get()
    
    def set_value(self,value):
        self._entry.set("%.9g"%str(self.to_units(value)))

    def get_value(self):
        return self.from_units(float(self._entry.get()))
    

class SelectorPanel(tk.Frame):
    def __init__(self,parent,parameters):
        tk.Frame.__init__(self,parent)
        self.parent = parent
        self.params = parameters
        self.init()

    def init(self):
        self.selectors = {}
        for key,text,units,to_units,from_units in self.params:
            self.selectors[key] = Selector(self,text,units,to_units,from_units)
            self.selectors[key].pack()

if __name__ == "__main__":
    root = tk.Tk()
    params = [("ra_offset","RA offset","arcmin",rad2arcmin,arcmin2rad),
              ("dec_offset","Dec offset","arcmin",rad2arcmin,arcmin2rad),
              ("p0","Period","ms",lambda x:x*1000.0,lambda x:x/1000.0),
              ("p1","P-dot","s/s",lambda x:x,lambda x:x)]
    panel = SelectorPanel(root,params)
    panel.pack()

    def printit():
        for sel in panel.selectors.values():
            print sel.get_value()

    tk.Button(root,text="Get",command=printit).pack()
    root.mainloop()

        

