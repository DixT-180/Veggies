from django.shortcuts import render,redirect
# Create your views here.
from .models import Fbought, Fconsumed
from django.db.models import Sum
from django.utils import timezone
def index(request):

    return render(request,"myapp/index.html",{})


def navbar(request):
    return render(request,"myapp/navbar.html")


def fb(request):
    return render(request,"myapp/fb.html")


def fc(request):
    return render(request,"myapp/fc.html")


def insert_fbought(request):
    fbought = request.POST['fbought']
    fbamount = request.POST['fbamount']
    date=request.POST['date']
    fb_ = Fbought( fbought= fbought,fbamount=fbamount,date=date)
    fb_.save()
    return render(request,'myapp/fb.html',{})

def viewtables(request):
    bought = Fbought.objects.all()
    consumed = Fconsumed.objects.all()
    return render(request, "myapp/viewdetails.html", {'bought_data': bought, 'consumed_data': consumed})









def insert_fconsumed(request):
    fconsumed = request.POST['fconsumed']
    fcamount = request.POST['fcamount']
    date=request.POST['date']
    fc_ = Fconsumed( fconsumed=fconsumed,fcamount=fcamount,date=date)
    fc_.save()
    return render(request,'myapp/fc.html',{})




def deletefbitem(request,id):
    fb=Fbought.objects.get(id=id)
    fb.delete()
    # return render(request,'myapp/viewdetails.html',{})
    return redirect("/viewtables")
    
def deletefcitem(request,id):
    fc=Fconsumed.objects.get(id=id)
    fc.delete()
    # return render(request,'myapp/viewdetails.html',{})
    return redirect("/viewtables")

def editfbitem(request,id):
    fb_item=Fbought.objects.get(id=id)
    return render(request,"myapp/edititem.html",{'fb_item':fb_item
    })

def editfcitem(request,id):
    fc_item=Fconsumed.objects.get(id=id)
    return render(request,"myapp/editfcitem.html",{'fc_item':fc_item
    })


def updatefbitem(request,id):
    # new_fid=request.POST['nid']
    new_fbought=request.POST['nfbought']
    new_famount=request.POST['nfamount']
    new_date=request.POST['ndate']
    fb=Fbought.objects.get(id=id)
    fb.fbought = new_fbought
    fb.fbamount = new_famount
    fb.date = new_date
    fb.save()
    return redirect("/viewtables")

def updatefcitem(request,id):
    # new_fid=request.POST['nid']
    new_fc=request.POST['nfconsumed']
    new_famount=request.POST['nfcamount']
    new_date=request.POST['ndate']
    fc=Fconsumed.objects.get(id=id)
    fc.fconsumed = new_fc
    fc.fcamount = new_famount
    fc.date = new_date
    fc.save()
    return redirect("/viewtables")

def remaining_food(request):
    current_date = timezone.now().date()  # Automatically get the current date

    # Get all distinct food items that have been bought
    food_items = Fbought.objects.values_list('fbought', flat=True).distinct()
    
    remaining_foods = []

    for food_item in food_items:
        # Calculate the total bought amount of the food item until the current date
        total_bought = Fbought.objects.filter(fbought=food_item, date__lte=current_date).aggregate(total=Sum('fbamount'))['total'] or 0

        # Calculate the total consumed amount of the food item until the current date
        total_consumed = Fconsumed.objects.filter(fconsumed=food_item, date__lte=current_date).aggregate(total=Sum('fcamount'))['total'] or 0

        # Calculate the remaining amount
        remaining = total_bought - total_consumed

        remaining_foods.append({
            'food_item': food_item,
            'remaining': remaining
        })

    return render(request, 'myapp/index.html', {
        'remaining_foods': remaining_foods,
        'date': current_date
    })