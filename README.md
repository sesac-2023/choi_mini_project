1. 개요
넷플릭스 신규 VOD 텔레그램으로 알림전송

전세계의 VOD,OTT 시리즈 드라마 또는 영화등을 순위하여 집계하는 사이트인 
flixpatrol에서 제공하는 넷플릭스 최신 VOD 리스트 데이터를 크롤링하여 텔레그램에 전송하였다.


2. 정보

넷플릭스에서 제공하는 신규 업데이트된 VOD 리스트를 원하는 특정 텔레그램 사용자에게 ,
select_list = new_titles:전체리스트", "new_movies:영화리스트", "new_shows:시리즈리스트" 3가지중 선택한 데이터를 크롤링하여 결과를 전송해준다.


3. 결과

텔레그램에 /new new_titles 를 사용자가 입력시에 다음과 같은 메세지를 전송해준다.

<2023년 08월 04일 Netflix의 new_titles 리스트!>
--------------------
제목: The Big Nailed It Baking Challenge (season 1)
국가: United States
출시날짜: 08/04/2023
장르: Quiz Show
평점: 
votes: 
--------------------
제목: Head to Head
국가: Saudi Arabia
출시날짜: 08/03/2023
장르: Comedy
평점: 
votes: 
--------------------
제목: Zom 100: Bucket List of the Dead
국가: Japan
출시날짜: 08/03/2023
장르: Comedy
평점: 6.3/10
votes: 12
--------------
......