from django.shortcuts import render

def viewTU(request):
    elementosDeLista = [
    "TU1","TU2","TU3",
    ]
    context = {'elementos_de_lista': elementosDeLista}
    return render(request, 'reqApp/lista_expandible.html', context)

def viewRU(request):
    elementosDeLista = [
    "RU1","RU2","RU3",
    ]
    context = {'elementos_de_lista': elementosDeLista}
    return render(request, 'reqApp/lista_expandible.html', context)

def viewRS(request):
    elementosDeLista = [
    "RS1","RS2","RS3",
    ]
    context = {'elementos_de_lista': elementosDeLista}
    return render(request, 'reqApp/lista_expandible.html', context)

def viewMD(request):
    elementosDeLista = [
    "MD1","MD2","MD3",
    ]
    context = {'elementos_de_lista': elementosDeLista}
    return render(request, 'reqApp/lista_expandible.html', context)

def viewCP(request):
    elementosDeLista = [
    "CP1","CP2","CP3",
    ]
    context = {'elementos_de_lista': elementosDeLista}
    return render(request, 'reqApp/lista_expandible.html', context)
