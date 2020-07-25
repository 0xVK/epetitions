from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
import json
import requests
import e_petitions.settings as settings
from django.contrib import messages
from core.models import *


@csrf_exempt
def fb_login(request):

    fb_response = json.loads(request.POST.get('ajaxData'))
    token = json.loads(request.POST.get('token'))

    username = fb_response.get('email') or fb_response.get('id')
    password = username
    email = fb_response.get('email')
    first_name = fb_response.get('first_name')
    last_name = fb_response.get('last_name')
    fb_link = fb_response.get('link')
    gender = fb_response.get('gender')

    response = requests.get('https://graph.facebook.com/debug_token', {
        'input_token': token,
        'access_token': settings.FACEBOOK_ACCESS_TOKEN,
    }).json()

    data = dict()

    is_token_valid = response.get('data', {}).get('is_valid', False)

    if not is_token_valid:
        data['status'] = 'Помилка при авторизації. Якщо помилка повторюється - зверніться до адміністратора.'
        data['code'] = 102
        return JsonResponse(data)

    if User.objects.filter(username=username).exists():

        user = authenticate(username=username, password=password)
        login(request, user)
        data['code'] = 100
        data['status'] = 'Авторизовано'

    else:

        u = User.objects.create_user(username=username, first_name=first_name,
                                     last_name=last_name, email=email, password=password)

        u.profile.gender = 'M'
        u.profile.fb_link = fb_link
        u.profile.save()

        user = authenticate(username=username, password=password)
        login(request, user)

        data['code'] = 101
        data['status'] = 'Зареєстровано'

    return JsonResponse(data)


def login_page(request):

    return render(request, 'login.html')


def my_petitions(request):

    l_petitions = request.user.profile.get_user_petitions()
    l_signed_petitions = request.user.profile.get_user_signed_petitions()
    l_petitions_to_review = request.user.profile.get_petitions_to_rewiew()

    data = {
        'petitions_signs': settings.PETITION_SIGNATURES,
        'petitions': l_petitions,
        'my_petitions_count': len(l_petitions),
        'petitions_signed_by_me_count': len(l_signed_petitions),
        'petitions_to_review_count': len(l_petitions_to_review),
    }

    return render(request, 'my-petitions.html', data)


def my_signed_petitions(request):

    l_petitions = request.user.profile.get_user_petitions()
    l_signed_petitions = request.user.profile.get_user_signed_petitions()
    l_petitions_to_review = request.user.profile.get_petitions_to_rewiew()

    data = {
        'petitions_signs': settings.PETITION_SIGNATURES,
        'petitions': l_signed_petitions,
        'my_petitions_count': len(l_petitions),
        'petitions_signed_by_me_count': len(l_signed_petitions),
        'petitions_to_review_count': len(l_petitions_to_review),
    }

    return render(request, 'my-signed-petitions.html', data)


def petitions_to_review(request):

    petitions = request.user.profile.get_user_petitions()
    signed_petitions = request.user.profile.get_user_signed_petitions()
    l_petitions_to_review = request.user.profile.get_petitions_to_rewiew()

    data = {
        'petitions_signs': settings.PETITION_SIGNATURES,
        'petitions': l_petitions_to_review,
        'my_petitions_count': len(petitions),
        'petitions_signed_by_me_count': len(signed_petitions),
        'petitions_to_review_count': len(l_petitions_to_review),
    }

    return render(request, 'petitions-to-review.html', data)


def bug_ticket(request):

    if request.method == 'GET':

        return render(request, 'ticket.html')

    if request.method == 'POST':

        name = request.POST.get('name')[:50]
        email = request.POST.get('email')[:50]
        text = request.POST.get('text')[:5000]

        Ticket(name=name, email=email, text=text).save()

        messages.success(request, 'Ваше повідомлення успішно відправлено!')

        return render(request, 'ticket.html')
