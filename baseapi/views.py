import requests
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError

def index(request):
    movie=[]
    if request.method=="POST":
        search_url="https://api.themoviedb.org/3/search/movie"
        params = {
                'query' : request.POST['search'],
                'api_key' : settings.MOVIE_DATA_API_KEY,
        }
    
        r=requests.get(search_url,params=params)
        print(r)
        s=r.json()['results']
        print(s)
        for result in s:
            movies={
                'title':result['title'],
                'overview':result['overview'][:100],
                'release':result['release_date'],
                'poster':result['poster_path'],
            }
            movie.append(movies)
    context={
        'movie':movie
    } 
        
    return render(request,'html/search.html',context)


def recomend(request):
    movie_list=[]
    url_recomend='https://api.themoviedb.org/3/trending/movie/day'
    params= {
        'api_key' : 'e6f1e03ae70bc830f87e22213e3038a3'
    }
    r=requests.get(url_recomend,params=params)
    s=r.json()['results']

    for result in s:
        movies={
            'title':result['title'],
            'overview':result['overview'][:100],
            'release':result['release_date'],
            'poster':result['poster_path'],
        }
        movie_list.append(movies)
    
    context = {
        'movie_list':movie_list
    }
    return render(request,'html/movie.html',context)






# movielist=[]
#     r=requests.get(search_url,params=params)
#     s=r.json()['results']
#     # print(r.json()['results'][0]['title'])
#     # print(r.json()['results'][0]['overview'][:50])
#     # print(r.json()['results'][0]['release_date'])
#     # print(r.json()['results'][0]['poster_path'])
#     for result in s:
#         movielist.append(result['title'])
#         movielist.append(result['overview'])
#         movielist.append(result['release_date'])
#         movielist.append(result['poster_path'])
#         movielist.append(result['id'])
#     # movie_params={
#     #     'api_key' : settings.MOVIE_DATA_API_KEY,
#     #     'movie_id' : '157336'
#     # }    
#     # r=request.get(movie_url,params=movie_params)
#     # print(r.text)
        
#     return render(request,'baseapi/index.html')

