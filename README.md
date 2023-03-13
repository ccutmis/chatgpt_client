# chatgpt_client 使用說明:

昨天我對 chatGPT官網所提供的 Python 範例進行了一些修改，並加入了PySide6的GUI介面，使得使用者可以直接與ChatGPT互動，而無需開啟瀏覽器。此外，使用者還可以將聊天內容儲存為Markdown文件。

-----

# 安裝 chatgpt_client 的需求如下:
1. 擁有OpenAI API金鑰：使用者可以自行上網搜尋 "OpenAI API key"以取得此金鑰。請注意，請勿外流此金鑰或將其儲存在程式碼中。根據 chatGPT官網的設定範例，使用者需將取得的API金鑰設置為環境變數"OPENAI_API_KEY"。 取得 OpenAI API key的網址：https://platform.openai.com/
2. 安裝 Python 3.7 或更高版本：我們推薦安裝 Python 3.10，這樣您還可以試用其他基於Python的開源AI生成圖片專案。在安裝Python時，請確認勾選 "Add Python to PATH"，然後完成安裝。
3. 安裝Python依賴套件：安裝Python完成後，請在命令提示字元(CMD)中輸入以下指令再按Enter送出即可：`pip install pyside6 openai`

-----

當以上步驟都完成後，您即可正常執行 chatgpt_client。您可以使用GIT指令：`git clone https://github.com/ccutmis/chatgpt_client.git` 或者下載 https://github.com/ccutmis/chatgpt_client/archive/refs/heads/master.zip ，並將其解壓縮至 C:\ 底下。例如，解壓後的目錄為：C:\chatgpt_client。然後，執行目錄中的app.py，順利的話，您即可在您的電腦上看到 chatgpt_client 的介面了！