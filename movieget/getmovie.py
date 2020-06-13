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
        my_data = dict()
        my_data['model'] = "movies.movie"
        if 'original_title' not in ResultData[j].keys():
            ResultData[j]['original_title'] = ''
        if 'release_date' not in ResultData[j].keys():
            ResultData[j]['original_title'] = ''
        if 'popularity' not in ResultData[j].keys():
            ResultData[j]['original_title'] = ''
        if 'vote_count' not in ResultData[j].keys():
            ResultData[j]['original_title'] = ''
        if 'vote_average' not in ResultData[j].keys():
            ResultData[j]['original_title'] = ''
        if 'adult' not in ResultData[j].keys():
            ResultData[j]['original_title'] = ''
        if 'video' not in ResultData[j].keys():
            ResultData[j]['original_title'] = ''
        if 'overview' not in ResultData[j].keys():
            ResultData[j]['original_title'] = ''
        if 'original_language' not in ResultData[j].keys():
            ResultData[j]['original_title'] = ''
        if 'poster_path' not in ResultData[j].keys():
            ResultData[j]['original_title'] = ''
        if 'backdrop_path' not in ResultData[j].keys():
            ResultData[j]['original_title'] = ''
        if 'genre_ids' not in ResultData[j].keys():
            ResultData[j]['original_title'] = ''
        if 'like_users' not in ResultData[j].keys():
            ResultData[j]['original_title'] = ''

        
        my_data['fields'] = ResultData[j]
        # print(ResultData[j].get('title'))
        result.append(my_data)

# print(result)

with open('movie.json', 'w', encoding="utf-8") as make_file:
    json.dump(result, make_file, ensure_ascii=False, indent="\t")