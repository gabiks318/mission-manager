from tkinter import *
import xml.etree.ElementTree as ET
from XML_manager import Mission
import time

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
        
        # initialize the rest of the table
        for i in range(self.start_row,self.height+self.start_row):
            row_content = []  # store the content of the row
            
            for j in range(self.start_col,self.start_col+self.width):

                square=Text(self.master,width=15,height=1,wrap=WORD)
                square.grid(row=i,column=j)
                row_content.append(square)
                square.config(state=DISABLED)

            self.TABLE_CONTENT.append(row_content)

    def insert_first_row(self,content):
        self.insert_text(0,content)

    def insert_text(self,rownum,content):
        i=0
        while i<(self.width):
            self.TABLE_CONTENT[rownum][i].config(state=NORMAL)
            self.TABLE_CONTENT[rownum][i].insert(0.0,content[i])
            self.TABLE_CONTENT[rownum][i].config(state=DISABLED)
            i+=1
                                    
    def get_height(self):
        
        return (1+len(self.TABLE_CONTENT))

    def resize_column(self,column,mod_wid):
        for i in self.TABLE_CONTENT:
            i[column].config(state=NORMAL)
            i[column].config(width=mod_wid)
            i[column].config(state=DISABLED)

    def delete(self):
        i = 1 # starts from the second row,not to delete the first row
        while i < len(self.TABLE_CONTENT):
            for j in self.TABLE_CONTENT[i]:
                j.config(state=NORMAL)
                j.delete(0.0,END)
                j.config(state=DISABLED)
            i += 1

    def get_mission_descriptions(self):
        descriptions = []
        for content in self.TABLE_CONTENT:
            desc = content[len(content)-1].get(1.0, END)
            descriptions.append(desc)
        return descriptions


class Main_Table(Table):

    def __init__(self,master,height,width,in_row,in_column=0):
        Table.__init__(self,master,height,width,in_row,in_column)
        #first row content
        self.FIRST_ROW=["Category","Date","Detailed Description","Completed"]
        self.insert_first_row(self.FIRST_ROW)
        



class Mission_window(object):

    def __init__(self,master,path):
        self.master=master
        self.frame=Frame(self.master)
        self.cat_entry=None
        self.des_entry=None
        self.path=path
        self.type=StringVar()
        self.create_widgets(self.master)
        

    def create_widgets(self,master):
        row_counter=0

        Label(master,
              text="Category:"
              ).grid(row=row_counter,column=0,sticky='W')#Main Label

        self.cat_entry=Entry(master)
        self.cat_entry.grid(row=row_counter,column=1,sticky='W')
        row_counter+=1

        Label(master,
              text="Description:"
              ).grid(row=row_counter,column=0,sticky='W')#Main Label
        self.des_entry=Entry(master)
        self.des_entry.grid(row=row_counter,column=1,columnspan=5,sticky='W')

        row_counter+=1

        self.routine_button=Radiobutton(master,
                                        text="Routine",
                                        value="routine",
                                        variable=self.type)
        self.routine_button.grid(row=row_counter,column=0,sticky='W')
                                        
        row_counter+=1

        self.immediate_button=Radiobutton(master,
                                        text="Immediate",
                                        value="immediate",
                                        variable=self.type)
        self.immediate_button.grid(row=row_counter,column=0,sticky='W')
                                        
        row_counter+=1
        
        self.update_button=Button(master,text="Add",command=self.add
                           ).grid(row=row_counter,column=1,sticky='W')

        self.cancel_button=Button(master,text="Cancel",command=self.cancel
                           ).grid(row=row_counter,column=0,sticky='W')
        

    def cancel(self):
        self.master.destroy()

    def add(self):
        cat=self.cat_entry.get().lower().title()
        des=self.des_entry.get().lower()
        date1=time.strftime("%d-%m-%y")
        mission=Mission(date=date1,description=des,category=cat,due=self.type.get())
        mission.write(self.path)
        self.master.destroy()


