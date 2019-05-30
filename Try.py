from tkinter import *

class Table(object):
    
    def __init__(self,master,height,width,in_row,in_column=0):
        self.TABLE_CONTENT=[] #holds the texts squares of the table
        self.start_row=in_row
        self.master=master
        self.height=height
        self.start_col=in_column
        self.width=width
        self.initialize_table()

       
    def initialize_table(self):
        
        #initialize the rest of the table           
        for i in range(self.start_row,self.height+self.start_row):
            row_content=[] #store the content of the row
            
            for j in range(self.start_col,self.start_col+self.width):

                square=Text(self.master,width=15,height=1,wrap=WORD)
                square.grid(row=i,column=j)
                row_content.append(square)
                square.config(state=DISABLED)
                   
                
            self.TABLE_CONTENT.append(row_content)

        
    def insert_first_row(self,content):
        self.insert_text(0,content)

            
    def insert_text(self,rownum,content):
        for i in range(self.width):
            self.TABLE_CONTENT[rownum][i].config(state=NORMAL)
            self.TABLE_CONTENT[rownum][i].insert(0.0,content[i])
            self.TABLE_CONTENT[rownum][i].config(state=DISABLED)
                                    
    def get_height(self):
        
        return (1+len(self.TABLE_CONTENT))

    def resize_column(self,column,mod_wid):
        for i in self.TABLE_CONTENT:
            i[column].config(width=mod_wid)

    def delete(self):
        i=1 # starts from the second row,not to delete the first row
        while i<len(self.TABLE_CONTENT):
            for j in i:
                j.config(state=NORMAL)
                j.delete(0.0,END)
                j.config(state=DISABLED)
            

    
    

def main():
    root=Tk()
    root.title("Mission Control")
    root.geometry("580x450")
    app=Frame(root)
    app.grid()
    table=None
    table=Table(app,height=8,width=4,in_row=1)
    table.resize_column(3,50)
    #square=Text(app,width=15,height=1,wrap=WORD)
    #square.grid(row=0,column=0)
    root.mainloop()
    
main()
