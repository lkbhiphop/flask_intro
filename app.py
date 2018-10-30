import random
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import csv
import datetime

app = Flask(__name__)

## route 설정을 해줬다(주소설정)
## 내 서버의 최상단으로 요청했을 때 나는 밑에 것을 리턴할거야 
## /뒤에 아무것도 없을 때 뜨는 것
## local 컴퓨터가 아니라 거기서 돌아가고 있는 외부의 서버중 하나기 때문에 local host가 아니라 고유 url을 가지게 된다. 
## flask는 자동으로 reload가 아니라 서버를 껏다 켜줘야한ㄷㅏ다아아앙\
## git add . 하면 지금 내가 있는 working directory에 있는 모든 파일을 올리겟다
## git status 
## app.py는 tracking을 하고 있는데 감지하고 있고
## 빨간색으로 뜨면 add가 안되어있다는 뜻이다. 
## git remote add origin https://github.com/lkbhiphop/flask_intro.git
## git 프로그램 remote 명령어 사용 뒤에 있는 주소의 이름을 origin이라는 별명을 붙혀준다는 뜻이다.
## git remote -v 하면 어떤 원격저장소가 되어잇는지 써있다. \
## git push -u origin master
## -u 옵션은? 
## master 는 branch 명 하나의 가지를 하나의 branch라고 하고 그 branch의 이름이 master다
@app.route("/") 
def hello():
    return render_template("root.html")
    
@app.route("/welcome")
def welcome():
    return "welcome flask"

@app.route("/html_tag")
def html_tag():
    return "<h1>안녕하셔유</h1>"
## ul은 뭐주?
@app.route("/html_line")
def html_lint():
    return """
    <h1> 여러 줄을 보내봐용:)</h1>
    <ul>
        <li>1번</li>
        <li>2번</li>
    </ul>
    """

# html 파일을 받기
# template 폴더만들기(안에 있는 거를 사용해여ㅑ하는데 같은 레벨에 있어야 사용이 가능)
# render_template import하기
@app.route("/html_file")
def html_file():
    return render_template("file.html")


@app.route("/hello_p/<string:name>")  # string 데이터 타입으로 name이라는 변수에 받을 것이다. 받아들일 수 있는 route로 처리할 것이다.
## 고정 url이 아니라 app.route에 hello에 어떤 문자가 들어와도 상관없지만 이를 name이라는 이름으로 부를께라는 뜻이다.
def hello_p(name):
    return render_template("hello.html",user_name = name) # name이라는 매개변수를 사용하는 방법 html 뒤에 name 을 쓴다.
        
## client 쪽에서 hello/창희 라고 보내면 name이라는 변수로 저장되서 hello name이라는 변수로 들어가고 
## hello.html에서 user_name을 사용할 수 잇다. 

## template안에만 이름을 적으면 파일경로를 설정안해도 되는것이다.
## 검색 요령: flask route integer
@app.route("/cube/<int:number>")
def cube(number):
    result = number**3
    return render_template("cube.html",triple = result, number = number)

# html안에서 파이썬 문법을 사용할 수 있다.
# triple = result에서 triple이 바로 html파일에서의 변수 / result는 python파일내에서 변수
# backend에서 연산을 다해야한다 html은 변수만 가져와서 사용하는 것이다. 

@app.route("/lunch")
def lunch():
    menu = ["감자","고구마","스파게티","김밥"]
    return render_template("lunch.html",pick = random.choice(menu))

@app.route("/lunch_p")
def lunch_p():
    menu = ["감자","고구마","스파게티","김밥"]
    picture = {"감자":"https://s-i.huffpost.com/gen/3940536/thumbs/o-3-570.jpg?7",
               "고구마":"https://img1.daumcdn.net/thumb/R720x0/?fname=http://t1.daumcdn.net/liveboard/realfood/bee4ea5e3e8c491d8353e531be0aaec4.jpg",
               "스파게티":"http://recipe1.ezmember.co.kr/cache/recipe/2015/06/08/a2464362f70de9c32b802926d178cb5a.jpg",
               "김밥":"http://recipe1.ezmember.co.kr/cache/recipe/2015/04/04/0461907459756bc3a56472da407a1a9d1.jpg"}
    today_menu = random.choice(menu)
    today_picture = picture[today_menu]
    return render_template("lunch.html",text = today_menu, image = today_picture)
    ## alt = 무슨사진 
    ## <img src={{image}} alt = "음식사진" width = "300" height = "300" >
@app.route("/lotto")
def lotto():
    lotto_num = list(range(1,46))
    lucky = random.sample(lotto_num,6)
    return render_template("lotto.html", lotto_num = sorted(lucky))

## {% for num in lotto_num%}
##                 <h2>{{num}}</h2>
## {% endfor %}  
## indent로 구분이 불가능하기 떄문에 endfor라는 명확한 끝을 표시해줘야한다. 


## 우리페이지에서 데이터를 담아서 네이버에 요청하는 것 (대리로 검색해주는 것)
@app.route("/naver")
def naver():
    return render_template("naver.html")
    
## form 태그에 대해서 배울것이다.
## <input type="text" name=""/>
## <input type="submit" value="Submit"/>
## form은 input으로 받은 데이터를 가져와서 action에 있는 route로 보낸다. 
# input은 닫는태그가 없다.
# <input type="text" name=""/> 
# name="" -> input데이터를 담을 변수의 이름을 정한다. 
# type ="submit" --> 제출이라는 단어가 나온다.
# https://search.naver.com/search.naver?query=%EB%A9%80%EC%BA%A0
# ?전반부는 어디로 보낼지
# ?후반부는 뭐를 보낼지(네이벗에서는 query라는 파라미터변수를 이용해야한다.)

