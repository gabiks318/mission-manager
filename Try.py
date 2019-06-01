from tkinter import *

def printt():
    print(square.get(1.0,END))
    
def main(root):

    root.mainloop()

root=Tk()
root.title("Mission Control")
root.geometry("580x450")
app=Frame(root)
app.grid()
square=Text(app,width=15,height=1,wrap=WORD)
square.grid(row=0,column=0)
square.insert(0.0,'meeeeeir')
b= Button(app,text="print",command=printt)
b.grid(row=1,column=0,sticky='W')

main(root=root)
