import tkinter as tk
from tkinter import ttk

class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        #x, y, _, _ = self.widget.bbox("insert")
        #x += self.widget.winfo_rootx() + 25
        #y += self.widget.winfo_rooty() + 25
        # Calcula la posición del widget en la ventana principal
        x = self.widget.winfo_rootx() 
        y = self.widget.winfo_rooty() + self.widget.winfo_height()
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
   
# Uso del ToolTip
def createToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

# El siguiente bloque solo se ejecutará si tooltips.py es el script principal
if __name__ == "__main__":
    root = tk.Tk()
    b1 = tk.Button(root, text="Botón")
    b1.pack(padx=10, pady=5)
    createToolTip(b1, "Información del botón")
    root.mainloop()