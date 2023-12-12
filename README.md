# BDIA-Hackathon

<h2>쓱싹쓱싹 그림일기</h2>

<p align="center">
<img src="https://github.com/seonghorang/seonghorang/blob/main/img/hackathon.png" width="600" height="300" style="float: right;">
</p>


### **부산광역시/부산정보산업진흥원**
### **기간:** 2023.12.09 ~ 2023.12.10 (24시간/5인)

## 목표
- 사용자의 글을 분석해 주제와 감정을 반영한 이미지를 제공
- 텍스트의 시각화로 풍부해진 표현기능을 제공
- 자발적인 데이터 생성을 유도하여 사용자의 라이프로그를 축적하고자함

## 데이터
- sketches_png_zip 데이터셋

## 구현
- 사용자는 웹 인터페이스를 통해 텍스트(일기)를 입력합니다.
- 입력된 텍스트는 CLOVA Studio β의 HyperCLOVA X 언어 모델과 CLOVA Sentiment를 통해 감정분석이 됩니다.
- 분석된 결과는 TF-IDF 가중치 계산을 통해 키워드로 변환됩니다.
- 키워드를 바탕으로 그림일기에 필요한 이미지가 생성됩니다.

## 역할
- naver CLOVA Sentiment & CLOVA Studio를 활용한 사용자 텍스트 속 감정 분석
- TF-IDF 가중치 계산을 통한 사용자 텍스트 속 키워드 분석
- sketches_png_zip 데이터셋과 키워드 간 데이터 매핑 작업

## 사용 프로그램
- 언어 : Python
- 협업 : Notion, Discord
- 전처리 : Python(Pandas, Numpy)
- 분석 : ncloud(CLOVA Sentiment, CLOVA Studio, CLOVA Summary)
- 웹 : HTML/CSS, Javascript, django, fastapi

## 고찰
- CLOVA Studio의 감정분석 모델등의 API활용에 대한 숙련도가 낮아 필드의 데이터를 모두 확인하지 못했는데, 시간이 더 있었더라면 계획했던 세부 감정들의 이모지화를 구현할 수 있었을 것이라는 아쉬움이 남습니다.
- 감정분석 모델의 더욱 정교한 정확도를 위해 튜닝을 진행하고 싶었지만 시간적 문제와 숙련도 문제로 약간의 교정밖에 적용하지 못했습니다. 주어진 시간이 충분하였더라면 관련 자료를 집중적으로 찾아보며 보다 정교한 커스텀 모델을 만들 수 있었을 것이라는 아쉬움이 남아있습니다.
- 문법 교정 모델을 사용하여 문장의 맞춤법을 검사하는 과정에서, 상관 없는 문장이 첨언되거나 영어나 중국어로 번역되는 등의 오류가 발생했습니다. 파라미터를 조정하여 해결해보려 하였으나 완전히 해결하지 못하여 아쉬움이 남습니다.
- 스키마추론이 가능하여 DB조회와 적재를 빠르고 편리하게 해주었으나, 중간에 연결오류로 최종적으로 코드를 완성하지 못하여서 아쉬움이 큽니다.
