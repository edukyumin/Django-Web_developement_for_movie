# final_pjt (진석 and 규민)

> - 사전 설치리스트
>   - python -m venv venv
>   - source venv/Scripts/activate
>   - pip install django==2.1.15
>   - pip install django-bootstrap4
>   - pip install requests
> - 공유방법 : github
>   - https://github.com/edukyumin/Web_Django_for_Movie.git
>   - https://github.com/qlraor09/Django_Movie_pjt

## 진행 현황

### day1_0611

- 프로젝트 사전준비

  - Model 정의
    - accounts
      - User
        - followers
    - movies
      - Genre
        - name
      - Movie
        - title
        - original_title
        - release_date
        - popularity
        - vote_count
        - vote_average
        - adult
        - video
        - overview
        - original_language
        - poster_path
        - backdrop_path
        - `genre_ids`
        - `like_users`
      - Review
        - title
        - rank
        - content
        - created_at
        - updated_at
        - `user`
        - `movie`
      - Comment
        - content
        - created_at
        - updated_at
        - `review`
        - `user`

  

  - Base.html 생성

    - nav bar 를 위한 bootstrap4 사용

  - Accounts app

    - 기존 프로젝트의 accounts apps 클론코딩

  - Movies app

    

### day2_0612

- TMDB 서버 API 가져오기
  - fixtures/getmovie.py 함수 생성
  - movie.json / genres.json 두 파일 업로드
    - `python manage.py loaddata '경로'`
- index (movie_list) 생성
- movie create 생성
- movie_detail 생성

### day3_0613

- API 로 가져온 데이터중 null 값 혹은 key 없는것 해결
  - models에 `null=True` 추가
- bootstrap4 를 통한 스타일링

### day4_0614

- movie_create 중 genres 입력되지 않는 문제 진행중
- 기타 문제점 정리
- 빠진 기능 정리

### day5_0615





## 문제발생 + 해결방법

- `Templates no found` Error 발생
  - 각 apps의 templates 안에 또한번의 경로 만들어주어 해결!
- API 가져오기 굉장히 어려웠다. 특히 원하는 json의 구조와 주어진 json의 구조가 다름을 처리하기 어려웠다.
  - 알고리즘적 해결
  - 빈 `dictionary`를 만든 후 requests로 받아온 json 파일을 원하는 구조로 바꾸는 함수를 getmovies.py 에 생성
  - gengre는 따로 가져온다
  - 그 후 두 파일 `loaddata`
- `movie_create`