import requests
from django.conf import settings
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from . models import Movie
import urllib
from .forms import MovieForm
import traceback
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User,auth
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
User = get_user_model()
@login_required(redirect_field_name="log")
def index(request):
    movie=[]
    # try:
    if request.method=="POST":
        if "taskAdd" in request.POST:
            print(list(request.POST.items()))
            title=request.POST["title"]
            release=request.POST["release"]
            poster=request.POST["poster"]
            vote_average=request.POST["vote_average"]
            movie_id=request.POST["movie_id"]
            task=Movie(title=title,release=release,poster=poster,vote_average=vote_average,movie_id=movie_id,admin=request.user)
            task.save()
            return redirect('/search')
        search_url="https://api.themoviedb.org/3/search/movie"
        params = {
                'query' : request.POST['search'],
                'api_key' : settings.MOVIE_DATA_API_KEY,
        }
    
        r=requests.get(search_url,params=params)
        s=r.json()['results']
        for result in s:
            movies={
                'id':result['id'],
                'title':result['title'][:15],
                'overview':result['overview'][:100],
                'release':result['release_date'],
                'poster':result['poster_path'],
                'vote_average' :result['vote_average'],
            }
            movie.append(movies)
    context={
        'movie':movie
    } 
    return render(request,'html/search.html',context)
    # except Exception as error:
    #     print(error)
    #     traceback.print_exc()
        
    # return render(request,'html/no_internet.html')


def error_404_view(request, exception):
    data = {"name": "ThePythonDjango.com"}
    return render(request,'html/error.html', data) 

@login_required(redirect_field_name="log")
def trending(request):
    movie_list=[]
    try:
        if request.method=="POST":
            if "taskAdd" in request.POST:
                title=request.POST["title"]
                release=request.POST["release"]
                poster=request.POST["poster"]
                vote_average=request.POST["vote_average"]
                movie_id=request.POST["movie_id"]
                task=Movie(title=title,release=release,poster=poster,vote_average=vote_average,movie_id=movie_id,admin=request.user)
                task.save()
                return redirect('/')
        url_recomend='https://api.themoviedb.org/3/trending/movie/day'   
        params= {
            'api_key' : settings.MOVIE_DATA_API_KEY,
        }
        r=requests.get(url_recomend,params=params)
        s=r.json()['results']

        for result in s:
            movies={
                'id':result['id'],
                'title':result['title'][:15],
                'overview':result['overview'][:110],
                'release':result['release_date'],
                'poster':result['poster_path'],
                'vote_average' :result['vote_average'],
            }
            movie_list.append(movies)
            # print(movie_list)
        
        context = {
            'movie_list':movie_list
        }
        return render(request,'html/movie.html',context)
    except:
        print('no internet')
    return render(request,'html/no_internet.html')  


  
@login_required(redirect_field_name="log")
def cast(request, id):
    try:
        movie_list=[]
        crew_list=[]
        #similar movies list
        similar_list=[]
        genere_list=[]
        url_data='https://api.themoviedb.org/3/movie/{}?&append_to_response=videos,credits'.format(id)
        url='https://api.themoviedb.org/3/movie/{}/similar'.format(id)
        params= {
            'api_key' : settings.MOVIE_DATA_API_KEY,
        }
        response=requests.get(url_data,params=params)
        data=response.json()
        original_title=data['original_title'][:15]
        overview=data['overview']
        release=data['release_date']
        tagline=data['tagline'][:45]
        vote_average=data['vote_average']
        video = data['videos']['results'][0]['key']
        generes=response.json()['genres']
        for genere in generes:
            genere= {
                'name':genere['name']
            }
            genere_list.append(genere)
        #similar movies request    
        r=requests.get(url,params=params)
        alldata=r.json()['results']
        for i in data['credits']['cast']:
            movies={
                'character': i['character'],
                'profile_path': i['profile_path'],
            }
            movie_list.append(movies)
        for j in data['credits']['crew']:
            movie= {
                'name':j['name'][:14],
                'job':j['job'][:15],
                'profile':j['profile_path'],
            }
            crew_list.append(movie)
        for result in alldata:
            movies={
                'id':result['id'],
                'title':result['title'],
                'release':result['release_date'],
                'poster':result['poster_path'],
                'vote_average':result['vote_average'],
            } 
            similar_list.append(movies)   
        context = {
            'movie_list':movie_list,
            'overview':overview,
            'video' :video,
            'original_title' : original_title,
            'similar_list' : similar_list,
            'crew_list':crew_list,
            'tagline':tagline,
            'release':release,
            'vote_average':vote_average,
            'genere_list':genere_list
            
            
        }
        return render(request,'html/cast.html',context)
    except:
        print('no internet')
    return render(request,'html/no_internet.html')

@login_required(redirect_field_name="log")
def movielist(request):
    movie=Movie.objects.filter(admin_id=request.user)
    context = {
    "movie": movie
    }
    return render(request,'html/movie_list.html',context)

@login_required(redirect_field_name="log")
def delete(request,id):
    if request.method=="POST":
        Movie.objects.filter(id=id).delete()
        return redirect("/movielist")
def log(request):
  if request.method=='POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username,password=password)

    if user is not None:
        auth.login(request,user)
        messages.success(request,'Now you are logged into movie-poster')
        return redirect('/trending')
    else:
        messages.error(request,'Login failed') 
        return redirect('log')   

  else:      
    return render(request, 'registration/login.html')
def signup(request):
  if request.method=='POST':
   #Get form values
   first_name = request.POST['first_name']
   username = request.POST['username']
   email = request.POST['email']
   password = request.POST['password1']

   if password == password:
     # check username
        if User.objects.filter(username=username).exists():
            messages.error(request,'This  username already taken')
            return redirect('signup')
        else:  
            if User.objects.filter(email=email).exists():
               messages.error(request,'this email already taken')
               return redirect('signup') 
            else:
              user = User.objects.create_user(username=username,password=password,email=email,
              first_name=first_name) 
              user.save()
              messages.success(request,'you are now registerd and login')
              return redirect('log')
   else:
    messages.error(request,'passwords do not match')
    return redirect('signup')   
  else:      
    return render(request,'registration/signup.html')

# def signup(request):
#     if request.method=="POST":
#         first_name=request.POST['first_name']
#         last_name=request.POST['last_name']
#         username=request.POST['username']
#         password=request.POST['password1']
#         password2=request.POST['password2']
#         email=request.POST['email']
#         user=User.objects.create_user(username=username,password=password,last_name=last_name,email=email,first_name=first_name)
#         user.save()
#         print('user created')
#         return redirect("/log")
#     else:
#         return render(request,'registration/signup.html')
@login_required(redirect_field_name="log")   
def logouts(request):
    if request.method=='POST':
      auth.logout(request)
      messages.success(request,'you are logged out')
    return redirect('/log')
                
@login_required(redirect_field_name="log")
def account(request):
    
    return render(request,'html/account.html')    



# def handler404(request):
#     return render(request, "html/no_internet.html")