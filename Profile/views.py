from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.shortcuts import render, redirect


@login_required
def profile_view(request):
    user = request.user
    form = ProfileForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('profile')

    context = {
        'user': user,
        'form': form,
    }
    return render(request, 'profiles/profile.html', context)