@app.route("/google")
def google():
    return render_template("google.html")
    
    
@app.route("/hell")
def hell():
    return render_template("hell.html")
#<form action = "/hi"> hi라는 경로가 어디로 가냐?
# 우리서버 뒤에 hi라는 경로로 온다. 
# hi? 뒤에 입력값이 달린다.


# 위에 from flask import request 를 한다.
# hi라는 route를 열어준다.
@app.route("/hi")
def hi():
    user_name = request.args.get("name") # 물음표 뒤에있는 name이라는 파라미터의 값을 가져올 것이다.
    return render_template("hi.html",user_name=user_name)

## 우리는 hi?name=창희 라는 라우팅을 열지 않았다
## ?뒤에는 파라미터값으로 받은 것이다. 
## html에서 이미 name이라는 변수를 받아서 받아오는 것이다. 
## name에 들어가는 변수명을 가져올 것이다. 
#3 <form action = "/chucheon"> 
## action은 액션을 했을 때의 경로말해주기


@app.route("/dododo")
def whatyoudo():
    return render_template("dododo.html")
    
@app.route("/chucheon")
def doitdoit():
    today_missions = ["반팔, 반바지 입고 아이스크림먹기","빨래집게 꼽고 다니기","얼굴낙서하고 편의점 가기"
                        , "머리 삭발하기", "딱밤맞고 머리박살나기"]
    today_mission_picture = {"반팔, 반바지 입고 아이스크림먹기":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQvbQj5ExCzDcWWuxSOE4lq2FohyvJR9rlD3NY_6bGywyFieNkV",
                             "빨래집게 꼽고 다니기":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQdJZOpo0CLhdIvqY6B-MwMeEfwrkOPZ1Ld2fPaxGMCVoOeRmlL",
                             "얼굴낙서하고 편의점 가기":"https://i.ytimg.com/vi/ZZymJ5f2Vuc/maxresdefault.jpg",
                             "머리 삭발하기":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSsiwdUnOG_IUQAx81nDtRZ59R1lhyB_ucD3jI-ZXH-I6yZ2oPp",
                             "딱밤맞고 머리박살나기":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTPhDffdK76YBgu7L8DSJZ3gtHJSfRFezo8HuD1PVK67DoLBeKK"}
    today_mission = random.choice(today_missions)
    mission_picture = today_mission_picture[today_mission]
    user_name = request.args.get("name")
    return render_template("chucheon.html",user_name = user_name,today_mission= today_mission, mission_picture = mission_picture )
    
    
## 연관성 있고 입력과 연관성이 있는거하기 

# 입력을 받을 url
@app.route("/summoner")
def summoner():
    return render_template("summoner.html")
    
# 검색을 실행할 url    
@app.route("/opgg")
def opgg():
    summoner = request.args.get("summoner")
    url = "http://www.op.gg/summoner/userName="
    print(url+summoner)
    # summoner와 url을 합친다.
    html = requests.get(url+summoner).text
    ## 요청을 보내면 응답만 받는 것이고, .text를 해야 그것에 대한 html문서를 받는 것이다.
    soupob = BeautifulSoup(html,"html.parser")
    wins = soupob.select('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.TierBox.Box > div.SummonerRatingMedium > div.TierRankInfo > div.TierInfo > span.WinLose > span.wins')
    losses = soupob.select('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.TierBox.Box > div.SummonerRatingMedium > div.TierRankInfo > div.TierInfo > span.WinLose > span.losses')
    # select는 list를 반환한다. 오른쪽 조건에 맞는 모든 리스트를 반환한다.
    # select_one은 태그객체를 반환한다.
    # win타입이 bs4의 element기때문에 바로 리턴이 불가능하다.
    if len(wins) == 0:
        wins_i = "0패"
    else:
        wins_i = wins[0].text
    if len(losses) == 0:
        losses_i = "0패"
    else:
        losses_i = losses[0].text
    
    # csv파일로 자료 저장하기
    # import csv csv파일저장을 위해
    # import datetime 시간처리를 위해
    f = open("list.csv","a+", encoding = "utf-8", newline="")
    # csv.writer() 메소드를 이용해서 csv객체를 만든다.
    csvfile = csv.writer(f)
    # datatime.now로 현재시각을 넣는다.
    data = [summoner, wins_i, losses_i, datetime.datetime.now()]
    csvfile.writerow(data)
    f.close()
    
    # 일반 txt 파일로 저장하기
    
    # f = open("list_txt","a+") # a는 append의 의미이다.
    # python file 저장방법
    # r w a 라는 옵션이 있는다
    # 나중에 설명 :)
    # data에 정보를 넣고 이를 작성한다.
    # data = "소환사의 이름은 {} {}승 {}패 입니다.".format(summoner,wins_i,losses_i)

    # f.write(data)
    # f.close()
    return render_template("opgg.html",summoner=summoner, wins_i = wins_i, losses_i = losses_i)
    
@app.route("/log")
def log():
    f = open("list.csv","r",encoding='utf-8')
    logs = csv.reader(f)
    return  render_template("log.html",logs= logs)