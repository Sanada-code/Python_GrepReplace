import json
import os
import sys


class Setting:
    setting_path = './config.json'

    def __init__(self, logger):
        # 設定ファイル存在チェック
        if not os.path.isfile(self.setting_path):
            logger.exception(self.setting_path + 'が存在しません')
            # exit(1)

        try:
            # 設定ファイルオープン
            with open(self.setting_path, encoding='utf-8') as f:
                self.jsn = json.load(f, strict=False)
        except:
            # エラーログの出力
            logger.exception('設定ファイルエラー')
            logger.exception(sys.exc_info())
            # exit(1)

    def get_grep_dir(self):
        return self.jsn['GREP_DIR']

    def get_exclude_extension(self):
        ex_list = self.jsn['EXCLUDE_EXT']
        ex_list = list(map(str.lower, ex_list))  # 小文字に変換
        return tuple(ex_list)

    def get_replace_words(self):
        return self.jsn['REPLACE_WORDS']
