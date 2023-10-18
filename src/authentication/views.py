from django.shortcuts import render, redirect

from authentication.forms import CustomUserCreationForm


# Create your views here.
def user_registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', locals())
