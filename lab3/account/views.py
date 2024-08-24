from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from .models import *
from .forms import *


def account_list(request):
    context = {}
    accounts = Account.list_account()
    context["accounts"] = accounts
    return render(request, "account/list.html", context)




def account_create(request):
    context = {}
    form = CreateAccount()
    context["form"] = form
    if request.method == "POST":
        form = CreateAccount(request.POST, request.FILES)
        if form.is_valid():
            accountobj = Account.create_account(
                form.cleaned_data["username"],
                form.cleaned_data["email"],
                form.cleaned_data["password"],
                form.cleaned_data["image"],
            )
            return redirect(accountobj)
        else:
            context["error"] = form.errors
    return render(request, "account/create.html", context)




def account_update(request, id):
    context = {}
    try:
        accountobj = Account.objects.get(id=id)
        form = UpdateAccount(
            initial={
                "username": accountobj.username,
                "email": accountobj.email,
                "password": accountobj.password,
                "image": accountobj.image,
            }
        )

        if request.method == "POST":
            form = UpdateAccount(request.POST, request.FILES)
            if form.is_valid():
                username = form.cleaned_data["username"]
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                image = form.cleaned_data["image"]

                if not password:
                    password = accountobj.password

                if not image:
                    image = accountobj.image

                account_url = Account.update_account(
                    id, username, email, password, image
                )
                return redirect(account_url)
            else:
                context["error"] = form.errors

        context["form"] = form
        context["account"] = accountobj

    except Account.DoesNotExist:
        return HttpResponse("Track not found", status=404)

    return render(request, "account/update.html", context)




def account_delete(request, id):
    try:
        if request.method == "POST":
            Account.delete_account(id)
            return JsonResponse({"success": True})
    except Account.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Account not found"}, status=404
        )




def account_details(request, id):
    context = {}
    try:
        accountobj = Account.details_account(id)
        context["account"] = accountobj
    except Account.DoesNotExist:
        return HttpResponse("Account not found", status=404)
    return render(request, "account/details.html", context)
