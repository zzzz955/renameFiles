# FileRenamer(v2.0)
이미지 파일명 끝에 특정 단어가 있을 경우 원하는 이름으로 파일명을 일괄 변경해주는 프로그램
글로벌 프로젝트 내 다국어 변경에 대한 리소스 감소를 위해 제작

# mainwindow.py
앱의 메인 화면
폴더 or 여러개의 이미지 파일을 업로드 할 수 있음(드래그 & 드롭 가능)
변경 기준 설정 후 파일명 변경 실행 구동부

# dialogs.py
첨부된 이미지 목록을 확인하거나 파일명 변경 기준을 설정하는 등
mainwindow의 기능을 실행 하기 위해 노출되는 팝업 다이얼로그의 집합 모듈

# classifyimages.py
이미지 경로를 받아 와 가로, 세로 이미지 값을 재전달 해주는 함수 모듈

# jsons.py
변경 내용 저장을 위한 json 파일 생성/작성/불러오기 함수 모듈

# logs.py
로그 기능 함수 모듈
