"""
A class to edit the database.
Three XML files:Active missions,standby missions and archive.
XML file structure:
<missions>
    <mission1 id=x>
        <day>
        <month>
        <year>
        <description>
        <state>?
        <classification>
        <due>
        <category>
    <mission1>
    <mission2>
    ...
    <mission3>
    ...
<missions>
"""

import xml.etree.ElementTree as ET

class Mission(object):

    def __init__(self,date,description,category,due):
        """Get the mission's details"""
        self.date=date
        self.description=description
        self.category=category
        self.due=due
        self.state="A"
        self.classification="true"

    def __getFile(self,path):
        tree=ET.parse(path)
        root=tree.getroot()
        return tree,root
        
    def write(self, path):
        mission=ET.Element('mission')
        mission.set('id',self.__get_id(path=path))

        write_day=ET.SubElement(mission,'day')
        write_day.text=self.date[:2]
        write_month=ET.SubElement(mission,'month')
        write_month.text=self.date[3:5]
        write_year=ET.SubElement(mission,'year')
        write_year.text=self.date[6:]
        
        write_description=ET.SubElement(mission,'description')
        write_description.text=self.description
        
        write_state=ET.SubElement(mission,'state')
        write_state.text=self.state
        
        write_classification=ET.SubElement(mission,'classification')
        write_classification.text=self.classification

        write_due=ET.SubElement(mission,'due')
        write_due.text=self.due

        write_cat=ET.SubElement(mission,'category')
        write_cat.text=self.category
        
        tree,root=self.__getFile(path)
        root.append(mission)
        tree.write(path)

    def __get_id(self, path):
        tree,root=self.__getFile(path)
        new_id=len(root)+1
        return str(new_id)
        
    def rewrite(self,path,edit_id):
        tree,root=self.__getFile(path)
        
        mission=root[edit_id]

        mission[0].text=self.date[:2]
        mission[1].text=self.date[3:5]
        mission[2].text=self.date[6:]
        mission[3].text=self.description
        mission[4].text=self.state
        mission[5].text=self.classification
        mission[6].text=self.due
        mission[7].text=self.category
        tree.write(path)


