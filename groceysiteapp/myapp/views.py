from django.shortcuts import render,redirect
# Create your views here.
from .models import Fbought, Fconsumed,Ffreezer
from django.db.models import Sum
from django.utils import timezone
# def index(request):

#     return render(request,"myapp/index.html",{})


def index(request):
    bought = Fbought.objects.all()
    consumed = Fconsumed.objects.all()
    freezed = Ffreezer.objects.all()

    for item in bought:
        # Initialize the expiry date to None
        expiry_date = None
        
        # Check if the item is frozen
        if item.freeze:
            # Get the frozen food life from the Ffreezer table
            freezer_item = Ffreezer.objects.filter(fbought=item).first()
            if freezer_item and freezer_item.ffreeze:
                food_life = int(freezer_item.ffreeze)  # Convert to integer
                expiry_date = item.date + timedelta(days=food_life)
        else:
            # Get the non-frozen food life from the Ffreezer table
            freezer_item = Ffreezer.objects.filter(fbought=item).first()
            if freezer_item and freezer_item.fnfreeze:
                food_life = int(freezer_item.fnfreeze)  # Convert to integer
                expiry_date = item.date + timedelta(days=food_life)

        # Set the calculated expiry date to the item
        item.expiry_date = expiry_date

    return render(request, "myapp/index.html",{'bought_data': bought, 'consumed_data': consumed,"freezer_data":freezed})

def navbar(request):
    return render(request,"myapp/navbar.html")


def fb(request):
    return render(request,"myapp/fb.html")


def fc(request):
    return render(request,"myapp/fc.html")


def ff(request):
    return render(request,"myapp/ff.html")


# def insert_fbought(request):
#     fbought = request.POST['fbought']
#     fbamount = request.POST['fbamount']
#     date=request.POST['date']
#     fb_ = Fbought( fbought= fbought,fbamount=fbamount,date=date)
#     fb_.save()
#     return render(request,'myapp/fb.html',{})


