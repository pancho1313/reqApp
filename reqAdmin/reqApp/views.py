from django.shortcuts import render

def test(request):
    context = {'latest_poll_list': ''}
    return render(request, 'reqApp/lista.html', context)
"""    
def test(request):
    context = {'latest_poll_list': ''}
    return render(request, 'reqApp/base.html', context)

def test(request):
    context = {'latest_poll_list': ''}
    return render(request, 'reqApp/base.html', context)

def test(request):
    context = {'latest_poll_list': ''}
    return render(request, 'reqApp/base.html', context)

def test(request):
    context = {'latest_poll_list': ''}
    return render(request, 'reqApp/base.html', context)
"""
