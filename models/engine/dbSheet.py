from openpyxl.utils import coordinate_to_tuple, get_column_letter, load_workbook


class Workbook:
    __workbook = None
    
    
    @classmethod
    def init(cls, filePath=None):
        cls.__workbook = load_workbook(filePath)

     @classmethod   
    def open_session(cls, filePath=None):
        if not cls.__workbook:
            cls.init(filePath)


     @classmethod       
    def getDbsheet(cls, sheetName="Db"):
        return cls.__workbook.get_sheet_by_name(sheetName)
    @classmethod
    def saveWorkbook(cls, fileName):
        cls.__workbook.save(f"{fileName}.xlsx")
        
    @classmethod
    def dbSubject(cls, sheetName="Db"):
        sub = []
        cell = "j2"
        db = cls.getDbsheet(sheetName)
        while db[cell].value:
            sub.append(db[cell].value)
            row, col = coordinate_to_tuple(cell)
            cell = f"{get_column_letter(col + 6)}{row}"
        return sub