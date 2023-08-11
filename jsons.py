import json

def load_data():
    with open('data.json', 'r', encoding='utf-8') as file:
        # data.json 불러와 mainwindow에 데이터 전달
        data = json.load(file)
        data_list = data.get('datas', [])
        criteria_val = data.get('criteria_val', [])
        table_data = []
        for data in data_list:
            tmp_data = []
            for _, value in data.items():
                tmp_data.append(value)
            table_data.append(tmp_data)
        return table_data, criteria_val

def save_data(fending_data):
    # mainwindow에서 데이터 전달 받아 data.json 작성
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(fending_data, file, ensure_ascii=False, indent=2)