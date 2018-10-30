from flask import Flask
app = Flask(__name__)

## route 설정을 해줬다(주소설정)
## 내 서버의 최상단으로 요청했을 때 나는 밑에 것을 리턴할거야 
## /뒤에 아무것도 없을 때 뜨는 것
## local 컴퓨터가 아니라 거기서 돌아가고 있는 외부의 서버중 하나기 때문에 local host가 아니라 고유 url을 가지게 된다. 
## flask는 자동으로 reload가 아니라 서버를 껏다 켜줘야한ㄷㅏ다아아앙
@app.route("/") 
def hello():
    return "빅콘테스트 우승!"
    
@app.route("/welcome")
def welcome():
    return "welcome flask"

@app.route("/html_tag")
def html_tag():
    return "<h1>안녕하셔유</h1>"
## ul은 뭐주?
@app.route("html_line")
def html_lint():
    return """
    <h1> 여러 줄을 보내봐용:)</h1>
    <ul>
        <li>1번</li>
        <li>2번</li>
    </ul>
    """