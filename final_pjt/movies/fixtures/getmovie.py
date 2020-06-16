import requests
import json
TMD_KEY = '39bcb34e0b2ceaa2f7ca06393ab5a458'

result = []
for i in range(1, 51):
    page_num = i
    url = f'https://api.themoviedb.org/3/discover/movie?api_key={TMD_KEY}&language=ko-KR&page={page_num}'

    ListData = requests.get(url)
    # print(ListData)
    JsonData = ListData.json()
    ResultData = JsonData.get('results')
    # print(ResultData)
    # print(len(ResultData))
    # print(ResultData)

    
    # my_data = dict()
    for j in range(len(ResultData)):
        if ResultData[j]['poster_path'] != None:
            if ResultData[j]['vote_average'] != 0:
                if len(ResultData[j]['genre_ids']) > 0:
                    if ResultData[j]['overview'] != "" :

                        my_data = dict()
                        my_data['model'] = "movies.movie"
                        

                        # if 'original_title' not in ResultData[j].keys():
                        #     ResultData[j]['original_title'] = '1'
                        # if 'release_date' not in ResultData[j].keys():
                        #     ResultData[j]['release_date'] = '1'
                        # if 'popularity' not in ResultData[j].keys():
                        #     ResultData[j]['popularity'] = '1'
                        # if 'vote_count' not in ResultData[j].keys():
                        #     ResultData[j]['vote_count'] = '1'
                        # if 'vote_average' not in ResultData[j].keys():
                        #     ResultData[j]['vote_average'] = '1'
                        # if 'adult' not in ResultData[j].keys():
                        #     ResultData[j]['adult'] = '1'
                        # if 'video' not in ResultData[j].keys():
                        #     ResultData[j]['video'] = '1'
                        # if 'overview' not in ResultData[j].keys():
                        #     ResultData[j]['overview'] = '1'
                        # if 'original_language' not in ResultData[j].keys():
                        #     ResultData[j]['original_language'] = '1'
                        # if ResultData[j]['poster_path'] == None:
                        #     ResultData[j]['poster_path'] = 'https://www.seoularts.ac.kr/Web-home/func/familyCompany/images/noimg.jpg'
                        # if ResultData[j]['backdrop_path'] == None:
                        #     ResultData[j]['backdrop_path'] = 'https://www.seoularts.ac.kr/Web-home/func/familyCompany/images/noimg.jpg'


                        # if 'genre_ids' not in ResultData[j].keys():
                        #     ResultData[j]['original_title'] = '1'
                        # if 'like_users' not in ResultData[j].keys():
                        #     ResultData[j]['original_title'] = '1'
                        
                        my_data['fields'] = ResultData[j]
                        # print(ResultData[j].get('title'))
                        result.append(my_data)

# print(result)

with open('movies.json', 'w', encoding="utf-8") as make_file:
    json.dump(result, make_file, ensure_ascii=False, indent="\t")