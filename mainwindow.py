import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QFileDialog, \
    QHBoxLayout, QMessageBox, QAction
from qt_material import apply_stylesheet
from logs import setup_logger
from dialog import file_List, imageSizeValue, changeCriteriaValue
import classifyImages
import jsons

# 기본 로거 초기화
logger = setup_logger()

class FileRenamer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("파일명 일괄 변경")
        self.setGeometry(0,0, 400, 600)
        self.setLayout(self.layout())

        self.file_paths = []
        self.replacement_string = ""

        self.upload_list_btn = QPushButton("파일 목록 확인")
        self.image_sizes_setting_btn = QPushButton("변경 이미지 크기 설정")
        self.changeCriteria_btn = QPushButton("변경 기준 관리")
        self.button_browse = QPushButton("파일 업로드 (Alt+Q)")
        self.button_rename = QPushButton("실행")
        self.button_close = QPushButton("종료")

        # 버튼 시그널 추가
        self.button_browse.clicked.connect(self.upload_folder)
        self.upload_list_btn.clicked.connect(self.uploaded_filelist_check)
        self.image_sizes_setting_btn.clicked.connect(self.image_sizes_setting)
        self.changeCriteria_btn.clicked.connect(self.changeCriteria)
        self.button_rename.clicked.connect(self.rename_files)
        self.button_close.clicked.connect(self.appClose)

        # 레이아웃 추가
        layout = QVBoxLayout()
        layout.addWidget(self.upload_list_btn)
        layout.addWidget(self.image_sizes_setting_btn)
        layout.addWidget(self.changeCriteria_btn)
        layout.addWidget(self.button_browse)

        h_layout2 = QHBoxLayout()

        layout.addLayout(h_layout2)
        layout.addWidget(self.button_rename)
        layout.addWidget(self.button_close)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # 단축키 설정
        shortcut_browse = QAction(self)
        shortcut_browse.setShortcut("Alt+Q")
        shortcut_browse.triggered.connect(self.button_browse.click)
        self.addAction(shortcut_browse)

        shortcut_rename = QAction(self)
        shortcut_rename.setShortcut("Alt+Return")
        shortcut_rename.triggered.connect(self.button_rename.click)
        self.addAction(shortcut_rename)

        # 드래그 드롭 기능 추가
        self.setAcceptDrops(True)

        self.check_filelist = file_List(self)
        self.manage_size = imageSizeValue(self)
        self.manage_Criteria = changeCriteriaValue(self)

    def uploaded_filelist_check(self):
        self.check_filelist.exec()

    def image_sizes_setting(self):
        self.manage_size.remember_init_data()
        self.manage_size.exec()

    def changeCriteria(self):
        self.manage_Criteria.exec()

    def dragEnterEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls() and mime_data.urls()[0].isLocalFile():
            event.acceptProposedAction()

    def dropEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            folder_path = mime_data.urls()[0].toLocalFile()
            if folder_path:
                self.folder_path = folder_path
                self.check_filelist.uploaded_file_list.clear()
                self.image_files = [file for file in os.listdir(folder_path) if
                               file.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]
                self.check_filelist.uploaded_file_list.clear()
                self.check_filelist.uploaded_file_list.addItems(self.image_files)

                image_files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if
                               filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]

                self.get_image_val = classifyImages.get_image_datas(image_files)
                print(self.get_image_val)

    def upload_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Upload Folder')
        if folder_path:
            self.folder_path = folder_path
            self.check_filelist.uploaded_file_list.clear()
            self.image_files = [file for file in os.listdir(folder_path) if
                           file.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]
            self.check_filelist.uploaded_file_list.addItems(self.image_files)

            image_files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if
                           filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]

            self.get_image_val = classifyImages.get_image_datas(image_files)
            print(self.get_image_val)

    def rename_files(self):
        try:
            self.renameCount = 0
            if not self.folder_path:
                return
            set_width = []
            set_height = []
            set_replace_val = []
            set_size = self.manage_size.table_widget.rowCount()
            for row in range(set_size):
                set_width.append(self.manage_size.table_widget.item(row, 1).text())
                set_height.append(self.manage_size.table_widget.item(row, 2).text())
                set_replace_val.append(self.manage_size.table_widget.item(row, 3).text())

            for key, values in self.get_image_val.items():
                value1, value2 = values
                for i in range(set_size):
                    if str(value1) == set_width[i] and str(value2) == set_height[i]:
                        self.replace(key, set_replace_val[i])

        except Exception as e:
            QMessageBox.critical(self, "파일명 변경 중단", str(e))

        if self.renameCount > 0:
            # 변경 개수 노출
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("파일명 변경 완료")
            msg_box.setText(f"{self.renameCount}개 파일명이 변경되었습니다.")
            logger.info(f"작업 완료, {self.renameCount}개 파일 이름 변경 완료")
            open_folder_button = msg_box.addButton("폴더 열기", QMessageBox.ActionRole)
            ok_button = msg_box.addButton(QMessageBox.Ok)
            msg_box.setDefaultButton(ok_button)
            msg_box.exec_()
            if msg_box.clickedButton() == open_folder_button:
                self.open_folder()

        if self.renameCount == 0:
            # 변경된 파일 없음
            QMessageBox.warning(None, "변경된 파일 없음", "이름이 변경된 파일이 없습니다. 파일명 및 포함 단어를 다시 한 번 확인해 주세요.")
            logger.info(f"작업 완료, 변경된 파일명 없음")

    def replace(self, key, set_replace_val):
        directory = os.path.dirname(key) # 파일 경로 불러 오기
        filename = os.path.basename(key) # 파일명 불러 오기
        base_name, extension = os.path.splitext(filename) # 파일명과 확장자 분리

        new_base_name = set_replace_val
        base_name_lower = base_name.lower()  # 파일명 소문자로 변환

        for i in range(self.manage_Criteria.listwidget_language.count()):
            item = self.manage_Criteria.listwidget_language.item(i)
            item_text_lower = item.text().lower()  # 변경 기준 소문자로 변환
            if item_text_lower in base_name_lower:  # 대소문자 구분 없이 비교
                new_base_name += item.text()  # 변경 값과 변경 기준 결합
                index = base_name_lower.find(item_text_lower) # 변경 기준 뒤 문자열 찾기
                if index != -1:
                    new_base_name += base_name[index + len(item_text_lower):] # 변경 기준 뒤 문자열 결합

                new_filename = new_base_name + extension # 확장자 결합
                new_file_path = os.path.join(directory, new_filename) # 경로 결합
                os.rename(key, new_file_path) # 파일명 변경
                logger.info(f"파일명 변경 완료 : {filename} → {new_filename}")
                self.renameCount += 1

    def open_folder(self):
        if not self.folder_path:
            return
        directory = os.path.dirname(self.folder_path)

        os.startfile(directory)  # Windows에서 폴더 열기
        logger.info("저장된 폴더 열기 완료")

    def to_json(self):
        # reward_table의 보상 정보를 JSON 형식으로 반환합니다.
        datas = []
        for row in range(self.manage_size.table_widget.rowCount()):
            width_size = self.manage_size.table_widget.item(row, 1).text()
            height_size = self.manage_size.table_widget.item(row, 2).text()
            replace_val = self.manage_size.table_widget.item(row, 3).text()
            save_data = {
                'width_size': width_size,
                'height_size': height_size,
                'replace_val': replace_val,
            }
            datas.append(save_data)
        fending_data = {'datas': datas}
        jsons.save_data(fending_data)

    def appClose(self):
        self.to_json()
        self.close()
        logger.info("앱 종료")

if __name__ == '__main__':
    app = QApplication([])
    apply_stylesheet(app, theme='custom.xml')
    window = FileRenamer()
    window.show()
    app.exec_()