def insert_fbought(request):
    if request.method == "POST":
        fbought = request.POST.get('fbought', '')
        fbamount = request.POST.get('fbamount', '')
        date = request.POST.get('date', '')
        # Handle the checkbox for freeze
        freeze = request.POST.get('ffreeze') == 'on'  # Checkbox is sent as 'on' if checked, otherwise not sent



        print(freeze,'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        
        fb_ = Fbought(fbought=fbought, fbamount=fbamount, date=date, freeze=freeze)
        fb_.save()
        return redirect('fb')  # Redirect to the fb page or another page after saving
    return render(request, 'myapp/fb.html', {})




def viewtables(request):
    bought = Fbought.objects.all()
    consumed = Fconsumed.objects.all()
    freezed = Ffreezer.objects.all()
    return render(request, "myapp/viewdetails.html", {'bought_data': bought, 'consumed_data': consumed,"freezer_data":freezed})









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


def deletefreezeritem(request,id):
    fz=Ffreezer.objects.get(id=id)
    fz.delete()
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

def editfreezeritem(request,id):
    fz_item=Ffreezer.objects.get(id=id)
    return render(request,"myapp/editfreeze.html",{'fz_item':fz_item
    })




def updatefbitem(request,id):
    # new_fid=request.POST['nid']
    new_fbought=request.POST['nfbought']
    new_ffreeze = request.POST.get('nffreeze') == 'on'
    # new_ffreeze=request.POST['nffreeze']
    new_famount=request.POST['nfamount']
    new_date=request.POST['ndate']
    fb=Fbought.objects.get(id=id)
    fb.fbought = new_fbought
    fb.freeze = new_ffreeze
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



def updatefreezeritem(request, id):
    if request.method == "POST":
        try:
            # Fetch the existing Ffreezer instance by its ID
            fz = Ffreezer.objects.get(id=id)

            # Update the fields with new values from the form
            fbought_name = request.POST.get('ffbought')
            fbought_instance = Fbought.objects.get(fbought=fbought_name)

            new_fz = request.POST.get('flfreeze')
            new_nfz = request.POST.get('flnfreeze')

            fz.fbought = fbought_instance
            fz.ffreeze = new_fz
            fz.fnfreeze = new_nfz
            fz.save()

            return redirect("/viewtables")
        except Ffreezer.DoesNotExist:
            # Handle the case where the Ffreezer instance does not exist
            return redirect("/viewtables")
    else:
        return redirect("/viewtables")












   
    new_fb = request.POST['ffbought']
    new_fz=request.POST['flfreeze']
    new_nfz=request.POST['flnfreeze']
    fz=Ffreezer.objects.get(id=id)
    fz.fbought = new_fb
    fz.ffreeze = new_fz
    fz.fnfreeze = new_nfz
    fz.save()
    return redirect("/viewtables")









# def insert_ffreeze(request):
#     fbought = request.POST['fbought']
#     flfreeze = request.POST['flfreeze']
#     flnfreeze = request.POST['flnfreeze']
#     ff= Ffreezer( fbought=fbought, ffreeze= flfreeze,fnfreeze=flnfreeze)
#     ff.save()
#     return render(request,'myapp/ff.html',{})



def insert_ffreeze(request):
    if request.method == "POST":
        fbought_name = request.POST.get('fbought')
        flfreeze = request.POST.get('flfreeze')
        flnfreeze = request.POST.get('flnfreeze')

        try:
            # Retrieve the Fbought instance based on the name
            fbought_instance = Fbought.objects.get(fbought=fbought_name)
            
            # Create the Ffreezer instance with the Fbought instance
            ff = Ffreezer(fbought=fbought_instance, ffreeze=flfreeze, fnfreeze=flnfreeze)
            ff.save()

            return redirect('ff')  # Redirect to the ff page or another page after saving
        except Fbought.DoesNotExist:
            # Handle the case where the specified Fbought instance does not exist
            return render(request, 'myapp/ff.html', {'error': 'The specified food item does not exist.'})
    
    return render(request, 'myapp/ff.html', {})











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



from django.utils.dateparse import parse_datetime
from datetime import timedelta


def viewtables_exp(request):
    bought = Fbought.objects.all()
    consumed = Fconsumed.objects.all()
    freezed = Ffreezer.objects.all()

    for item in bought:
        # Initialize the expiry date to None
        expiry_date = None
        
        # Check if the item is frozen
        if item.freeze:
            # Get the frozen food life from the Ffreezer table
            freezer_item = Ffreezer.objects.filter(fbought=item).first()
            if freezer_item and freezer_item.ffreeze:
                food_life = int(freezer_item.ffreeze)  # Convert to integer
                expiry_date = item.date + timedelta(days=food_life)
        else:
            # Get the non-frozen food life from the Ffreezer table
            freezer_item = Ffreezer.objects.filter(fbought=item).first()
            if freezer_item and freezer_item.fnfreeze:
                food_life = int(freezer_item.fnfreeze)  # Convert to integer
                expiry_date = item.date + timedelta(days=food_life)

        # Set the calculated expiry date to the item
        item.expiry_date = expiry_date

    return render(request, "myapp/index.html",{'bought_data': bought, 'consumed_data': consumed,"freezer_data":freezed})



# def viewtables(request):
#     bought = Fbought.objects.all()
#     consumed = Fconsumed.objects.all()
#     freezed = Ffreezer.objects.all()

#     for item in bought:
#         # Initialize the expiry date to None
#         expiry_date = None
        
#         # Check if the item is frozen
#         if item.freeze:
#             # Get the frozen food life from the Ffreezer table
#             freezer_item = Ffreezer.objects.filter(fbought=item).first()
#             if freezer_item and freezer_item.ffreeze:
#                 food_life = int(freezer_item.ffreeze)  # Convert to integer
#                 expiry_date = item.date + timedelta(days=food_life)
#         else:
#             # Get the non-frozen food life from the Ffreezer table
#             freezer_item = Ffreezer.objects.filter(fbought=item).first()
#             if freezer_item and freezer_item.fnfreeze:
#                 food_life = int(freezer_item.fnfreeze)  # Convert to integer
#                 expiry_date = item.date + timedelta(days=food_life)

#         # Set the calculated expiry date to the item
#         item.expiry_date = expiry_date

#     return render(request,"myapp/index.html" ,{'bought_data': bought, 'consumed_data': consumed,"freezer_data":freezed})




# def viewtables(request):
#     bought = Fbought.objects.all()
#     consumed = Fconsumed.objects.all()
#     freezed = Ffreezer.objects.all()
#     return render(request, "myapp/viewdetails.html", {'bought_data': bought, 'consumed_data': consumed,"freezer_data":freezed})