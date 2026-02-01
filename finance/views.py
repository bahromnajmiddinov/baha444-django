from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Account, Transaction, Budget, Category

@login_required
def finance_dashboard(request):
    accounts = Account.objects.filter(user=request.user, is_active=True)
    total_balance = accounts.aggregate(total=Sum('balance'))['total'] or 0
    
    this_month = datetime.now().replace(day=1).date()
    
    income = Transaction.objects.filter(
        user=request.user,
        category__category_type='income',
        date__gte=this_month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    expenses = Transaction.objects.filter(
        user=request.user,
        category__category_type='expense',
        date__gte=this_month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    recent_transactions = Transaction.objects.filter(user=request.user)[:10]
    budgets = Budget.objects.filter(user=request.user, month__gte=this_month)
    
    context = {
        'accounts': accounts,
        'total_balance': total_balance,
        'income': income,
        'expenses': expenses,
        'balance': income - expenses,
        'recent_transactions': recent_transactions,
        'budgets': budgets,
    }
    
    return render(request, 'finance/dashboard.html', context)
