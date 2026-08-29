from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Expense
from .forms import ExpenseForm

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Expense
from .forms import ExpenseForm, RegisterForm

# Create your views here.
# LOGIN
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('expense_list')

        return render(request, 'expenses/login.html', {
            'error': 'Invalid username or password.'
        })

    return render(request, 'expenses/login.html')

# LOGOUT
@login_required
def logout_view(request):

    logout(request)

    return redirect('login')


# VIEW EXPENSES
@login_required
def expense_list(request):

    expenses = Expense.objects.filter(
        user=request.user
    ).order_by('-date')

    return render(request, 'expenses/expense_list.html', {
        'expenses': expenses
    })


# CREATE EXPENSE
@login_required
def add_expense(request):

    if request.method == 'POST':

        form = ExpenseForm(request.POST)

        if form.is_valid():

            expense = form.save(commit=False)

            expense.user = request.user

            expense.save()

            return redirect('expense_list')

    else:
        form = ExpenseForm()

    return render(request, 'expenses/add_expense.html', {
        'form': form
    })

# registration
def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.set_password(
                form.cleaned_data['password']
            )

            user.save()

            login(request, user)

            return redirect('expense_list')

    else:
        form = RegisterForm()

    return render(request, 'expenses/register.html', {
        'form': form
    })