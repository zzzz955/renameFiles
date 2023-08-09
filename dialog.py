from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, \
    QListWidget, QListWidgetItem, QHBoxLayout, QMessageBox, QDialog, QTableWidget, QTableWidgetItem

class file_List(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle('첨부 파일 리스트')
        self.main_window = main_window
        self.setGeometry(500, 100, 400, 600)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.uploaded_file_list = QListWidget()
        layout.addWidget(self.uploaded_file_list)
        layout.addWidget(QPushButton("확인", clicked=self.accept))

class imageSizeValue(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle('변경 이미지 사이즈 설정')
        self.setGeometry(500, 100, 500, 400)
        self.main_window = main_window
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(['삭제', '가로 Size', '세로 Size', '변경 값'])
        self.table_widget.resizeColumnsToContents()

        Hlayout = QHBoxLayout()
        self.layout.addLayout(Hlayout)

        self.add_size_btn = QPushButton("추가")
        self.add_size_btn.clicked.connect(self.add_sizes)
        Hlayout.addWidget(self.add_size_btn)
        self.trunc_size_btn = QPushButton("초기화")
        self.trunc_size_btn.clicked.connect(self.trunc_sizes)
        Hlayout.addWidget(self.trunc_size_btn)

        Hlayout2 = QHBoxLayout()
        self.layout.addLayout(Hlayout2)

        self.accept_btn = QPushButton("저장")
        self.accept_btn.clicked.connect(self.accept)
        Hlayout2.addWidget(self.accept_btn)
        self.reject_btn = QPushButton("취소")
        self.reject_btn.clicked.connect(self.reject)
        Hlayout2.addWidget(self.reject_btn)

    def add_sizes(self):
        count = self.table_widget.rowCount()
        self.table_widget.insertRow(count)
        item = QPushButton("삭제")
        item.clicked.connect(lambda checked, row=count: self.del_sizes(row))
        self.table_widget.setCellWidget(count, 0, item)

    def trunc_sizes(self):
        self.table_widget.clear()
        self.table_widget.setRowCount(0)
        self.table_widget.setHorizontalHeaderLabels(['삭제', '가로 Size', '세로 Size', '변경 값'])

    def del_sizes(self, row):
        self.table_widget.removeRow(row)

    def remember_init_data(self):
        self.rowCount = self.table_widget.rowCount()
        self.table_data = []
        for row in range(self.table_widget.rowCount()):
            row_data = []
            for col in range(self.table_widget.columnCount()-1):
                item = self.table_widget.item(row, col+1)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append(None)
            self.table_data.append(row_data)

    def accept(self):
        rowCount = self.table_widget.rowCount()
        colCount = self.table_widget.columnCount()
        result = True
        for row in range(rowCount):
            for col in range(colCount-1):
                item = self.table_widget.item(row, col+1)
                if item is None:
                    result = False
        if result:
            super().accept()
        else:
            QMessageBox.critical(self,'경고', '모든 데이터가 입력 되어 있는지 확인해 주세요.')

    def reject(self):
        try:
            if len(self.table_data) > 0:
                self.table_widget.clear()
                self.table_widget.setHorizontalHeaderLabels(['삭제', '가로 Size', '세로 Size', '변경 값'])
                self.table_widget.setRowCount(len(self.table_data))
                self.table_widget.setColumnCount(len(self.table_data[0])+1)
                rowCount = self.table_widget.rowCount()
                colCount = self.table_widget.columnCount()

                for row in range(rowCount):
                    item_btn = QPushButton("삭제")
                    item_btn.clicked.connect(lambda checked, row=row: self.del_sizes(row))
                    self.table_widget.setCellWidget(row, 0, item_btn)
                    for col in range(colCount-1):
                        item = QTableWidgetItem(self.table_data[row][col])
                        self.table_widget.setItem(row, col+1, item)
                super().reject()
            else:
                self.table_widget.clear()
                self.table_widget.setRowCount(0)
                self.table_widget.setHorizontalHeaderLabels(['삭제', '가로 Size', '세로 Size', '변경 값'])
                super().reject()
        except Exception as e:
            print(e)

class changeCriteriaValue(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle('변경 기준 관리')
        self.setGeometry(500, 100, 400, 500)
        self.main_window = main_window
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.listwidget_language = QListWidget()
        self.label_language = QLabel("변경 기준 List")
        self.line_edit_language = QLineEdit()
        self.button_add_language = QPushButton("추가")
        self.button_remove_language = QPushButton("제거")
        self.button_remove_all_languages = QPushButton("전체 제거")

        self.button_add_language.setProperty('class', 'success')
        self.button_add_language.clicked.connect(self.add_language)
        self.button_remove_language.clicked.connect(self.remove_language)
        self.button_remove_all_languages.clicked.connect(self.remove_all_languages)

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.label_language)
        v_layout.addWidget(self.listwidget_language)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.line_edit_language)
        h_layout.addWidget(self.button_add_language)
        h_layout.addWidget(self.button_remove_language)
        h_layout.addWidget(self.button_remove_all_languages)

        self.layout.addLayout(v_layout)
        self.layout.addLayout(h_layout)

        # Default 변경 기준 추가
        self.default_languages = ["_en", "_de", "_es", "_fr", "_id", "_it", "_kr", "_pt", "_ru", "_th", "_tr", "_tw", "_ar", "_cn"]
        for language in self.default_languages:
            item = QListWidgetItem(language)
            self.listwidget_language.addItem(item)
        self.line_edit_language.returnPressed.connect(self.add_language)

        self.exit_dialog_btn = QPushButton("종료")
        self.exit_dialog_btn.clicked.connect(self.exit_dialog)
        self.layout.addWidget(self.exit_dialog_btn)

    def add_language(self):
        language = self.line_edit_language.text().strip()
        if language:
            # 중복 확인
            if self.check_duplicate_language(language):
                return

            # 입력된 값을 ListWidget에 추가
            item = QListWidgetItem(language)
            self.listwidget_language.insertItem(0, item)
            self.line_edit_language.clear()

    def check_duplicate_language(self, language):
        # 중복 확인 함수
        for index in range(self.listwidget_language.count()):
            item = self.listwidget_language.item(index)
            if item.text() == language:
                return True
        return False

    def remove_language(self):
        # 변경 기준 삭제
        selected_items = self.listwidget_language.selectedItems() # 선택된 아이템
        for item in selected_items:
            self.listwidget_language.takeItem(self.listwidget_language.row(item))

    def remove_all_languages(self):
        self.listwidget_language.clear()

    def exit_dialog(self):
        self.accept()