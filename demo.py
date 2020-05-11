

from PyQt5 import QtGui, QtCore
from PyQt5.QtSql import QSqlQueryModel,QSqlDatabase,QSqlQuery
from PyQt5.QtWidgets import QApplication, QWidget,QTableWidget, QVBoxLayout,QTableView
import sys
import pandas as pd
import numpy as np

Qt = QtCore.Qt




class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, filename, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)

        tmp_filename = "tmp/" + filename.split("/")[-1]
        df = pd.read_excel(filename)
        df.to_csv(tmp_filename)
        self.__headers = list(df)
        data = df.replace(np.nan, '', regex=True)
        self._data = df

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.__headers[section]
            else:
                # set row names: color 0, color 1, ...
                return "%s" % str(section + 1)

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return QtCore.QVariant(str(
                    self._data.values[index.row()][index.column()]))
        return QtCore.QVariant()





def onclicked(clickedIndex):


    r = clickedIndex.row()
    df = projectModel._data
    header = list(df)
    data = df.values.tolist()












if __name__ == "__main__":

    filename = "data/Ismailia.xls"
    app = QApplication(sys.argv)

    projectModel = PandasModel(filename)



    projectView = QTableView()
    projectView.setModel(projectModel)
    projectView.showMaximized()
    projectView.clicked.connect(onclicked)
    projectView.show()
    app.exec_()


