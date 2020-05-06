
from PyQt5.QtWidgets import QApplication,QTableView
import sys


app = QApplication(sys.argv)
tableview = QTableView()
tableview.setWindowTitle('Stations')
tableview.showMaximized()
sys.exit(app.exec_())