class Edit_window(object):

    def __init__(self, master, path):
        self.master = master
        self.frame = Frame(self.master)
        self.active_db_path = path
        self.missions_index = {}  # Holds indexing between row number and a mission
        self.RADIO_BUT = []
        self.option = StringVar()
        self.create_widgets()
        self.fill_table()
        self.create_table_indexing()

    def create_widgets(self):

        row_counter=0

        Label(self.master,
              text="Select Mission"
              ).grid(row=row_counter,column=0,sticky='W')

        row_counter += 1
        
        self.tree = ET.parse(self.active_db_path)
        self.root = self.tree.getroot()
        tree_len = len(self.root)

        self.create_radio(rows=tree_len,count=row_counter)
        
        self.table = None
        self.table = Table(self.master, height=tree_len, width=3, in_row=row_counter,in_column=1)
        self.table.resize_column(column=2, mod_wid=25)

        row_counter += tree_len

        self.edit_button = Button(self.master,text="Edit",command=self.edit
                                  ).grid(row=row_counter,column=1,sticky='W')

        self.cancel_button = Button(self.master,text="Cancel",command=self.cancel
                                    ).grid(row=row_counter,column=0,sticky='W')

        self.delete_button = Button(self.master, text="Delete", command=self.delete_mission
                                    ).grid(row=row_counter,column=2,sticky = 'W')

    def create_table_indexing(self):
        descriptions_list = self.table.get_mission_descriptions()
        height = self.table.get_height() -1
        for i in range(height):
            self.missions_index[i] = descriptions_list[i]

    def create_radio(self,rows,count):
        i=0
        while i < rows:
            button = Radiobutton(self.master,
                               text = "",
                               value = str(i),
                               variable = self.option)
            button.grid(row=i+count, column=0, sticky='W')
            self.RADIO_BUT.append(button)
            i += 1
                               
    def fill_table(self):
        i=0 #number of iterations
        j=0 #table row index number
            #immediate missions
        while (i < len(self.root)):
         
            #check what type of mission
            if self.root[i].find('due').text=='routine':
                i+=1
                continue
            else:
                #get mission details
                
                cat=self.root[i][7].text
                desc=self.root[i][3].text
                due=self.root[i][6].text
                
                content=[cat,due,desc]#remember to cancel the last element
                self.table.insert_text(rownum=j,content=content)
                i+=1
                j+=1
                
        i=0
            #routine missions
        while (j<len(self.root)): 
         
            #check what type of mission
            if self.root[i].find('due').text == 'immediate':
                i += 1
                continue
            else:
                #get mission details
                cat=self.root[i][7].text
                desc=self.root[i][3].text
                due=self.root[i][6].text
                
                content = [cat, due, desc] # remember to cancel the last element
                self.table.insert_text(rownum=j, content=content)
                i += 1
                j += 1

    def cancel(self):
        self.master.destroy()

    def edit(self):
        self.toplevel_mission_window = Toplevel(self.master)
        self.mission_window = Sub_edit_window(self.toplevel_mission_window,self.active_db_path,int(self.option.get()))

    def delete_mission(self):
        tree = ET.parse(self.active_db_path)
        root = tree.getroot()
        description = self.missions_index[int(self.option.get())]
        description = description[:len(description)-1]  # Truncate the \n
        for mission in root:
            mission_description = mission[3].text
            if description == mission_description:
                root.remove(mission)
        tree.write(self.active_db_path)
        self.master.destroy()

class Sub_edit_window(object):

    def __init__(self,master,path,idnum):
        self.master=master
        self.frame=Frame(self.master)
        self.id=idnum
        self.cat_entry=None
        self.des_entry=None
        self.path=path
        self.type=StringVar()
        self.create_widgets(self.master)
        

    def create_widgets(self,master):
        row_counter=0

        Label(master,
              text="Category:"
              ).grid(row=row_counter,column=0,sticky='W')#Main Label

        self.cat_entry=Entry(master)
        self.cat_entry.grid(row=row_counter,column=1,sticky='W')
        row_counter+=1

        Label(master,
              text="Description:"
              ).grid(row=row_counter,column=0,sticky='W')#Main Label
        self.des_entry=Entry(master)
        self.des_entry.grid(row=row_counter,column=1,columnspan=5,sticky='W')

        row_counter+=1

        self.routine_button=Radiobutton(master,
                                        text="Routine",
                                        value="routine",
                                        variable=self.type)
        self.routine_button.grid(row=row_counter,column=0,sticky='W')
                                        
        row_counter+=1

        self.immediate_button=Radiobutton(master,
                                        text="Immediate",
                                        value="immediate",
                                        variable=self.type)
        self.immediate_button.grid(row=row_counter,column=0,sticky='W')
                                        
        row_counter+=1
        
        self.update_button=Button(master,text="Edit",command=self.edit
                           ).grid(row=row_counter,column=1,sticky='W')

        self.cancel_button=Button(master,text="Cancel",command=self.cancel
                           ).grid(row=row_counter,column=0,sticky='W')
        

    def cancel(self):
        self.master.destroy()

    def edit(self):
        cat=self.cat_entry.get().lower().title()
        des=self.des_entry.get().lower()
        date1=time.strftime("%d-%m-%y")
        mission=Mission(date=date1,description=des,category=cat,due=self.type.get())
        mission.rewrite(self.path,self.id)
        self.master.destroy()       

