1.使い方
以下のURLからmy_functions_2.pyをダウンロードし、auto_backup.pyと同じディレクトリに置いてください
https://drive.google.com/open?id=1M3GIC3Kb6mgzsd_U3grE2Wv1ASUdPFfI
Windowsではコマンドプロンプト、MacではTerminalにコマンドを入力することでバックアップが開始されます。
backup_configファイルを書き換えることでバックアップ元のディレクトリ、バックアップ先のディレクトリなどを指定できます。backup_configファイルについては1.3をご覧ください。

1.1 Windowsでの使い方
auto_backup.pyが含まれているディレクトリにcdコマンドで移動します。
=>cd [auto_backup.pyが含まれているディレクトリのパス]
例）cd C:/Users/XAIZA/Documents/auto_backup/
auto_backup.pyを実行します。半角スペースの後ろにbackup_configファイルのパスを指定します。
=>py auto_backup.py [backup_configファイルのパス]
例）py auto_backup.py backup_config.ini

1.2 Macでの使い方
auto_backup.pyが含まれているディレクトリにcdコマンドで移動します。
=>cd [auto_backup.pyが含まれているディレクトリのパス]
例）cd C:/Users/XAIZA/Documents/auto_backup/
auto_backup.pyを実行します。半角スペースの後ろにbackup_configファイルのパスを指定します。
=>python auto_backup.py [backup_configファイルのパス]
例）python auto_backup.py backup_config.ini

1.3 backup_configファイル
[input]のdirectory_pathにはバックアップ元のディレクトリのパスを指定してください。
=>directory_path = [バックアップ元のディレクトリのパス]
例）directory_path = C:/Users/XAIZA/Documents/
[input]のdirectory_structure_pathにはdirectory_structureファイルのパスを指定してください。directory_structureファイルについては2.1をご覧ください
=>directory_structure_path = [directory_structureファイルのパス]
例）directory_structure_path = C:/Users/XAIZA/Documents/auto_backup/directory_structure.json
[input]のfault_list_pathにはfault_listファイルのパスを指定してください。fault_listファイルについては2.2をご覧ください
=>fault_list_path = [fault_listファイルのパス]
例）fault_list_path = C:/Users/XAIZA/Documents/auto_backup/fault_list.txt
[output]のdirectory_pathにはバックアップ先のディレクトリのパスを指定してください。
=>directory_path = [バックアップ先のディレクトリのパス]
例）directory_path = G:/backup/XAIZA-PC/20200506/


2. directory_structureファイルとfault_listファイル
2.1 directory_structureファイル
バックアップ元となったディレクトリの構造と更新日時が記録されているファイルです。directory_structureファイルを参照することで前回バックアップを行って以来、あるファイルに更新があったかどうかを確認し、更新があった場合はバックアップの対象となります。また、directory_structureファイルに含まれていないファイルは必ずバックアップの対象となります。
2.2 fault_listファイル
バックアップを試みたが失敗した場合、fault_listファイルに失敗したファイルやディレクトリのパスが記録されます。
