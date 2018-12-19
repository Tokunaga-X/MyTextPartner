# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtWidgets
from PyQt5 import QtPrintSupport
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt

from ext import *
from langdetect import detect

#翻译模块
from translate import Translator

#add(QSS)

class CommonHelper:
    def __init__(self,parent=None):
        pass
    def readQss(self,  style):
        with open(style,'r') as f:
            return f.read()


class Main(QtWidgets.QMainWindow):

    choice_list=['中文','English','Français','日本語 ','한국어']

    def __init__(self,parent=None):
        QtWidgets.QMainWindow.__init__(self,parent)

        #add(QSS)

        styleFile = 'style.qss'
        qssStyle = CommonHelper.readQss(self,styleFile)
        self.setStyleSheet(qssStyle)

        self.filename = ""

        self.changesSaved = True

        self.initUI()

    def initToolbar(self):
        #语言输入

        #speakAction = QtWidgets.QAction(QtGui.QIcon("icons/speak.png"),"Speak",self)
        #speakAction.setStatusTip("Write down what u say.")
        #speakAction.triggered.connect(self.speakInput)


        self.newAction = QtWidgets.QAction(QtGui.QIcon("icons/new1.png"),"New",self)
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.setStatusTip("新建一个编辑器程序。")
        self.newAction.triggered.connect(self.new)

        self.openAction = QtWidgets.QAction(QtGui.QIcon("icons/open1.png"),"Open file",self)
        self.openAction.setStatusTip("打开已存在的文本文件。")
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.open)

        self.saveAction = QtWidgets.QAction(QtGui.QIcon("icons/save1.png"),"Save",self)
        self.saveAction.setStatusTip("如果已存在文件，保存当前内容；如果是新建的，就要选定位置保存。")
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.save)

        self.undoAction = QtWidgets.QAction(QtGui.QIcon("icons/undo.png"),"Undo last action",self)
        self.undoAction.setStatusTip("撤销上一步操作。")
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.triggered.connect(self.text.undo)

        self.redoAction = QtWidgets.QAction(QtGui.QIcon("icons/redo.png"),"Redo last undone thing",self)
        self.redoAction.setStatusTip("重新执行上一步操作。")
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.triggered.connect(self.text.redo)

        dateTimeAction = QtWidgets.QAction(QtGui.QIcon("icons/time.png"),"Insert current date/time",self)
        dateTimeAction.setStatusTip("在文本中插入当前时间。")
        dateTimeAction.setShortcut("Ctrl+D")
        dateTimeAction.triggered.connect(datetime.DateTime(self).show)

        tableAction = QtWidgets.QAction(QtGui.QIcon("icons/table.png"),"Insert table",self)
        tableAction.setStatusTip("在文本中插入表格。")
        tableAction.setShortcut("Ctrl+T")
        tableAction.triggered.connect(table.Table(self).show)

        imageAction = QtWidgets.QAction(QtGui.QIcon("icons/image.png"),"Insert image",self)
        imageAction.setStatusTip("在文本中插入图片。")
        imageAction.setShortcut("Ctrl+Shift+I")
        imageAction.triggered.connect(self.insertImage)

        bulletAction = QtWidgets.QAction(QtGui.QIcon("icons/bullet.png"),"Insert bullet List",self)
        bulletAction.setStatusTip("在文本中插入点列表。")
        bulletAction.setShortcut("Ctrl+Shift+B")
        bulletAction.triggered.connect(self.bulletList)

        numberedAction = QtWidgets.QAction(QtGui.QIcon("icons/number.png"),"Insert numbered List",self)
        numberedAction.setStatusTip("在文本中插入数字列表。")
        numberedAction.setShortcut("Ctrl+Shift+L")
        numberedAction.triggered.connect(self.numberList)

        boldAction = QtWidgets.QAction(QtGui.QIcon("icons/bold.png"),"Bold",self)
        boldAction.setStatusTip("设置选中文本为粗体。")
        boldAction.triggered.connect(self.bold)

        italicAction = QtWidgets.QAction(QtGui.QIcon("icons/italic.png"),"Italic",self)
        italicAction.setStatusTip("设置选中文本为斜体。")
        italicAction.triggered.connect(self.italic)

        strikeAction = QtWidgets.QAction(QtGui.QIcon("icons/strike.png"),"Strike-out",self)
        strikeAction.setStatusTip("设置选中文本为删去状态。")
        strikeAction.triggered.connect(self.strike)


        alignLeft = QtWidgets.QAction(QtGui.QIcon("icons/align-left.png"),"Align left",self)
        alignLeft.triggered.connect(self.alignLeft)

        alignCenter = QtWidgets.QAction(QtGui.QIcon("icons/align-center.png"),"Align center",self)
        alignCenter.triggered.connect(self.alignCenter)

        alignRight = QtWidgets.QAction(QtGui.QIcon("icons/align-right.png"),"Align right",self)
        alignRight.triggered.connect(self.alignRight)

        alignJustify = QtWidgets.QAction(QtGui.QIcon("icons/align-justify.png"),"Align justify",self)
        alignJustify.triggered.connect(self.alignJustify)


        fontColor = QtWidgets.QAction(QtGui.QIcon("icons/font-color.png"),"改变字体颜色",self)
        fontColor.triggered.connect(self.fontColorChanged)


        themeAction = QtWidgets.QAction(QtGui.QIcon("icons/theme.png"),"改变主题",self)
        themeAction.setStatusTip("最小化窗口。")
        themeAction.triggered.connect(self.ThemeChange)


        minisizeAction = QtWidgets.QAction(QtGui.QIcon("icons/minimize.png"),"最小化",self)
        minisizeAction.setStatusTip("最小化窗口。")
        minisizeAction.triggered.connect(self.MinisizeB)

        closeAction = QtWidgets.QAction(QtGui.QIcon("icons/close.png"),"关闭",self)
        closeAction.setStatusTip("关闭窗口。")
        closeAction.triggered.connect(self.CloseB)

        self.toolbar = QtWidgets.QToolBar()
        self.addToolBar(QtCore.Qt.TopToolBarArea,self.toolbar)
        #self.toolbar.setFont(QtGui.QFont("华文彩云"))

        #speakAction添加
        #self.toolbar.addAction(speakAction)

        self.toolbar.addAction(self.newAction)
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.saveAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(imageAction)
        self.toolbar.addAction(tableAction)
        self.toolbar.addAction(dateTimeAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(bulletAction)
        self.toolbar.addAction(numberedAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(fontColor)
        self.toolbar.addAction(boldAction)
        self.toolbar.addAction(italicAction)
        self.toolbar.addAction(strikeAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(alignLeft)
        self.toolbar.addAction(alignCenter)
        self.toolbar.addAction(alignRight)
        self.toolbar.addAction(alignJustify)

        self.toolbar.addSeparator()
        self.toolbar.addAction(themeAction)
        self.toolbar.addAction(minisizeAction)
        self.toolbar.addAction(closeAction)

        self.addToolBarBreak()

    def initFormatbar(self):
        fontBox = QtWidgets.QFontComboBox(self)
        fontBox.currentFontChanged.connect(lambda font: self.text.setCurrentFont(font))
        fontBox.setFont(QtGui.QFont("华文彩云"))

        fontSize = QtWidgets.QSpinBox(self)

        self.translateBox=QtWidgets.QLineEdit(self)
        self.comboBox = QtWidgets.QComboBox(self)

        self.translateButton=QtWidgets.QPushButton(self)
        self.translateButton.setIcon(QtGui.QIcon('C:/Users/lenovo/Documents/GitHub/Software-Engineering-Program/Code/icons/translate.png'))
        self.translateButton.clicked.connect(self.translate)

        # Will display " pt" after each value
        fontSize.setSuffix(" pt")
        fontSize.value()
        fontSize.setSingleStep(5)
        fontSize.setWrapping(True);

        fontSize.valueChanged.connect(lambda size: self.text.setFontPointSize(size))

        fontSize.setValue(15)

        self.formatbar = QtWidgets.QToolBar()
        self.addToolBar(QtCore.Qt.BottomToolBarArea,self.formatbar)

        self.formatbar.addWidget(fontBox)
        self.formatbar.addWidget(fontSize)

        self.formatbar.addSeparator()

        self.formatbar.addWidget(self.translateBox)
        self.formatbar.addWidget(self.comboBox)
        self.comboBox.addItems(self.choice_list)
        self.formatbar.addWidget(self.translateButton)

    def initUI(self):

        self.text = QtWidgets.QTextEdit(self)

        # Set the tab stop width to around 33 pixels which is
        # more or less 8 spaces
        self.text.setTabStopWidth(33)

        self.initToolbar()
        #self.initMenubar()
        self.setCentralWidget(self.text)
        self.initFormatbar()

        # Initialize a statusbar for the window
        self.statusbar = self.statusBar()

        #self.statusbar.setStyleSheet(QDialog{background-image:"icons/drag.png"})

        # If the cursor position changes, call the function that displays
        # the line and column number
        self.text.cursorPositionChanged.connect(self.cursorPosition)

        # We need our own context menu for tables
        self.text.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text.customContextMenuRequested.connect(self.context)

        self.text.textChanged.connect(self.changed)

        self.setGeometry(500,100,850,800)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        #self.setAttribute(Qt.WA_TranslucentBackground)
        #self.setWindowTitle("MyReadingPartner")
        #self.setWindowIcon(QtGui.QIcon("icons/icon.png"))

    #语音输入
    def speakInput(self):
        #my_record()
        #use_cloud(get_token())
        #testString=
        testString='Contents'
        cursor = self.text.textCursor()
        cursor.insertText(testString)

    #翻译
    def translate(self):
        def translateGoogle(text):
            if self.comboBox.currentText()==self.choice_list[0]:
                test='zh'
            elif self.comboBox.currentText()==self.choice_list[1]:
                test='en'
            elif self.comboBox.currentText()==self.choice_list[2]:
                test='fr'
            elif self.comboBox.currentText()==self.choice_list[3]:
                test='ja'
            elif self.comboBox.currentText()==self.choice_list[4]:
                test='ko'
            else:
                test='ru'
            translator=Translator(to_lang=test,from_lang=detect(text))
            translation=translator.translate(text)
            return translation

        stringtest = translateGoogle(self.text.textCursor().selectedText())
        self.translateBox.setText(stringtest)

    #主题切换
    def ThemeChange(self):
        print("black or white")

    def CloseB(self):
        """
        关闭窗口
        """
        self.close()

    def MinisizeB(self):
        """
        最小化窗口
        """
        self.showMinimized()

    def changed(self):
        self.changesSaved = False

    def closeEvent(self,event):

        if self.changesSaved:

            event.accept()

        else:

            popup = QtWidgets.QMessageBox(self)

            popup.setIcon(QtWidgets.QMessageBox.Warning)

            popup.setText("The document has been modified")

            popup.setInformativeText("Do you want to save your changes?")

            popup.setStandardButtons(QtWidgets.QMessageBox.Save   |
                                      QtWidgets.QMessageBox.Cancel |
                                      QtWidgets.QMessageBox.Discard)

            popup.setDefaultButton(QtWidgets.QMessageBox.Save)

            answer = popup.exec_()

            if answer == QtWidgets.QMessageBox.Save:
                self.save()

            elif answer == QtWidgets.QMessageBox.Discard:
                event.accept()

            else:
                event.ignore()

    def context(self,pos):

        # Grab the cursor
        cursor = self.text.textCursor()

        # Grab the current table, if there is one
        table = cursor.currentTable()

        # Above will return 0 if there is no current table, in which case
        # we call the normal context menu. If there is a table, we create
        # our own context menu specific to table interaction
        if table:

            menu = QtGui.QMenu(self)

            appendRowAction = QtWidgets.QAction("Append row",self)
            appendRowAction.triggered.connect(lambda: table.appendRows(1))

            appendColAction = QtWidgets.QAction("Append column",self)
            appendColAction.triggered.connect(lambda: table.appendColumns(1))


            removeRowAction = QtWidgets.QAction("Remove row",self)
            removeRowAction.triggered.connect(self.removeRow)

            removeColAction = QtWidgets.QAction("Remove column",self)
            removeColAction.triggered.connect(self.removeCol)


            insertRowAction = QtWidgets.QAction("Insert row",self)
            insertRowAction.triggered.connect(self.insertRow)

            insertColAction = QtWidgets.QAction("Insert column",self)
            insertColAction.triggered.connect(self.insertCol)


            mergeAction = QtWidgets.QAction("Merge cells",self)
            mergeAction.triggered.connect(lambda: table.mergeCells(cursor))

            # Only allow merging if there is a selection
            if not cursor.hasSelection():
                mergeAction.setEnabled(False)


            splitAction = QtWidgets.QAction("Split cells",self)

            cell = table.cellAt(cursor)

            # Only allow splitting if the current cell is larger
            # than a normal cell
            if cell.rowSpan() > 1 or cell.columnSpan() > 1:

                splitAction.triggered.connect(lambda: table.splitCell(cell.row(),cell.column(),1,1))

            else:
                splitAction.setEnabled(False)


            menu.addAction(appendRowAction)
            menu.addAction(appendColAction)

            menu.addSeparator()

            menu.addAction(removeRowAction)
            menu.addAction(removeColAction)

            menu.addSeparator()

            menu.addAction(insertRowAction)
            menu.addAction(insertColAction)

            menu.addSeparator()

            menu.addAction(mergeAction)
            menu.addAction(splitAction)

            # Convert the widget coordinates into global coordinates
            pos = self.mapToGlobal(pos)

            # Add pixels for the tool and formatbars, which are not included
            # in mapToGlobal(), but only if the two are currently visible and
            # not toggled by the user

            if self.toolbar.isVisible():
                pos.setY(pos.y() + 45)

            if self.formatbar.isVisible():
                pos.setY(pos.y() + 45)

            # Move the menu to the new position
            menu.move(pos)

            menu.show()

        else:

            event = QtGui.QContextMenuEvent(QtGui.QContextMenuEvent.Mouse,QtCore.QPoint())

            self.text.contextMenuEvent(event)

    def removeRow(self):

        # Grab the cursor
        cursor = self.text.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Delete the cell's row
        table.removeRows(cell.row(),1)

    def removeCol(self):

        # Grab the cursor
        cursor = self.text.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Delete the cell's column
        table.removeColumns(cell.column(),1)

    def insertRow(self):

        # Grab the cursor
        cursor = self.text.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Insert a new row at the cell's position
        table.insertRows(cell.row(),1)

    def insertCol(self):

        # Grab the cursor
        cursor = self.text.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Insert a new row at the cell's position
        table.insertColumns(cell.column(),1)

    def toggleToolbar(self):

        state = self.toolbar.isVisible()

        # Set the visibility to its inverse
        self.toolbar.setVisible(not state)

    def toggleFormatbar(self):

        state = self.formatbar.isVisible()

        # Set the visibility to its inverse
        self.formatbar.setVisible(not state)

    def toggleStatusbar(self):

        state = self.statusbar.isVisible()

        # Set the visibility to its inverse
        self.statusbar.setVisible(not state)

    def speakinput(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
        try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
         print("Google Speech Recognition thinks you said \n" + r.recognize_google(audio))

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")

        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def new(self):

        spawn = Main()

        spawn.show()

    def open(self):

        # Get filename and show only .writer files
        #PYQT5 Returns a tuple in PyQt5, we only need the filename
        self.filename = QtWidgets.QFileDialog.getOpenFileName(self,"选取文件","C:/", "All Files (*);;Text Files (*.txt)")[0]

        if self.filename:
            with open(self.filename,"rt") as file:
                self.text.setText(file.read())

        """
        filename,_ = QtWidgets.QFileDialog.getOpenFileName(self);
        text=open(filename,'rt',encoding='UTF-8').read()
        self.text.setText(text)
        """
    def save(self):

        # Only open dialog if there is no filename yet
        #PYQT5 Returns a tuple in PyQt5, we only need the filename
        if not self.filename:
          self.filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')[0]

        if self.filename:
            """
            # Append extension if not there yet
            if not self.filename.endswith(".writer"):
              self.filename += ".writer"

            # We just store the contents of the text file along with the
            # format in html, which Qt does in a very nice way for us
            with open(self.filename,"wt") as file:
                file.write(self.text.toHtml())
            """
            file=open(self.filename,"wt")
            file.write(self.text.toHtml())

            self.changesSaved = True

    def cursorPosition(self):

        cursor = self.text.textCursor()

        # Mortals like 1-indexed things
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()

        self.statusbar.showMessage("Line: {} | Column: {}".format(line,col))

    def insertImage(self):

        # Get image file name
        #PYQT5 Returns a tuple in PyQt5
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Insert image',".","Images (*.png *.xpm *.jpg *.bmp *.gif)")[0]

        if filename:

            # Create image object
            image = QtGui.QImage(filename)

            # Error if unloadable
            if image.isNull():

                popup = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                          "Image load error",
                                          "Could not load image file!",
                                          QtWidgets.QMessageBox.Ok,
                                          self)
                popup.show()

            else:

                cursor = self.text.textCursor()

                cursor.insertImage(image,filename)

    def fontColorChanged(self):

        # Get a color from the text dialog
        color = QtWidgets.QColorDialog.getColor()

        # Set it as the new text color
        self.text.setTextColor(color)

    def bold(self):

        if self.text.fontWeight() == QtGui.QFont.Bold:

            self.text.setFontWeight(QtGui.QFont.Normal)

        else:

            self.text.setFontWeight(QtGui.QFont.Bold)

    def italic(self):

        state = self.text.fontItalic()

        self.text.setFontItalic(not state)

    def strike(self):

        # Grab the text's format
        fmt = self.text.currentCharFormat()

        # Set the fontStrikeOut property to its opposite
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())

        # And set the next char format
        self.text.setCurrentCharFormat(fmt)

    def alignLeft(self):
        self.text.setAlignment(Qt.AlignLeft)

    def alignRight(self):
        self.text.setAlignment(Qt.AlignRight)

    def alignCenter(self):
        self.text.setAlignment(Qt.AlignCenter)

    def alignJustify(self):
        self.text.setAlignment(Qt.AlignJustify)

    def bulletList(self):

        cursor = self.text.textCursor()

        # Insert bulleted list
        cursor.insertList(QtGui.QTextListFormat.ListDisc)

    def numberList(self):

        cursor = self.text.textCursor()

        # Insert list with numbers
        cursor.insertList(QtGui.QTextListFormat.ListDecimal)

    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(Qt.OpenHandCursor))  #更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):

        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos()-self.m_Position)#更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QtGui.QCursor(Qt.ArrowCursor))


def main():
    app = QtWidgets.QApplication(sys.argv)

    main = Main()
    main.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
