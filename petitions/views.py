from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect, reverse
from petitions.models import Petition
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
import e_petitions.settings as settings


def petition(request, pid):

    o_petition = get_object_or_404(Petition, id=pid)
    bl_user_signed = request.user.is_authenticated and o_petition.user_signed(request.user)
    l_signatures = o_petition.get_signatures()

    data = {
        'petition': o_petition,
        'user_signed': bl_user_signed,
        'signatures': l_signatures,
    }

    return render(request, 'petition.html', data)


def index(request):

    s_petitions_filter = request.GET.get('filter', 'active').strip().upper()

    if s_petitions_filter not in ('ACTIVE', 'ON_CONSIDERATION', 'ANSWERED', 'REJECTED'):
        s_petitions_filter = 'ACTIVE'

    l_petitions = Petition.objects.filter(status=s_petitions_filter)

    data = {
        'petitions': l_petitions,
        'petitions_signs': settings.PETITION_SIGNATURES,
    }

    return render(request, 'index.html', data)


@login_required()
def sign_petition(request, pid):

    o_petition = get_object_or_404(Petition, id=pid)

    if request.user.is_authenticated \
            and o_petition.is_active \
            and not o_petition.user_signed(request.user) \
            and request.method == 'POST':
        o_petition.sign(request.user)

    return redirect(o_petition)


@login_required()
def create_petition(request):

    if request.method == 'GET':

        return render(request, 'create_petition.html')

    else:

        title = request.POST.get('title')[:150]
        text = request.POST.get('text')[:10000]

        if title and text:
            p = Petition.objects.create(title=title, text=text, author=request.user)
            p.save()
            p.sign(request.user)

            return redirect(p)

        else:

            messages.error(request, 'Помилка при створенні петиції. Перевірте чи вказана назва і основний текст.')
            return render(request, 'create_petition.html')


def review_petition(request, pid):

    if not request.user.is_authenticated or not request.user.profile.is_admin:
        return HttpResponseForbidden('У Вас немає прав на відвідування цієї сторінки.')

    o_petition = get_object_or_404(Petition, id=pid)

    data = {
        'petition': o_petition,
    }

    if request.method == 'GET':

        return render(request, 'review_petition.html', data)

    if request.method == 'POST':

        o_petition.answer = request.POST.get('answer', '')[:10000]
        o_petition.responder = request.user
        o_petition.response_date = datetime.datetime.now()
        o_petition.status = o_petition.ANSWERED
        o_petition.save()

        return redirect(o_petition)
