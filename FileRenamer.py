import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, \
    QListWidget, QListWidgetItem, QHBoxLayout, QMessageBox, QAction
from qt_material import apply_stylesheet
import datetime
import logging

def setup_logger():
    # 로그 파일 설정
    current_datetime = datetime.datetime.now()
    log_directory = '파일명 변경 로그'
    log_filename = f'파일명 변경 로그_{current_datetime.strftime("%Y%m%d_%H%M%S")}.txt'
    log_filepath = os.path.join(log_directory, log_filename)

    # logs 폴더가 없을 경우 생성
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # 기본 로거 초기화
    logging.basicConfig(level=logging.DEBUG)

    # 파일 핸들러 생성
    file_handler = logging.FileHandler(log_filepath)
    file_handler.setLevel(logging.DEBUG)

    # 포매터 생성
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 핸들러에 포매터 설정
    file_handler.setFormatter(formatter)

    # 로거에 핸들러 추가
    logger = logging.getLogger('')
    logger.addHandler(file_handler)
    return logger

# 기본 로거 초기화
logger = setup_logger()


class FileRenamer(QMainWindow):
    def __init__(self):
        super().__init__()

        # UI 설정
        # 기본 창
        self.setWindowTitle("파일명 일괄 변경")
        self.setGeometry(self.x(), self.y(), 500, 800)

        # 변수 초기화
        self.file_paths = []
        self.replacement_string = ""

        # UI 요소 추가
        self.label_files = QLabel("파일 : ")
        self.label_file_paths = QLabel("파일 선택 필요")
        self.label_replacement = QLabel("변경 값 :")
        self.line_edit_replacement = QLineEdit()
        self.button_browse = QPushButton("파일 업로드 (Alt+O)")
        self.button_rename = QPushButton("실행 (Alt+Enter)")
        self.button_close = QPushButton("종료")

        # 다국어 코드 관련 위젯 추가
        self.label_language = QLabel("변경 기준 List")
        self.listwidget_language = QListWidget()
        self.line_edit_language = QLineEdit()
        self.button_add_language = QPushButton("추가")
        self.button_remove_language = QPushButton("제거")
        self.button_remove_all_languages = QPushButton("전체 제거")
        self.button_add_language.setProperty('class', 'success')

        # 버튼 시그널 추가
        self.button_browse.clicked.connect(self.browse_files)
        self.button_rename.clicked.connect(self.rename_files)
        self.button_add_language.clicked.connect(self.add_language)
        self.button_remove_language.clicked.connect(self.remove_language)
        self.button_remove_all_languages.clicked.connect(self.remove_all_languages)
        self.button_close.clicked.connect(self.appClose)

        # 레이아웃 추가
        layout = QVBoxLayout()
        layout.addWidget(self.label_files)
        layout.addWidget(self.label_file_paths)
        layout.addWidget(self.button_browse)

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.label_language)
        v_layout.addWidget(self.listwidget_language)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.line_edit_language)
        h_layout.addWidget(self.button_add_language)
        h_layout.addWidget(self.button_remove_language)
        h_layout.addWidget(self.button_remove_all_languages)

        h_layout2 = QHBoxLayout()
        h_layout2.addWidget(self.label_replacement)
        h_layout2.addWidget(self.line_edit_replacement)

        layout.addLayout(v_layout)
        layout.addLayout(h_layout)
        layout.addLayout(h_layout2)
        layout.addWidget(self.button_rename)
        layout.addWidget(self.button_close)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Default 변경 기준 추가
        self.default_languages = ["_en", "_de", "_es", "_fr", "_id", "_it", "_kr", "_pt", "_ru", "_th", "_tr", "_tw", "_ar", "_cn"]
        for language in self.default_languages:
            item = QListWidgetItem(language)
            self.listwidget_language.addItem(item)

        # Enter 키 시그널 추가
        self.line_edit_language.returnPressed.connect(self.add_language)
        self.line_edit_replacement.returnPressed.connect(self.rename_files)

        # 단축키 설정
        shortcut_browse = QAction(self)
        shortcut_browse.setShortcut("Alt+O")
        shortcut_browse.triggered.connect(self.button_browse.click)
        self.addAction(shortcut_browse)

        shortcut_rename = QAction(self)
        shortcut_rename.setShortcut("Alt+Return")
        shortcut_rename.triggered.connect(self.button_rename.click)
        self.addAction(shortcut_rename)

        # 스타일 입히기
        self.line_edit_replacement.setStyleSheet("QLineEdit { color: white; font-weight: bold; }")
        self.line_edit_language.setStyleSheet("QLineEdit { color: white; font-weight: bold; }")
        self.label_files.setStyleSheet("QLabel { font-weight: bold; }")
        self.label_file_paths.setStyleSheet("QLabel { font-weight: bold; }")
        self.label_replacement.setStyleSheet("QLabel { font-weight: bold; }")
        self.label_language.setStyleSheet("QLabel { font-weight: bold; }")

        # 메뉴 바 생성
        self.create_menu_bar()

        # 드래그 드롭 기능 추가
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            self.file_paths = [url.toLocalFile() for url in event.mimeData().urls()]
            self.label_file_paths.setText(f"{len(self.file_paths)}개 항목 선택됨")
            for file_name in self.file_paths:
                logger.info(f"업로드 파일 명 : {file_name}")
            logger.info(f"{len(self.file_paths)}개 파일 업로드 완료")
            event.accept()
        else:
            event.ignore()

    def create_menu_bar(self):
        # 파일 메뉴
        file_menu = self.menuBar().addMenu("파일")

        # "열기" 메뉴 항목 생성
        open_action = QAction("열기", self)
        open_action.setShortcut("Alt+O")
        open_action.triggered.connect(self.browse_files)
        file_menu.addAction(open_action)

        # 종료 액션
        exit_action = QAction("종료", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 도움말 메뉴
        help_menu = self.menuBar().addMenu("도움말")

        # 정보 액션
        about_action = QAction("정보", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def show_about_dialog(self):
        # 도움말 > 정보
        QMessageBox.about(
            self,
            "앱 정보",
            "파일명 바꾸기 앱 v1.0 (운영D팀 전상혁)\n\n"
            "오류 발생시 로그 파일과 함께 공유주시면 감사하겠습니다.\n\n"
            "zzzz955@igsinc.co.kr\n\n"
            "zzzzz955@gmail.com"
        )

    def add_language(self):
        language = self.line_edit_language.text().strip()
        if language:
            # 중복 확인
            if self.check_duplicate_language(language):
                return

            # 입력된 값을 ListWidget에 추가
            item = QListWidgetItem(language)
            self.listwidget_language.insertItem(0, item)
            logger.info(f"변경 기준 추가 완료 : {language}")
            self.line_edit_language.clear()

    def check_duplicate_language(self, language):
        # 중복 확인 함수
        for index in range(self.listwidget_language.count()):
            item = self.listwidget_language.item(index)
            if item.text() == language:
                return True
        return False

    def browse_files(self):
        # 파일 업로드
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        if file_dialog.exec_():
            self.file_paths = file_dialog.selectedFiles()
            self.label_file_paths.setText(f"{len(self.file_paths)}개 항목 선택됨")
        for file_name in self.file_paths:
            logger.info(f"업로드 파일 명 : {file_name}")
        logger.info(f"{len(self.file_paths)}개 파일 업로드 완료")

    def rename_files(self):
        # 파일명 변경
        try:
            self.renameCount = 0
            if not self.file_paths:
                # 파일 존재 여부 확인
                logger.error("파일이 존재 하지 않음")
                return

            self.replacement_string = self.line_edit_replacement.text()
            if not self.replacement_string:
                # 변경 값 존재 여부 확인
                logger.error("변경 값이 존재 하지 않음")
                return

            logger.info(f"입력된 변경값 : {self.replacement_string}")
            for file_path in self.file_paths:
                directory = os.path.dirname(file_path) # 파일 경로 불러 오기
                filename = os.path.basename(file_path) # 파일명 불러 오기
                base_name, extension = os.path.splitext(filename) # 파일명과 확장자 분리

                new_base_name = self.replacement_string
                base_name_lower = base_name.lower()  # 파일명 소문자로 변환

                for i in range(self.listwidget_language.count()):
                    item = self.listwidget_language.item(i)
                    item_text_lower = item.text().lower()  # 변경 기준 소문자로 변환
                    if item_text_lower in base_name_lower:  # 대소문자 구분 없이 비교
                        new_base_name += item.text()  # 변경 값과 변경 기준 결합
                        index = base_name_lower.find(item_text_lower) # 변경 기준 뒤 문자열 찾기
                        if index != -1:
                            new_base_name += base_name[index + len(item_text_lower):] # 변경 기준 뒤 문자열 결합

                        new_filename = new_base_name + extension # 확장자 결합
                        new_file_path = os.path.join(directory, new_filename) # 경로 결합
                        os.rename(file_path, new_file_path) # 파일명 변경
                        logger.info(f"파일명 변경 완료 : {filename} → {new_filename}")
                        self.renameCount += 1

        except Exception as e:
            QMessageBox.critical(self, "파일명 변경 중단", str(e))
            logger.critical(str(e))
            logger.warning("파일명 변경 중단")

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
            self.file_paths = []
            self.label_file_paths.setText("작업 완료.")

        if self.renameCount == 0:
            # 변경된 파일 없음
            QMessageBox.warning(None, "변경된 파일 없음", "이름이 변경된 파일이 없습니다. 파일명 및 포함 단어를 다시 한 번 확인해 주세요.")
            logger.info(f"작업 완료, 변경된 파일명 없음")
            self.label_file_paths.setText(f"{len(self.file_paths)}개 항목 선택됨, 변경 기준 확인 필요")

    def open_folder(self):
        if not self.file_paths:
            logger.error("폴더 열기 실패")
            return

        first_file_path = self.file_paths[0]
        directory = os.path.dirname(first_file_path)

        os.startfile(directory)  # Windows에서 폴더 열기
        logger.info("저장된 폴더 열기 완료")

    def remove_language(self):
        # 변경 기준 삭제
        selected_items = self.listwidget_language.selectedItems() # 선택된 아이템
        for item in selected_items:
            logger.info(f"변경 기준 삭제 완료 : {item.text()}")
            self.listwidget_language.takeItem(self.listwidget_language.row(item))

    def remove_all_languages(self):
        self.listwidget_language.clear()
        logger.info("변경 기준 전체 삭제 완료")

    def appClose(self):
        self.close()
        logger.info("앱 종료")

if __name__ == '__main__':
    app = QApplication([])
    apply_stylesheet(app, theme='dark_teal.xml')
    window = FileRenamer()
    window.show()
    app.exec_()