from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from account.forms import CustomRegistrationForm


class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("books:book_list")
        return super().dispatch(request, *args, **kwargs)


def register(request):
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data["password2"])
            new_user.save()
            return redirect("login")
    else:
        form = CustomRegistrationForm()
    return render(request, "registration/register.html", {"form": form})
