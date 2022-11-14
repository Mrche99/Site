from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm, ProfileImageForm,UserUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f'Пользователь {username} был успешно создан')
            return redirect('homepage')
    else:
        form = UserForm()
    return render(request,
                  'users/registration.html',
                  {
                      'title': 'Страница регистрации',
                      'form': form
                  }
                  )
@login_required
def profile(request):
    if request.method == "POST":
        profileform = ProfileImageForm(request.POST, request.FILES , instance=request.user.profile)
        updateuser = UserUpdateForm(request.POST, instance=request.user)
        if profileform.is_valid() and updateuser.is_valid():
            updateuser.save()
            profileform.save()
            messages.success(request, f'Ваш аккаунт был успешно обновлён')
            return redirect('profile')
    else:
        profileform = ProfileImageForm(instance=request.user.profile)
        updateuser = UserUpdateForm(instance=request.user)

    data = {'profileform': profileform,
            'updateuser': updateuser,
            }
    return render(request,'users/profile.html', data)
