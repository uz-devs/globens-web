from django.contrib.auth import authenticate as dj_authenticate
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as dj_logout
from django.contrib.auth import login as dj_login
from django.shortcuts import render, redirect
from . import db_helper as db


def handle_privacy_policy(request):
    return render(request=request, template_name='pp.html')


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
            return redirect(to='login')
    else:
        return redirect(to='login')


@login_required
@require_http_methods(['GET', 'POST'])
def handle_logout_api(request):
    dj_logout(request=request)
    return redirect(to='login')


@login_required
@require_http_methods(['GET'])
def handle_main_page(request):
    if len(request.user.username) > 2:
        country_code = request.user.username[-3:]
        publish_requests = []
        for gb_request in db.get_product_publish_requests(country_code=country_code):
            gb_product = db.get_product(product_id=gb_request['product_id'])
            gb_business_page = db.get_business_page(business_page_id=gb_request['business_page_id'])
            gb_requester_user = db.get_user(user_id=gb_request['requester_user_id'])
            publish_requests += [{
                'time': gb_request['timestamp'].strftime('%m/%d (%a), %I:%M %p'),
                'product_id': gb_product['id'],
                'product_name': gb_product['name'],
                'business_page_name': gb_business_page['title'],
                'requester_user_email': gb_requester_user['email']
            }]
        return render(
            request=request,
            template_name='main_page.html',
            context={
                'title': 'Globens dashboard',
                'publish_requests': publish_requests
            }
        )
    else:
        return redirect(to='logout')


@login_required
@require_http_methods(['GET'])
def handle_contents_page(request):
    # todo implement (google drive url view)
    return redirect(to='main-page')


@login_required
@require_http_methods(['GET'])
def handle_product_approve(request):
    if 'product_id' in request.GET and str(request.GET['product_id']).isnumeric():
        gb_product = db.get_product(product_id=int(request.GET['product_id']))
        db.publish_product(gb_product=gb_product)
        db.remove_product_publish_request(gb_product=gb_product)
    return redirect(to='main-page')


@login_required
@require_http_methods(['GET'])
def handle_product_disapprove(request):
    if 'product_id' in request.GET and str(request.GET['product_id']).isnumeric():
        gb_product = db.get_product(product_id=int(request.GET['product_id']))
        db.remove_product_publish_request(gb_product=gb_product)
    return redirect(to='main-page')
