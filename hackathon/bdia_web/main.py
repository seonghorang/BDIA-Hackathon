from fastapi import FastAPI, HTTPException, Request, Form,Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json
import http.client
from sklearn.feature_extraction.text import TfidfVectorizer
from kiwipiepy import Kiwi
import mysql.connector
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
 
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("login.html", context)

@app.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("signup.html", context)

class CompletionExecutor:
        def __init__(self, host, api_key, api_key_primary_val, request_id):
            self._host = host
            self._api_key = api_key
            self._api_key_primary_val = api_key_primary_val
            self._request_id = request_id
    
        def _send_request(self, completion_request):
            headers = {
                'Content-Type': 'application/json; charset=utf-8',
                'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
                'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
                'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id
            }
    
            conn = http.client.HTTPSConnection(self._host)
            conn.request('POST', '/testapp/v1/completions/LK-D2', json.dumps(completion_request), headers)
            response = conn.getresponse()
            result = json.loads(response.read().decode(encoding='utf-8'))
            conn.close()
            return result
    
        def execute(self, completion_request):
            res = self._send_request(completion_request)
            if res['status']['code'] == '20000':
                return res['result']['text']
            else:
                return 'Error'

class EmotionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def _send_request(self, emotion_request):
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id
        }

        conn = http.client.HTTPSConnection(self._host)
        conn.request('POST', '/testapp/v1/completions/LK-D2', json.dumps(emotion_request), headers)
        response = conn.getresponse()
        result = json.loads(response.read().decode(encoding='utf-8'))
        conn.close()
        return result

    def execute(self, emotion_request):
        res = self._send_request(emotion_request)
        if res['status']['code'] == '20000':
            output_text = res['result']['text']
            lines = output_text.split("\n")
            sentence = lines[2].replace("문장: ", "").strip()
            emotion = lines[3].replace("감정: ", "").strip()
            return sentence, emotion
        else:
            return 'Error'

@app.post("/result", response_class=HTMLResponse)
async def result(request: Request, preset_text: str = Form(...)):
    completion_executor = CompletionExecutor(
            host='clovastudio.apigw.ntruss.com',
            api_key='NTA0MjU2MWZlZTcxNDJiY+f0lJEP2FuLg87WY6ZmzX+jXvott0U9nc1Mo7Mnq0uUSYDx037FEGNP14aIQKCnKnTrPKbDl2UAlpltfggzQ2I1ZSMhGg2fXQ06/iDL9TUkSwb4yfMv9CGHjm/yDd2nWpNwRm1Houn6vvmvfdVT+4bOXHIxvonFa8Gv61V+cfhOKpjIkFBc1tsgfoSwbd0wySIth7vY5lYcb7X8BXRPQ3I=',
            api_key_primary_val = 'a9luzgrsGqbq1M1NbvCkkoOMw4Fdndz0rLxEjotR',
            request_id='b4b5f2d0ae1a47d380affd58c307c76c'
        )
    
    content = f"{preset_text}"
        
    request_data = {
        'text': content,
        'start': '\n교정:',
        'restart': '\n###\n',
        'includeTokens': True,
        'topP': 0.8,
        'topK': 0,
        'maxTokens': 150,
        'temperature': 0.01,
        'repeatPenalty': 8.0,
        'stopBefore': ['###', '문장:', '교정:', '###'],
        'includeAiFilters': True
    }
    
    corrected_text = completion_executor.execute(request_data)
    corrected_text = corrected_text.split('교정:')[1].strip() if '교정:' in corrected_text else corrected_text
    
    emotion_executor = EmotionExecutor(
        host='clovastudio.apigw.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiY+f0lJEP2FuLg87WY6ZmzX8t7ycW9ihSp7lZVgXlSz2mfJLHF9pnt23jyu56TB89BhnfoH69+FnbAfMr+mD5WQzf8XU61C9yFBX3oAuipgYiLfU68d28JMkPmToOeqryQeYHJ/vmdpgFPswFbamQz2p8wLYlIt9WkN8NvRgpKRIOZ6nRVYCWL7uIccA3GSuo9yXiaPSzsE3zNMTVkYYv0es=',
        api_key_primary_val='a9luzgrsGqbq1M1NbvCkkoOMw4Fdndz0rLxEjotR',
        request_id='4bf5982c550f467a8750b44872cfbe01'
    )

    corrected_text = corrected_text.replace("\n", " ")
    
    corrected_text = f"\n###\n문장: {corrected_text}"

    request_data = {
        'text': corrected_text,
        'start': '\n감정:',
        'restart': '\n###\n',
        'includeTokens': True,
        'topP': 0.6,
        'topK': 0,
        'maxTokens': 30,
        'temperature': 0.2,
        'repeatPenalty': 10.0,
        'stopBefore': ['###', '감정:', '질문:', '###'],
        'includeAiFilters': False
    }

    sentence, emotion = emotion_executor.execute(request_data)
    
    sentence = sentence.replace("#","")
    emotion = emotion.replace("#","")
    
    kiwi = Kiwi()

    nouns_list = []
    for st in kiwi.analyze(sentence):
        nouns = [token.form for token in st[0] if token.tag.startswith('NN')]
        if nouns:
            nouns_list.extend(nouns)

    vectorizer = TfidfVectorizer()

    X = vectorizer.fit_transform(nouns_list)

    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = {word: tfidf for word, tfidf in zip(feature_names, X.toarray().sum(axis=0))}

    keywords = sorted(tfidf_scores.keys(), key=lambda x: tfidf_scores[x], reverse=True)[:20]

    context = {"request": request, "text": sentence, "emotion": emotion, "keywords":keywords}
    
    print(context)

    return templates.TemplateResponse("result.html", context)



############로그인
# Database Configuration
DATABASE_URL = "mysql+mysqlconnector://user:data1q2w3e4r!!@db-k4c29-kr.vpc-pub-cdb.ntruss.com/dpvserver"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Model definition
Base = declarative_base()

class Member(Base):
    __tablename__ = "member"
    mem_email = Column(String(50),primary_key=True)
    mem_name = Column(String(20))
    mem_pw = Column(String(50))

@app.get("/member_login")
def login(request: Request, db: Session = Depends(get_db)):
    login_info=(db.query(Member).all())
    return(login_info)

    

