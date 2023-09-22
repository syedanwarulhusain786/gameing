from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import pandas as pd

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import pandas as pd
from difflib import SequenceMatcher

import pandas as pd
from utils.script import play_game,get_player_photo_url
from .models import GameData
from django.contrib import messages
combined_data_filtered = pd.read_csv(r'utils\ff.csv',encoding='ISO-8859-1')








def get_player_data(request):
    if request.method == 'POST' :
        selected_level = request.POST.get('level')
        
        # Process the POST data and retrieve the player data
        player_stats, player_name, player_id = play_game(combined_data_filtered, selected_level)
        # print(player_stats.to_string(index=False))
        player_data=player_stats.to_json(orient='records')
        request.session['player_name'] = player_name
        request.session['player_id'] = player_id
        print(player_id,player_name)
        # player_data=[]
        return JsonResponse(player_data, safe=False)
@login_required(login_url='login') 
def start_game(request):
        # Define a variable to keep track of the player's score

    # Define a variable to keep track of the player's score for close guesses
    close_guess_score = 0.5
    context={}
    # Example usage of function
    play_again = True
    score = 0
    context['win']=False
    
    # Initialize score to 0
    if request.method == 'POST':
        
        # Retrieve player_name from session
        url=""
        message=''
        
        player_name = request.session.get('player_name')
        player_id = request.session.get('player_id')
        guess = request.POST.get('guess')
        score = float(request.POST.get('currentScore').strip())
        
        name_similarity = SequenceMatcher(None, guess.lower(), player_name.lower()).ratio()
        if guess.lower() == player_name.lower():
            player_photo_url = get_player_photo_url(player_id)
            message="Congratulations! You got it right." 
            url=player_photo_url
            context['win']=True
            # Increment score by 1 and display current score
            score += 1
        elif name_similarity >= 0.8:
            player_photo_url = get_player_photo_url(player_id)
            message=f"Close enough! The player was {player_name}."
            # Increment score by close_guess_score and display current score
            context['win']=True
            score += close_guess_score
        else:
            message=f"Sorry, that's incorrect. The correct answer was {player_name}."
            player_photo_url = get_player_photo_url(player_id)
            context['win']=True
            # display current score
        context['player_photo_url']=player_photo_url
        context['message']=message
        context['player_name']=player_name
        context['score']=score
        context['player_id']=player_id
        user = request.user
        # Now you can use the 'user' object in your view
        typeEmailX = user.username
        new_user = GameData.objects.get(username=typeEmailX)
        if new_user.lastgame<score:
            new_user.lastgame=score
        new_user.current_score=score
        
        new_user.save()
        
        
        
    return JsonResponse(context, safe=False)
@login_required(login_url='login') 
def reset_game(request):
    user = request.user
        # Now you can use the 'user' object in your view
    typeEmailX = user.username
    # Initialize score to 0
    if request.method == 'POST':
        new_user = GameData.objects.get(username=typeEmailX)
        new_user.current_score=0
        
        new_user.save()
    context={
        'resp':True
    }
    return JsonResponse(context, safe=False)
@login_required(login_url='login') 
def home(request):
    user = request.user
        # Now you can use the 'user' object in your view
    typeEmailX = user.username
    
    user_ip_exists = GameData.objects.get(username=typeEmailX)
    if not user_ip_exists:
        current_score=0
        lastgame=0
        username=None
        
    else:
        filtered_users = user_ip_exists
        current_score=filtered_users.current_score
        lastgame=filtered_users.lastgame
        username=filtered_users.username

    top_users = GameData.objects.order_by('-lastgame')[:10]
    
    context={
        'current_score':current_score,
        'lastgame':lastgame,
        'username':username,
        'top_users': top_users
    }
    print(context)
    return render(request, 'home.html',context=context)



def custom_login(request):
    if request.method == 'POST':
        username = request.POST['typeEmailX']
        password = request.POST['typePasswordX']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the dashboard page after login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def custom_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout