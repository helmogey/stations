
import matplotlib
matplotlib.use('Qt5Agg')


from PyQt5 import QtGui, QtCore
from PyQt5.QtSql import QSqlQueryModel,QSqlDatabase,QSqlQuery
from PyQt5.QtWidgets import QApplication, QWidget,QTableWidget, QComboBox,QTableView,QGridLayout,QListWidget,QListWidgetItem, \
                            QPushButton, QLabel, QLineEdit
import sys
import pandas as pd
import numpy as np
import os
from PIL import Image, ImageDraw , ImageFont
import matplotlib.pyplot as plt
from functools import partial

Qt = QtCore.Qt




class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, filename, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)

        ext = filename.split("/")[-1].split(".")[-1]
        if ext == "xls":
            tmp_filename = "tmp/" + filename.split("/")[-1]
            df = pd.read_excel(filename)
            df.to_csv(tmp_filename, index=False)
        else:
            df = pd.read_csv(filename)
        self.__headers = list(df)
        df = df.replace(np.nan, '', regex=True)
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







class mainwindow(QWidget):

    def __init__(self,data_path,parent=None):
        super(mainwindow, self).__init__(parent)

        folders = os.listdir(data_path)




        self.mainLayout = QGridLayout(self)
        self.btn_layout = QGridLayout()
        self.buttons = []
        for num, folder in enumerate(folders):
            i = num%4
            j = num//4
            folder_button = QPushButton(folder)
            self.buttons.append(folder_button)
            self.btn_layout.addWidget(folder_button, j, i)
            folder_button.setFixedSize(200, 30)
            folder_button.clicked.connect(partial(self.dispatcher,folder))

        self.main_minue = QPushButton("back")
        self.btn_layout.addWidget(self.main_minue, 0, 0)
        self.main_minue.setFixedSize(200, 30)
        self.main_minue.hide()
        self.main_minue.clicked.connect(partial(self.main_layout,folder))



        self.projectView = QTableView()
        self.mainLayout.addWidget(self.projectView,1,0)
        self.projectView.showMaximized()
        self.projectView.hide()

        self.listWidget = QListWidget(self)
        self.mainLayout.addWidget(self.listWidget, 1, 0)
        self.listWidget.hide()

        self.status_push = QPushButton("Status")
        self.btn_layout.addWidget(self.status_push,0,2)
        self.status_push.setFixedSize(200, 30)
        self.status_push.hide()

        self.search_push = QPushButton("Search")
        self.btn_layout.addWidget(self.search_push, 0, 1)
        self.search_push.setFixedSize(200, 30)
        self.search_push.hide()
        self.search_push.clicked.connect(partial(self.search_fn,folder))

        self.search_counter = 0
        txt = "please entre search text"
        self.search_lable = QLabel(txt)
        self.btn_layout.setContentsMargins(0,0,0,0)
        self.btn_layout.addWidget(self.search_lable, 1, 0)
        self.search_lable.setFixedSize(200, 30)
        self.search_lable.hide()

        self.comboBox = QComboBox()
        self.comboBox.setObjectName(("comboBox"))
        self.btn_layout.addWidget(self.comboBox, 1, 2)

        self.comboBox.hide()


        self.search_line_edit = QLineEdit(self)
        self.btn_layout.addWidget(self.search_line_edit, 1, 1)
        self.search_line_edit.hide()

        self.search_line_edit.setFixedSize(200,30)

        self.status_push.clicked.connect(self.show_status)

        self.back_push = QPushButton("Back")
        self.back_push.clicked.connect(partial(self.close_all,folder))
        self.back_push.setFixedSize(200, 30)

        self.show_report = QPushButton("Show Report")
        self.show_report.clicked.connect(self.get_report)
        self.show_report.setFixedSize(200, 30)

        self.btn_layout.addWidget(self.back_push, 0, 0)
        self.btn_layout.addWidget(self.show_report, 0, 1)

        self.mainLayout.addLayout(self.btn_layout,0,0)

        self.back_push.hide()
        self.show_report.hide()

        self.setGeometry(0,0,1000,1000)


        self.imageLabel = QLabel(self)
        self.imageLabel.hide()
        self.setWindowTitle("Stations")

        self.mainLayout.addWidget(self.imageLabel, 1, 0)





    def search_fn(self,folder):
        filename = main_path + "/" + folder + "/" + folder + ".xls"
        df = pd.read_excel(filename)
        header = list(df)
        for h in header:
            self.comboBox.addItem(h)
        if self.search_counter == 0:
            self.search_line_edit.show()
            self.comboBox.show()
            self.search_counter += 1
        else:
            txt = self.search_line_edit.text()
            self.search_lable.hide()
            if txt == "":
                self.search_lable.show()

            else:
                self.search_counter = 2
                df = df.replace(np.nan, '', regex=True)
                df = df.applymap(str)
                h = str(self.comboBox.currentText())
                df1 = df[df[h].str.contains(txt)]
                tmp_filename = "tmp/tmp.csv"
                df1.to_csv(tmp_filename, index=False)
                self.show_table(tmp_filename)






    def main_layout(self,folder):
        if self.search_counter == 1:
            self.search_counter = 0
            self.search_line_edit.hide()
            self.search_line_edit.setText("")
            self.search_lable.hide()
            self.comboBox.hide()
        elif self.search_counter == 2:
            self.dispatcher(folder)
            self.search_counter = 1
            self.search_line_edit.setText("")
        else:

            self.setWindowTitle("Stations")
            self.projectView.hide()
            self.status_push.hide()
            self.search_push.hide()

            for folder in self.buttons:
                folder.show()
            self.main_minue.hide()


    def dispatcher(self,folder):
        filename = main_path + "/" + folder + "/" + folder + ".xls"
        # self.filename = filename
        self.setWindowTitle(folder + "  Stations")
        self.show_table(filename)





    def show_status(self):

        labels = 'Done','half year target'
        sizes = [35, 65]
        explode = (0.1, 0.0)

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')

        plt.show()



    def get_report(self):
        image_name = str(self.record[-1]) + ".jpg"

        if image_name in os.listdir("reports"):
            image_path = "reports" + "/" + image_name
            image = QtGui.QImage(image_path)

            self.qpixmap = QtGui.QPixmap.fromImage(image)
            self.imageLabel.setPixmap(self.qpixmap)




        else:
            img = Image.new('RGB', (700, 600), (0, 0, 0))

            draw = ImageDraw.Draw(img)
            draw.text((60, 250), "No Photo To Display for station number " + str(self.record[-1]), fill='rgb(255, 255, 255)',
                      font=ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 25))


            img = img.convert("RGBA")
            data = img.tobytes("raw", "RGBA")

            qim = QtGui.QImage(data, img.size[0], img.size[1], QtGui.QImage.Format_ARGB32)
            pix = QtGui.QPixmap.fromImage(qim)

            self.imageLabel.setPixmap(pix)

        self.listWidget.clear()
        self.listWidget.close()
        self.show_report.hide()
        self.imageLabel.show()
        self.main_minue.hide()




    def show_table(self,filename):
        self.projectModel = PandasModel(filename)

        self.projectView.setModel(self.projectModel)

        self.projectView.doubleClicked.connect(self.show_details)
        self.projectView.show()
        self.status_push.show()
        self.search_push.show()
        self.main_minue.show()
        for folder in self.buttons:
            folder.hide()







    def show_details(self,clickedIndex):

        self.projectView.hide()
        self.status_push.hide()
        self.search_push.hide()
        self.search_line_edit.hide()
        self.search_lable.hide()
        self.comboBox.hide()
        self.main_minue.hide()
        df = self.projectModel._data
        header = list(df)
        self.record = df.values.tolist()[clickedIndex.row()]

        self.listWidget.clear()
        self.listWidget.show()
        self.back_push.show()
        self.show_report.show()


        txt = ""
        for h , d in zip(header,self.record):
            txt += str(h) + ": " + str(d) + "\n\n"


        it = QListWidgetItem(txt)

        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(200)
        font.setPointSize(12)
        it.setFont(font)
        it.setBackground(QtGui.QBrush(QtGui.QColor("lightblue")))
        it.setTextAlignment(Qt.AlignRight)

        self.listWidget.addItem(it)



    def close_all(self,folder):
        self.search_line_edit.clear()
        self.search_counter = 0
        self.listWidget.clear()
        self.listWidget.close()
        self.back_push.hide()
        self.show_report.hide()
        self.imageLabel.hide()
        filename = main_path + "/" + folder + "/" + folder + ".xls"
        self.show_table(filename)





if __name__ == "__main__":

    # filename = "data/Ismailia/Ismailia.xls"
    main_path = "data"
    app = QApplication(sys.argv)
    exp = mainwindow(main_path)
    exp.show()
    sys.exit(app.exec_())


