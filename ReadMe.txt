■概要
Gerp置換を行います

指定フォルダ内のファイルを検索し
設定した文字列に置換します


■使い方
config.json に各種設定後、replace_file.exeを実行

■config.json
　GREP_DIR：置換対象のパスを記述（再帰的にサブフォルダも対象）
　
　EXCLUDE_EXT：	除外する拡張子
　
　REPLACE_WORDS：置換する文字列セット｛置換前, 置換後｝