from django.shortcuts import render, redirect
from .models import Todo

# tasks/views.py
import yfinance as yf

def index(request):
    try:
        # Fetch stock prices using yfinance
        nifty50_data = yf.download('^NSEI', period='1d')
        banknifty_data = yf.download('^NSEBANK', period='1d')
        finnifty_data = yf.download('NIFTY_FIN_SERVICE.NS', period='1d')

        # Extract the latest closing price if data is available
        nifty50_close = nifty50_data['Close'][-1] if len(nifty50_data) > 0 else None
        banknifty_close = banknifty_data['Close'][-1] if len(banknifty_data) > 0 else None
        finnifty_close = finnifty_data['Close'][-1] if len(finnifty_data) > 0 else None

        # Extract the latest opening price if data is available
        nifty50_open = nifty50_data['Open'][-1] if len(nifty50_data) > 0 else None
        banknifty_open = banknifty_data['Open'][-1] if len(banknifty_data) > 0 else None
        finnifty_open = finnifty_data['Open'][-1] if len(finnifty_data) > 0 else None

        # Calculate the changes in stock prices (open - close)
        nifty50_change = nifty50_open - nifty50_close if nifty50_open and nifty50_close else None
        banknifty_change = banknifty_open - banknifty_close if banknifty_open and banknifty_close else None
        finnifty_change = finnifty_open - finnifty_close if finnifty_open and finnifty_close else None

        # Convert changes to positive values
        nifty50_change = abs(nifty50_change) if nifty50_change is not None else None
        banknifty_change = abs(banknifty_change) if banknifty_change is not None else None
        finnifty_change = abs(finnifty_change) if finnifty_change is not None else None
    except Exception as e:
        # Handle the exception if there is an error fetching the data
        print(f"Error fetching stock prices: {e}")
        nifty50_close = None
        banknifty_close = None
        finnifty_close = None
        nifty50_change = None
        banknifty_change = None
        finnifty_change = None

    todos = Todo.objects.all().order_by('-created_at')
    context = {
        'nifty50_price': nifty50_close,
        'nifty50_change': nifty50_change,
        'banknifty_price': banknifty_close,
        'banknifty_change': banknifty_change,
        'finnifty_price': finnifty_close,
        'finnifty_change': finnifty_change,
        'todos': todos
    }
    return render(request, 'tasks/index.html', context)


def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        Todo.objects.create(title=title)
    return redirect('tasks:index')

def complete_task(request, task_id):
    todo = Todo.objects.get(id=task_id)
    todo.completed = True
    todo.save()
    return redirect('tasks:index')

def delete_task(request, task_id):
    todo = Todo.objects.get(id=task_id)
    todo.delete()
    return redirect('tasks:index')
