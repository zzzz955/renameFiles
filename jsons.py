import json




def from_json(self, data):
    # JSON 데이터에서 보상 정보를 가져와서 reward_table에 추가합니다.
    rewards = data.get('rewards', [])
    for reward in rewards:
        reward_type = reward.get('reward_type', '')
        reward_count = reward.get('reward_count', '')
        reward_info_id = reward.get('reward_info_id', '')
        item_bind = reward.get('item_bind', '')
        event_item_period_info_id = reward.get('event_item_period_info_id', '')
        self.add_reward_to_table(reward_type, reward_count, reward_info_id, item_bind, event_item_period_info_id)

        tab_name = data.get('tab_name', '보상')
        self.main_window.tab_widget.setTabText(self.main_window.tab_widget.indexOf(self), tab_name)


def load_data(self):
    # data 파일 불러오기 함수
    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            tab_data_list = data.get('tabs', [])
            for tab_data in tab_data_list:
                tab = MainTab(self)
                tab.from_json(tab_data)
                tab_index = self.tab_widget.addTab(tab, tab_data.get('tab_name', '보상'))
                self.tab_widget.setCurrentIndex(tab_index)

    except Exception as e:
        QMessageBox.warning(self, '오류', f'불러올 데이터가 없거나, 데이터 로드 중 오류가 발생했습니다: {str(e)}')
        self.add_tab()


def save_data(fending_data):
    # data 파일 저장 함수
    '''tab_data_list = []
    for tab_index in range(self.tab_widget.count()):
        tab = self.tab_widget.widget(tab_index)
        tab_data = tab.to_json()
        tab_data_list.append(tab_data)'''

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(fending_data, file, ensure_ascii=False, indent=2)

