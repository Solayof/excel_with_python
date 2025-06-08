from openpyxl import load_workbook
from openpyxl.utils import coordinate_to_tuple, get_column_letter


class Workbook:
    __workbook = None
    filePath = ''
    
 
    def __init__(self, *args, **kwargs):
        self.filePath = kwargs.pop("filePath", None)
    
    def open_session(self):
        if not self.__workbook:
            self.__workbook = load_workbook(self.filePath)

       
    def getDbsheet(self, sheetName="Db"):
        return self.__workbook[sheetName]

    def saveWorkbook(self, fileName):
        if self.__workbook is None:
            return False
        self.__workbook.save(f"{fileName}.xlsx")
        return True

    def dbSubjects(self, sheetName="Db"):
        sub = []
        cell = "j2"
        db = self.getDbsheet(sheetName)
        while db[cell].value:
            sub.append(db[cell].value)
            row, col = coordinate_to_tuple(cell)
            cell = f"{get_column_letter(col + 6)}{row}"
        return sub
    
    def writeCell(self, cell, value, sheetName="Db"):
        sheet = self.getDbsheet(sheetName=sheetName)
        sheet[cell] = value

    def readCell(self, cell, sheetName="Db"):
        sheet = self.getDbsheet(sheetName=sheetName)
        return sheet[cell].value
    
    def getSubjectCell(self, subject, sheetName="Db"):
        cell = "j2"
        db = self.getDbsheet(sheetName)
        while db[cell].value and db[cell].value != subject:
            row, col = coordinate_to_tuple(cell)
            cell = f"{get_column_letter(col + 6)}{row}"

        if db[cell].value == subject:
            return cell


    def close(self):
        self.__workbook.close()


    def reload(self):
        self.__workbook = load_workbook(self.filePath)