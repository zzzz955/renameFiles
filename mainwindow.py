import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QFileDialog, \
    QHBoxLayout, QMessageBox, QAction, QFrame, QLabel
from PyQt5.QtCore import QFileInfo
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
        #self.setGeometry(0,0, 400, 600)

        # 위젯 추가
        self.label1 = QLabel("이미지 업로드")
        self.label2 = QLabel("변경 기준 설정")
        self.button_browse_folder = QPushButton("폴더 업로드 (Alt+D)")
        self.button_browse_File = QPushButton("파일 업로드 (Alt+F)")
        self.upload_list_btn = QPushButton("첨부된 이미지 목록 확인")
        self.image_sizes_setting_btn = QPushButton("이미지 변경 기준 설정")
        self.changeCriteria_btn = QPushButton("파일명 변경 기준 설정")
        self.button_rename = QPushButton("파일명 변경 실행")
        self.button_close = QPushButton("앱 종료")

        # 레이아웃 추가
        layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        v_layout = QVBoxLayout()
        h_layout2 = QHBoxLayout()
        v_layout2 = QVBoxLayout()
        box_frame = QFrame(self)
        box_frame.setFrameShape(QFrame.Box)
        layout.addWidget(box_frame)
        box_frame.setLayout(v_layout)
        v_layout.addWidget(self.label1)
        v_layout.addLayout(h_layout)
        h_layout.addWidget(self.button_browse_folder)
        h_layout.addWidget(self.button_browse_File)
        v_layout.addWidget(self.upload_list_btn)

        box_frame2 = QFrame(self)
        box_frame2.setFrameShape(QFrame.Box)
        layout.addWidget(box_frame2)
        box_frame2.setLayout(v_layout2)
        v_layout2.addWidget(self.label2)
        v_layout2.addLayout(h_layout2)
        h_layout2.addWidget(self.image_sizes_setting_btn)
        h_layout2.addWidget(self.changeCriteria_btn)

        layout.addWidget(self.button_rename)
        layout.addWidget(self.button_close)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # 버튼 시그널 추가
        self.button_browse_folder.clicked.connect(self.upload_folder)
        self.button_browse_File.clicked.connect(self.upload_files)
        self.upload_list_btn.clicked.connect(self.uploaded_filelist_check)
        self.image_sizes_setting_btn.clicked.connect(self.image_sizes_setting)
        self.changeCriteria_btn.clicked.connect(self.changeCriteria)
        self.button_rename.clicked.connect(self.rename_files)
        self.button_close.clicked.connect(self.appClose)

        # 단축키 설정
        shortcut_browse_folder = QAction(self)
        shortcut_browse_folder.setShortcut("Alt+D")
        shortcut_browse_folder.triggered.connect(self.button_browse_folder.click)
        self.addAction(shortcut_browse_folder)

        shortcut_browse_file = QAction(self)
        shortcut_browse_file.setShortcut("Alt+F")
        shortcut_browse_file.triggered.connect(self.button_browse_File.click)
        self.addAction(shortcut_browse_file)

        shortcut_rename = QAction(self)
        shortcut_rename.setShortcut("Alt+Return")
        shortcut_rename.triggered.connect(self.button_rename.click)
        self.addAction(shortcut_rename)

        # 드래그 드롭 기능 추가
        self.setAcceptDrops(True)

        # 클래스 인스턴스 생성
        self.check_filelist = file_List(self)
        self.manage_size = imageSizeValue(self)
        self.manage_Criteria = changeCriteriaValue(self)

        # 변수 초기화
        self.folder_path = ''
        self.file_paths = ''

        # 생성자 함수 실행
        self.from_json()

    def uploaded_filelist_check(self):
        # 다이얼 로그 호출
        self.check_filelist.exec()

    def image_sizes_setting(self):
        # 다이얼 로그 호출
        self.manage_size.remember_init_data()
        self.manage_size.exec()

    def changeCriteria(self):
        # 다이얼 로그 호출
        self.manage_Criteria.exec()

    def dragEnterEvent(self, event):
        # 파일 드래그 이벤트 함수
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        # 파일 드랍 이벤트 함수
        try:
            urls = event.mimeData().urls()
            file_paths = []
            for url in urls:
                file_path = url.toLocalFile()
                file_paths.append(file_path)
            if QFileInfo(file_paths[0]).isDir():
                self.folder_path = file_paths[0]
                self.check_filelist.uploaded_file_list.clear()
                self.image_files = [file for file in os.listdir(file_paths[0]) if
                               file.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]
                self.check_filelist.uploaded_file_list.clear()
                self.check_filelist.uploaded_file_list.addItems(self.image_files)
                image_files = [os.path.join(file_paths[0], filename) for filename in os.listdir(file_paths[0]) if
                               filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]
                self.get_image_val = classifyImages.get_image_datas(image_files)
                self.check_filelist.label_count.setText(f'{self.check_filelist.uploaded_file_list.count()}개 항목 업로드')
            else:
                self.file_paths = file_paths
                self.check_filelist.uploaded_file_list.clear()
                self.image_files = []
                for file in self.file_paths:
                    if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                        self.image_files.append(os.path.basename(file))
                    else:
                        return
                self.check_filelist.uploaded_file_list.addItems(self.image_files)
                self.get_image_val = classifyImages.get_image_datas(self.file_paths)
                self.check_filelist.label_count.setText(f'{self.check_filelist.uploaded_file_list.count()}개 항목 업로드')
        except Exception as e:
            print(e)

    def upload_folder(self):
        # 폴더 업로드 함수
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
            self.check_filelist.label_count.setText(f'{self.check_filelist.uploaded_file_list.count()}개 항목 업로드')

    def upload_files(self):
        # 파일 업로드 함수
        file_paths, _ = QFileDialog.getOpenFileNames(self, '파일 탐색', '', '사진 파일(*.png *.jpg *.jpeg *.gif)')
        if file_paths:
            self.file_paths = file_paths
            self.check_filelist.uploaded_file_list.clear()
            self.image_files = []
            for file in self.file_paths:
                self.image_files.append(os.path.basename(file))
            self.check_filelist.uploaded_file_list.addItems(self.image_files)
            self.get_image_val = classifyImages.get_image_datas(self.file_paths)
            self.check_filelist.label_count.setText(f'{self.check_filelist.uploaded_file_list.count()}개 항목 업로드')

    def rename_files(self):
        try:
            self.renameCount = 0
            if self.check_filelist.uploaded_file_list.count() == 0:
                return
            # 변경 기준 데이터 replace 함수 전달
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
            logger.critical(f"예외 발생, 정보 : {e}")

        if self.renameCount > 0:
            # 변경된 파일 정보 노출
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

    def replace(self, key, set_replace_val):
        # 파일명 변경 함수
        directory = os.path.dirname(key) # 파일 경로 변수
        filename = os.path.basename(key) # 파일명 변수
        base_name, extension = os.path.splitext(filename) # 파일명과 확장자 분리

        new_base_name = set_replace_val # 변경될 파일명 변수
        base_name_lower = base_name.lower()  # 파일명 소문자로 변환

        for i in range(self.manage_Criteria.listwidget_language.count()):
            item = self.manage_Criteria.listwidget_language.item(i)
            item_text_lower = item.text().lower()  # 변경 기준 소문자로 변환
            if base_name_lower.endswith(item_text_lower):  # 기존 파일명의 끝에 변경 기준이 위치 하는지?
                new_base_name += item.text()  # 변경 값과 변경 기준 결합
                '''index = base_name_lower.find(item_text_lower) # 변경 기준 뒤 문자열 찾기
                if index != -1:
                    new_base_name += base_name[index + len(item_text_lower):] # 변경 기준 뒤 문자열 결합'''
                new_filename = new_base_name + extension # 확장자 결합
                new_file_path = os.path.join(directory, new_filename) # 경로 결합
                os.rename(key, new_file_path) # 파일명 변경
                logger.info(f"파일명 변경 완료 : {filename} → {new_filename}")
                self.renameCount += 1

    def open_folder(self):
        # 변경 후 이미지 경로 폴더 오픈 여부?
        if not self.folder_path:
            return
        directory = os.path.dirname(self.folder_path)
        os.startfile(directory)

    def to_json(self):
        # jsons.py에 데이터 전달
        datas = []
        criteria_val = []
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
        for val in range(self.manage_Criteria.listwidget_language.count()):
            item = self.manage_Criteria.listwidget_language.item(val)
            criteria_val.append(item.text())
        fending_data = {'datas': datas, 'criteria_val': criteria_val}
        jsons.save_data(fending_data)

    def from_json(self):
        # jsons.py로 부터 데이터 받아오기
        try:
            table_data, criteria_val = jsons.load_data()
            self.manage_size.set_before_data(table_data)
            self.manage_Criteria.listwidget_language.addItems(criteria_val)
            self.manage_Criteria.label_count.setText(f"{len(criteria_val)}개 항목")
        except Exception as e:
            QMessageBox.warning(self, '데이터 확인', f'기존 데이터가 확인되지 않습니다. {e}')
            logger.critical(f"예외 발생, 정보 : {e}")

    def appClose(self):
        self.close()

    def closeEvent(self, event):
        result = QMessageBox.question(self, '데이터 저장', '변경 내용을 저장 하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if result == QMessageBox.Yes:
            self.to_json()
            event.accept()
        else:
            event.accept()

if __name__ == '__main__':
    app = QApplication([])
    apply_stylesheet(app, theme='custom.xml')
    window = FileRenamer()
    window.show()
    app.exec_()