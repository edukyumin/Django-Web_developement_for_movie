# 삼성청년소프트웨어 아카데미(SSAFY) Final Project!

> Django 기반의 웹 개발 (Front & Back end)
>
> User 선호도 기반의 영화 추천 알고리즘

## 1. 개발 도구

- 프론트엔드 

  - `HTML` / `CSS` / `JavaScript`

  - `Bootstrap` / `Axios`

- 백엔드

  - `Django` / `Python`

## 2. 개발 과정

- The Movie Database (`TMDb`)의 API를 통한 영화 데이터 수집

- `ERD`를 이용한 Modeling

- Accouts 앱 개발

  - `signup`, `login` , `logout`, `profile` , `follow`

- Movies 앱 개발

  - 영화 목록

    - `index`,`movie_create` , `movie_update` , `movie_delete` , `like`

  - 관람 후기

    -  `create` , `detail` , `review_detail` , `update`, `delete` 

  - 후기 댓글

    - `comments_create`, `comments_delete`

  - 영화 추천

    > User 선호도별 영화 추천, filtering

    - `choice_create`, `recommend`



## 3. 구현 결과

- Home (index)

  ![index](C:\Users\82102\Desktop\SSAFY온라인\projects\Final_pjt_Github용\Readme.assets\index.png)

- Movie_detail

  ![detail](C:\Users\82102\Desktop\SSAFY온라인\projects\Final_pjt_Github용\Readme.assets\detail.png)

- Profile

  ![profile](C:\Users\82102\Desktop\SSAFY온라인\projects\Final_pjt_Github용\Readme.assets\profile-1592740208212.png)

- Movie_recommend

  ![recommend](C:\Users\82102\Desktop\SSAFY온라인\projects\Final_pjt_Github용\Readme.assets\recommend.png)

- Review

  ![review](C:\Users\82102\Desktop\SSAFY온라인\projects\Final_pjt_Github용\Readme.assets\review.png)





## 4. 주의사항 (개발자 용)

- 사전 환경
  - `python -m venv venv` 명령어를 통해 가상환경 구축
  - `source venv/Scripts/activate` 로 가상환경 켜기
  - `pip install django=2.1.15`
  - `pip install django-bootstrap4`
  - `pip install requests 실행`
- 영화 수집은 final_pjt > movies > fixtures > getmovie.py 함수 실행

- `Youtube_api_key` 문제로 `View.py`의 `index`함수와 `detail` 함수에 주석처리 되어있습니다.
  - 만약 `영화 예고편`이 제생되지 않는다면 YOUTUBE_API_KEY를 재발급 받는다
    - https://console.developers.google.com/
- 구현중 `recommend` 가 아닌 `recommand` 로 되있는 부분이 있음.

