import requests
import pandas as pd
import datetime
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

# select_list 된 url 크롤링 
def pop_list(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    pop_listTag = soup.select_one('div.overflow-x-auto')
    info = pop_listTag.find_all('tr',{'class':'table-group'})

    data_list = []

    for i in info:
        title = i.find_all('div', {'class': 'group-hover:underline'})
        title_text = title[0].get_text().strip()
        title_info = i.find_all('span', {'class': False, 'title': False})
        nation_text = title_info[0].text
        date = title_info[1].text
        genre = title_info[3].text

        sub_info = i.find_all("td", class_="table-td")
        imdb = ''
        tomatoes = ''
        other_info = ''

        for td in sub_info:
            if "platform-imdb" in str(td):  # 평점
                imdb = td.text.strip()
            else:  # 조회수 
                other_info = td.text.strip()
                other_info = other_info.replace(',', '')
        data_list.append([title_text, nation_text, date, genre, imdb, other_info])

    return data_list

url1 = 'https://flixpatrol.com/calendar/new/titles/netflix/'
url2 = 'https://flixpatrol.com/calendar/new/movies/netflix/'
url3 = 'https://flixpatrol.com/calendar/new/tv-shows/netflix/'

netflix_new_titles = pop_list(url1)
netflix_new_movies = pop_list(url2)
netflix_new_shows = pop_list(url3)


with open('./secret','r') as f:
        secret= {l.split('=')[0]: l.split('=')[1].strip() for l in f.readlines()}
token = secret['TELEGRAM_TOKEN']


def send_to_telegram(message):

    chat_id = ''
    url = f'https://api.telegram.org/bot{token}/sendMessage'

    try:
        response = requests.post(url, 
                            json={'chat_id': chat_id, 'text':message}) 
              
    except Exception as e:
        print(e)
        
# 텔레그램으로 크롤링된 list를 netflix_db에 각각 key 값으로 저장
netflix_db ={
    'new_titles':netflix_new_titles,
    'new_movies':netflix_new_movies,
    'new_shows':netflix_new_shows
}

# string을 보기편하게 출력
def print_info(new_list):
    info_str = ""
    for index in new_list:
        title, country, release_date, genre, imdb, votes = index
        info_str += f"제목: {title}\n"
        info_str += f"국가: {country}\n"
        info_str += f"출시날짜: {release_date}\n"
        info_str += f"장르: {genre}\n"
        info_str += f"평점: {imdb}\n"
        info_str += f"votes: {votes}\n"
        info_str += "-" * 20 + "\n"
    return info_str

now = datetime.datetime.now()
# print(now.strftime("%Y년%m월%d일"))


# 텔레그램으로 메세지 전송
async def new(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    target = update.message.text.split()[-1]
    new_list=[]
    
    if target in netflix_db:
        new_list=netflix_db[target]
        info_str = print_info(new_list)
        
        # 메시지길이제한
        max_message_length = 500
        if len(info_str) > max_message_length:
            info_str = "\n"+ "-" * 20+"\n"+ info_str[:max_message_length - 3] + "......"  
            now_t=now.strftime("%Y년 %m월 %d일")
        # await update.message.reply_photo(open('./powerpuffy2.png', 'rb'))
        await update.message.reply_text(f'<{now_t} Netflix의 {target} 리스트!>{info_str}')
    else:
        # await update.message.reply_photo(open('./powerpuffymyself.png', 'rb'))
        await update.message.reply_text('다시 입력해주세요\n어떤 장르의 신규리스트를 알려드릴까요? "new_titles:전체리스트", "new_movies:영화리스트", "new_shows:시리즈리스트"')

app = ApplicationBuilder().token(token).build()       
app.add_handler(CommandHandler("new",new)) 
app.add_handler(CommandHandler("print_movie_info",print_info)) 

# 텔레그램 봇 실행 및 사용자가 select_list 입력하면 함수 호출하여 사용자가 원하는 정보를 계속 받을 수 있음.
if __name__ == '__main__':
    
    select_list = ["/new new_titles", "/new new_movies", "/new new_shows"]
    send_to_telegram(f'지금 Netflix 의 새로운 영상을 알고 싶으시면\n {select_list}\n를 입력해주세요.: ')
    app.run_polling()
