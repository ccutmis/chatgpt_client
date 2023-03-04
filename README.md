# chatgpt_client 使用說明

昨天把 chatGPT官網的 api for python 範例作一些修改，加上用 PySide6 做的 GUI 介面，就可以不用開網頁直接跟ChatGPT互動了。也可以把聊天內容另存為markdown文件。

# chatgpt_client 需求:
1. OpenAi api key : 可以自行上網搜尋 'OpenAi api key'，請注意這個不要外流，也不要把它寫在程式裡面，以 chatGPT官網的範例說明，取得OpenAi api key之後，要把它設為本機電腦的環境變數"OPENAI_API_KEY"。 ( 取得 OpenAi api key的網址 : [https://platform.openai.com/](https://platform.openai.com/) )

2. 安裝 Python 3.7 之後的版本 : 推薦安裝 Python 3.10，這樣還可以玩一些其它的 Python 開源 AI 生成圖片的專案，在安裝 Python 時請記得把 "Add to PATH"勾選，再進行安裝。

3. 安裝 Python 依賴套件 : 安裝 Python 完成後，進到命令提示字元(CMD)，輸入 `pip install pyside6 openai`

上列步驟都正確完成後，就可以正常執行 chatgpt_client，你可以用 GIT指令 `git clone http://github.com/ccutmis/chatgpt_client.git` 或是 下載 [https://github.com/ccutmis/chatgpt_client/archive/refs/heads/master.zip](https://github.com/ccutmis/chatgpt_client/archive/refs/heads/master.zip) 並將它解壓縮到 C:\ 底下，例如: C:\chatgpt_client，然後執行裡面的 app.py 順利的話就能看見聊天圖型介面了!
