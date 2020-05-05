
from PyQt5.QtWidgets import QApplication, QWidget,QTableWidget, QVBoxLayout
import sys






class mainwindow(QWidget):

    def __init__(self, parent=None):
        super(mainwindow, self).__init__(parent)

        self.title = 'PyQt5 table - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.showMaximized()
        self.createTable()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        # Show widget
        self.show()

    def createTable(self):
        # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(2)












if __name__ == "__main__":
    app = QApplication(sys.argv)
    exp=mainwindow()
    exp.show()
    sys.exit(app.exec_())





