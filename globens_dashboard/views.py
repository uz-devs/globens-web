from django.contrib.auth import authenticate as dj_authenticate
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as dj_logout
from django.contrib.auth import login as dj_login
from django.shortcuts import render, redirect
from . import db_helper as db


@require_http_methods(['GET', 'POST'])
def handle_login_api(request):
    if request.method == 'GET':
        return render(
            request=request,
            template_name='login_page.html',
            context={'title': 'Authenticate'}
        )
    elif request.method == 'POST':
        user = dj_authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            dj_login(request, user)
            return redirect(to='main-page')
        else:
            return redirect(to='login-page')
    else:
        return redirect(to='login-page')


@login_required
@require_http_methods(['GET', 'POST'])
def handle_logout_api(request):
    dj_logout(request=request)
    return redirect(to='login-page')


@login_required
@require_http_methods(['GET'])
def handle_main_page(request):
    return render(
        request=request,
        template_name='main_page.html',
        context={'title': 'Globens dashboard'}
    )
