#Mission Control program
from tkinter import *
import windows
import xml.etree.ElementTree as ET
from XML_manager import Mission

class Main_application(object):
    #main application window
                
    def __init__(self,master):
        """initialize the frame."""
        self.master=master
        self.active_db_path="Database\Active Missions.xml"
        self.frame=Frame(self.master)
        self.create_menu(self.master)
        self.create_widgets(self.master)
        self.print_missions()
        
 
    def create_menu(self,master):
        self.menu=Menu(master)
        master.config(menu=self.menu)

        self.file_menu=Menu(self.menu)
        self.menu.add_cascade(label="Menu",menu=self.file_menu)
        self.file_menu.add_command(label="History"#, command=callback #history window
                             )
        self.file_menu.add_command(label="Edit Mission",command=self.create_edit_window #edit mission window
                             )
        
    def create_widgets(self,master):
        row_counter=0 #keep track of the row number

        Label(master,
              text="Mission Control 10,000"
              ).grid(row=row_counter,column=2,sticky='W')#Main Label
        row_counter+=2
        
        Label(master,
              text="Immediate:"
              ).grid(row=row_counter,column=0,sticky='W')#Immediate missions label
        row_counter+=1

        self.immediate_table=None
        self.immediate_table=windows.Main_Table(master,height=7,width=4,in_row=row_counter,in_column=0)
        self.immediate_table.resize_column(column=2,mod_wid=25)
        row_counter+=self.immediate_table.get_height()
        row_counter+=1
        
        Label(master,
              text="Routine:"
              ).grid(row=row_counter,column=0,sticky='W')#Immediate missions label
        row_counter+=1

        self.routine_table=None
        self.routine_table=windows.Main_Table(master,height=11,width=4,in_row=row_counter,in_column=0)
        self.routine_table.resize_column(column=2,mod_wid=25)
        row_counter+=self.routine_table.get_height()
        row_counter+=1

        #buttons
    

        self.append_button=Button(master,text="Add Mission",command=self.add_mission
                                  )
        self.append_button.grid(row=row_counter,column=0,sticky='W')

        self.update_button=Button(master,text="Update Missions",command=self.update_missions
                                  )
        self.update_button.grid(row=row_counter,column=1,sticky='W')



    def add_mission(self):
        self.toplevel_mission_window=Toplevel(self.master)
        #self.add_mission_window.protocol("WM_DELETE_WINDOW",self.print_missions)
        self.mission_window=windows.Mission_window(self.toplevel_mission_window,self.active_db_path)
        #self.app.frame.bind("<Destroy>",self.print_missions())
        
        
    def print_missions(self):
        self.immediate_table.delete()
        self.routine_table.delete()
        
        #parse the active missions XML file
        tree=ET.parse(self.active_db_path)
        root=tree.getroot()

        #immediate table:
        i=0 #number of iterations
        j=1 #table row index number
        
        while (i<len(root)): 
         
            #check what type of mission
            if root[i].find('due').text=='routine':
                i+=1
                continue
            else:
                #get mission details
                cat=root[i][7].text
        
                day=root[i][0].text
                month=root[i][1].text
                year=root[i][2].text
                date=day+"-"+month+"-"+year

                desc=root[i][3].text
                content=[cat,date,desc,""]#remember to cancel the last element
                self.immediate_table.insert_text(rownum=j,content=content)
                i+=1
                j+=1
        
        #routine table:
        a=0 #number of iterations
        b=1 #table row index number
        
        while (a<len(root)): 
         
            #check what type of mission
            if root[a].find('due').text=='immediate':
                a+=1
                continue
            else:
                #get mission details
                cat=root[a][7].text
        
                day=root[a][0].text
                month=root[a][1].text
                year=root[a][2].text
                date=day+"-"+month+"-"+year

                desc=root[a][3].text
                content=[cat,date,desc,""]
                self.routine_table.insert_text(rownum=b,content=content)
                a+=1
                b+=1

    def update_missions(self):
        self.print_missions()

    def create_edit_window(self):
        self.toplevel_edit_mission_window=Toplevel(self.master)
        self.edit_mission_window=windows.Edit_window(self.toplevel_edit_mission_window)
        



        
def main():
    root=Tk()
    root.title("Mission Control")
    root.geometry("580x450")
    app=Main_application(root)
    root.mainloop()
    
main()
