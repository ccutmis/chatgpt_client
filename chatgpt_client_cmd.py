from datetime import datetime
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
conversation_history = []
used_tokens = 0


class fg:
  black = "\u001b[30m"
  red = "\u001b[31m"
  green = "\u001b[32m"
  yellow = "\u001b[33m"
  blue = "\u001b[34m"
  magenta = "\u001b[35m"
  cyan = "\u001b[36m"
  white = "\u001b[37m"

  def rgb(r, g, b): return f"\u001b[38;2;{r};{g};{b}m"

class bg:
  black = "\u001b[40m"
  red = "\u001b[41m"
  green = "\u001b[42m"
  yellow = "\u001b[43m"
  blue = "\u001b[44m"
  magenta = "\u001b[45m"
  cyan = "\u001b[46m"
  white = "\u001b[47m"

  def rgb(r, g, b): return f"\u001b[48;2;{r};{g};{b}m"

def save_chat_record():
    global conversation_history
    answer = input(bg.red+fg.black+"\n確定要 將聊天內容另存為文字檔嗎? (請輸入Y/N) ")
    if answer.strip().upper()=='Y':
        now = datetime.now()
        date_time = now.strftime("%Y%m%d_%H%M%S")
        with open(date_time+'.md','w+',encoding='utf-8') as f:
            f.write("\n ## conversation_history: \n"+str(conversation_history).replace('},',',\n')+'\n\n已使用Tokens: '+str(used_tokens))
        print(bg.yellow+fg.black+'\n另存文檔完成，檔名為:'+date_time+'.md')
    else:
        return

def query_used_tokens():
    print(bg.green+fg.black+'\n目前已使用Tokens: '+str(used_tokens)+'\n')

def submit():
    global conversation_history,used_tokens
    quiz = input(bg.black+fg.white+"\n"+"\n請輸入要向ChatGPT提問的內容(輸入exit退出) : ")
    if quiz.strip() == "": 
        return 0
    elif quiz.strip() == "exit":
        return -1
    conversation_history.append({"role": "user", "content": quiz})
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")

    print(bg.rgb(222,222,222)+fg.rgb(22,22,22)+"\n"+"\n### "+date_time+' 我說 : \n'+quiz+'\n')
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":x['role'],"content":x['content']} for x in conversation_history]
    )
    return_msg = completion.choices[0].message['content']
    conversation_history.append({"role": "assistant", "content": return_msg})
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print(bg.rgb(188,188,188)+fg.rgb(22,22,22)+"### "+date_time+" ChatGPT說 : \n"+return_msg+'\n\n-----\n')
    used_tokens = int(completion["usage"]["prompt_tokens"])
    #print('\n目前已使用Tokens: '+str(used_tokens)+'\n')

def main():
    print("sfsf")

if __name__ == "__main__": 
    while(1):
        my_choice = input(bg.black + fg.white+"\n選擇要執行的動作(1.向ChatGPT提問 2.存檔聊天記錄 3.查詢已用Tokens 4.離開): ")
        if my_choice.strip()=='1':
            while(1):
                if submit()==-1:
                    break
        elif my_choice.strip()=='2':
            save_chat_record()
        elif my_choice.strip()=='3':
            query_used_tokens()
        elif my_choice.strip()=='4':
            break
        else:
            print('\n輸入選擇錯誤…請重試...')
    print(bg.black+fg.white+"\n")
