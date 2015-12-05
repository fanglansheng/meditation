from django.shortcuts import render, get_object_or_404
from django.db import transaction
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, update_session_auth_hash
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from meditation.forms import *
import json


def login_auth(request):
    dic = {}
    if request.method == 'GET':
        return HttpResponse('Request is GET.')
    request_data = json.loads(request.body)
    username = request_data['username']
    password = request_data['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            dic['type'] = 'success'
            dic['content'] = "Success login."
        else:
            dic['type'] = 'error'
            dic['errors'] = "The password is valid, but the account has been disabled!"
    else:
        dic['type'] = 'error'
        dic['errors'] = "The username and password were incorrect."
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')


@transaction.atomic
def register(request):
    context = {}

    if request.method == 'GET':
        return HttpResponse("Request is GET.")

    request_data = json.loads(request.body)

    form = RegistrationForm(request_data)
    context['register_form'] = form
    if not form.is_valid():
        dic = {}
        dic['type'] = 'error'
        dic['errors'] = [form.errors[e] for e in form.errors]
        data = json.dumps(dic)
        return HttpResponse(data, content_type='application/json')

    form.save()
    username = form.cleaned_data['username']
    to_email = form.cleaned_data['email']
    new_user = authenticate(username=username,
                            password=form.cleaned_data['password1'])

    new_user.is_active = False
    new_user.save()

    # set up an empty profile for the new registered user
    new_profile = Profile(user=new_user)
    new_profile.save()

    token = default_token_generator.make_token(new_user)

    email_body = """Welcome to Meditation. Please verify your email address and login to your account through below link.

    http://%s%s""" % (request.get_host(), reverse('confirm_register', args=(username, token)))

    send_mail(subject="Verify your new password by email",
              message=email_body,
              from_email="meditation.noreply@gmail.com",
              recipient_list=[to_email])
    data = json.dumps({"username": username})
    return HttpResponse(data, content_type='application/json')


def register_info(request, username):
    to_email = User.objects.get(username=username).email
    text = "%s, please confirm from the email sent you your address: %s to activate your account" % (username, to_email)
    return render(request, 'meditation/info-panel.html', {'text': text})


@transaction.atomic
def confirm_register(request, username, token):
    context = {}
    user = get_object_or_404(User, username=username)

    if not default_token_generator.check_token(user, token):
        raise Http404

    user.is_active = True
    user.save()

    text = "Thank you for confirming.Your account is now active. Please click back button to login."
    context['text'] = text

    return render(request, 'meditation/info-panel.html', context)


@transaction.atomic
def reset_password_email(request):
    context = {}

    if request.method == 'GET':
        return HttpResponse("Request is GET.")

    request_data = json.loads(request.body)
    form = MyPasswordResetForm(request_data)
    if not form.is_valid():
        dic = {}
        dic['type'] = 'error'
        dic['errors'] = [form.errors[e] for e in form.errors]
        data = json.dumps(dic)
        return HttpResponse(data, content_type='application/json')

    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('new_password1')

    user = get_object_or_404(User, username=username)

    to_email = user.email
    user.password = make_password(password, hasher='sha1')
    password_enc = user.password

    user.is_active = False
    user.save()

    token = default_token_generator.make_token(user)

    email_body = """Welcome to Meditation. Please verify your email address and change the password of your account through below link.

    http://%s%s""" % (request.get_host(), reverse('confirm_reset_password_email', args=(username, password_enc, token)))

    send_mail(subject="Verify your new password by email",
              message=email_body,
              from_email="meditation.noreply@gmail.com",
              recipient_list=[to_email])
    data = json.dumps({"username": username})
    return HttpResponse(data, content_type='application/json')


def reset_password_info(request, username):
    to_email = User.objects.get(username=username).email
    text = "%s, please confirm from the email sent you your address: %s to finish resetting your password" % (
    username, to_email)
    return render(request, 'meditation/info-panel.html', {'text': text})


@transaction.atomic
def confirm_reset_password_email(request, username, password_enc, token):
    context = {}
    user = get_object_or_404(User, username=username)

    if not default_token_generator.check_token(user, token):
        raise Http404

    if user.password != password_enc:
        raise Http404

    user.is_active = True
    user.save()

    text = "Thank you for confirming. Your password is successfully reset. Please click back button to login."
    context['text'] = text

    return render(request, 'meditation/info-panel.html', context)


@login_required
@transaction.atomic
def change_password_inner(request):
    dic = {}
    if request.method == 'GET':
        return HttpResponse('Request is GET.')
    request_body = json.loads(request.body)
    postForm = request.POST.copy()
    postForm['old_password'] = request_body['old_password']
    postForm['new_password1'] = request_body['new_password1']
    postForm['new_password2'] = request_body['new_password2']

    change_password_form = MyPasswordChangeForm(user=request.user, data=postForm)
    if not change_password_form.is_valid():
        dic['type'] = 'error'
        dic['errors'] = [change_password_form.errors[e] for e in change_password_form.errors]
        data = json.dumps(dic)
        return HttpResponse(data, content_type='application/json')
    change_password_form.save()
    # Change the password without logging the user out
    update_session_auth_hash(request, change_password_form.user)
    dic['type'] = 'success'
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')
