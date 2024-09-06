from django.shortcuts import render,redirect
# Create your views here.
from .models import Fbought, Fconsumed,Ffreezer,Food
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.db.models import Max
from django.db.models import Q
# def index(request):

#     return render(request,"myapp/index.html",{})

#done
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
            freezer_item = Ffreezer.objects.filter(ffbought=item).first()
            if freezer_item and freezer_item.ffreeze:
                food_life = int(freezer_item.ffreeze)  # Convert to integer
                expiry_date = item.date + timedelta(days=food_life)
        else:
            # Get the non-frozen food life from the Ffreezer table
            freezer_item = Ffreezer.objects.filter(ffbought=item).first()
            if freezer_item and freezer_item.fnfreeze:
                food_life = int(freezer_item.fnfreeze)  # Convert to integer
                expiry_date = item.date + timedelta(days=food_life)

        # Set the calculated expiry date to the item
        item.expiry = expiry_date
        item.save()

        #for remaining food part 
    current_date = timezone.now().date()  # Automatically get the current date

    # Get all distinct food items that have been bought
    food_items = Fbought.objects.values_list('fbought', flat=True).distinct()
    
    remaining_foods = []

    for food_item in food_items:
        # print(food_item, "xxxxx------------------>")
        
        # Calculate the total bought amount of the food item until the current date
        total_bought_frozen = Fbought.objects.filter(fbought=food_item,freeze=True, date__lte=current_date).aggregate(total=Sum('fbamount'))['total'] or 0

        total_bought_non_frozen = Fbought.objects.filter(fbought=food_item,freeze=False, date__lte=current_date).aggregate(total=Sum('fbamount'))['total'] or 0

        # Calculate the total consumed amount of the food item until the current date
        total_consumed_frozen = Fconsumed.objects.filter(fconsumed=food_item,food_freeze=True, date__lte=current_date).aggregate(total=Sum('fcamount'))['total'] or 0

        total_consumed_non_frozen = Fconsumed.objects.filter(fconsumed=food_item,food_freeze=False, date__lte=current_date).aggregate(total=Sum('fcamount'))['total'] or 0

        remaining_frozen =  total_bought_frozen - total_consumed_frozen

        remaining_non_frozen = total_bought_non_frozen - total_consumed_non_frozen
        remaining_foods.append({
            'food_item': food_item,
            'remaining_frozen': remaining_frozen,
            'remaining_non_frozen':remaining_non_frozen
        })

        # Initialize an empty dictionary to hold the summed values
    summed_data = {}

    for item in remaining_foods:
        food_item = item['food_item'].strip()
    
        if food_item in summed_data:
        # Add the current item's values to the accumulated totals
            summed_data[food_item]['remaining_frozen'] += item['remaining_frozen']
            summed_data[food_item]['remaining_non_frozen'] += item['remaining_non_frozen']
        else:
        # If it's the first time we've seen this food item, add it to the dictionary
            summed_data[food_item] = {
            'food_item': food_item,
            'remaining_frozen': item['remaining_frozen'],
            'remaining_non_frozen': item['remaining_non_frozen']
        }

# Convert the dictionary back into a list
    result = list(summed_data.values())
    # print(result,"result----->")
    distinct_fboughts = Fbought.objects.values('fbought').annotate(fcategory=Max('fcategory'))
    for item in distinct_fboughts:
            
        # Check if the food already exists
            food_obj, created = Food.objects.update_or_create(
            food_name=item['fbought'],
            defaults={'food_category': item['fcategory']})
    Food.objects.filter(Q(food_category='') | Q(food_category__isnull=True)).update(food_category='unknown')

    return render(request, 'myapp/index.html', {
        'remaining_foods': result,
        'date': current_date,'bought_data': bought,"freezer_data":freezed
    

    })
         
        

def navbar(request):
    return render(request,"myapp/navbar.html")


def fb(request):
    categories = Food.objects.values('food_category').distinct()
    

    




    # print(categories,'cats fb')
    return render(request, 'myapp/fb.html', {'categories': categories})
   


def fc(request):
    return render(request,"myapp/fc.html")


def ff(request):
    return render(request,"myapp/ff.html")



def calcount(request):
    veg_categories = Food.objects.filter(food_category='vegetable').values('food_name').distinct()
    fruit_categories = Food.objects.filter(food_category='fruit').values('food_name').distinct()
    carb_categories = Food.objects.filter(food_category='carbs').values('food_name').distinct()
    protein_categories = Food.objects.filter(food_category='protein').values('food_name').distinct()
  
    return render(request, 'myapp/caloriecal.html', {'veg_categories': veg_categories,'fruit_categories':fruit_categories,'carb_categories':carb_categories,'protein_categories':protein_categories})

# categories

def insert_fbought(request):
    if request.method == "POST":
        fbought = request.POST.get('fbought', '')
        fbamount = request.POST.get('fbamount', '')
        date = request.POST.get('date', '')
        fcat = request.POST.get('fcategory','')

        print(fbought,date,fcat,'fffccccaaaaatttttt')
        # Handle the checkbox for freeze
        freeze = request.POST.get('ffreeze') == 'on'
        fb_ = Fbought(fbought=fbought, fbamount=fbamount, date=date, freeze=freeze,fcategory=fcat)
        fb_.save()

        # distinct_fboughts = Fbought.objects.values('fbought').annotate(fcategory=Max('fcategory'))
        # for item in distinct_fboughts:
        # # Check if the food already exists
        #     food_obj, created = Food.objects.update_or_create(
        #     food_name=item['fbought'],
        #     defaults={'food_category': item['fcategory']})
        # Food.objects.filter(Q(food_category='') | Q(food_category__isnull=True)).update(food_category='unknown')



        return redirect('fb')  # Redirect to the fb page or another page after saving
    return render(request, 'myapp/fb.html', {})

def foodcat(request):
    return render(request,"myapp/foodcat.html")



def insert_food_cat(request):
    if request.method == "POST":
        food_name = request.POST.get('food_name', '')
        food_cat = request.POST.get('food_cat', '')
        fcals = request.POST.get('fcals', '')
        fprice = request.POST.get('fprice', '')
        
     
        food_ = Food(food_name=food_name, food_category=food_cat, food_calorie=fcals, fprice=fprice)
        food_.save()
        return redirect('foodcat')  #
    return render(request, 'myapp/caloriecal.html', {})



# bought_data



def viewtables(request):
    bought = Fbought.objects.all()
    consumed = Fconsumed.objects.all()
    freezed = Ffreezer.objects.all()
    foods = Food.objects.all( )





    bought_expiry= Fbought.objects.all()
    # Get the latest freezer entry for each bought item
    for item in bought_expiry:

      
        # Initialize the expiry date to None
        expiry_date = None
        
        # Check if the item is frozen
        if item.freeze:
            # Get the frozen food life from the Ffreezer table
            freezer_item = Ffreezer.objects.filter(ffbought=item).first()
           
            if freezer_item and freezer_item.ffreeze:
                food_life = int(freezer_item.ffreeze)  # Convert to integer
                expiry_date = item.date + timedelta(days=food_life)
        else:
            # Get the non-frozen food life from the Ffreezer table
            freezer_item = Ffreezer.objects.filter(ffbought=item).first()
        
            if freezer_item and freezer_item.fnfreeze:
                food_life = int(freezer_item.fnfreeze)  # Convert to integer
                expiry_date = item.date + timedelta(days=food_life)

        # Set the calculated expiry date to the item
        item.expiry_date = expiry_date

        #for remaining food part 

    return render(request, 'myapp/viewdetails.html', {'bought_expiry': bought_expiry,'bought_data': bought, 'consumed_data': consumed,"freezer_data":freezed,"foods":foods

    })












    return render(request, "myapp/viewdetails.html", {'bought_data': bought, 'consumed_data': consumed,"freezer_data":freezed})


    









def insert_fconsumed(request):
    fconsumed = request.POST['fconsumed']
    fcamount = request.POST['fcamount']
    food_freeze = request.POST.get('food_freeze') == 'on'
    date=request.POST['date']
    fc_ = Fconsumed( fconsumed=fconsumed,fcamount=fcamount,food_freeze=food_freeze,date=date)
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


def deletefooditem(request,id):
    food_item=Food.objects.get(id=id)
    food_item.delete()
    # return render(request,'myapp/viewdetails.html',{})
    return redirect("/viewtables")



def editfbitem(request,id):
    fb_item=Fbought.objects.get(id=id)
    categories = Food.objects.values('food_category').distinct()
    print('categories',categories)
    return render(request,"myapp/edititem.html",{'fb_item':fb_item,'categories':categories
    })

def editfcitem(request,id):
    fc_item=Fconsumed.objects.get(id=id)
    return render(request,"myapp/editfcitem.html",{'fc_item':fc_item
    })

def editfreezeritem(request,id):
    fz_item=Ffreezer.objects.get(id=id)
    return render(request,"myapp/editfreeze.html",{'fz_item':fz_item
    })

def editfooditem(request,id):
    food_eitem=Food.objects.get(id=id)
    return render(request,"myapp/editfood.html",{'food_eitem':food_eitem
    })



def updatefbitem(request,id):
    # new_fid=request.POST['nid']
    new_fbought=request.POST['nfbought']
    new_ffreeze = request.POST.get('nffreeze') == 'on'
    # new_ffreeze=request.POST['nffreeze']
    new_famount=request.POST['nfamount']
    new_date=request.POST['ndate']
    food_cat = request.POST['fcategory']
    fb=Fbought.objects.get(id=id)
    fb.fbought = new_fbought
    fb.freeze = new_ffreeze
    fb.fbamount = new_famount
    fb.date = new_date
    fb.fcategory = food_cat
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

# fb_item


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



def updatefooditem(request,id):
    # new_fid=request.POST['nid']
    food_ename=request.POST['food_ename']
    food_cat=request.POST['food_cat']
    food_cal=request.POST['food_cal']
    food_eprice = request.POST['fprice']
    food_=Food.objects.get(id=id)
    food_.food_name = food_ename
    food_.food_category = food_cat
    food_.food_calorie= food_cal
    food_.fprice= food_eprice
    food_.save()
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









def insert_ffreeze(request):
    ffbought = request.POST['ffbought']
    flfreeze = request.POST['flfreeze']
    flnfreeze = request.POST['flnfreeze']
    ff= Ffreezer( ffbought=ffbought, ffreeze= flfreeze,fnfreeze=flnfreeze)
    ff.save()
    return render(request,'myapp/ff.html',{})



# def insert_ffreeze(request):
#     if request.method == "POST":
#         fbought_name = request.POST.get('ffbought')
#         flfreeze = request.POST.get('flfreeze')
#         flnfreeze = request.POST.get('flnfreeze')

#         try:
#             # Retrieve the Fbought instance based on the name
#             fbought_instance = Fbought.objects.get(fbought=fbought_name)
            
#             # Create the Ffreezer instance with the Fbought instance
#             ff = Ffreezer(ffbought=fbought_instance, ffreeze=flfreeze, fnfreeze=flnfreeze)
#             ff.save()

#             return redirect('ff')  # Redirect to the ff page or another page after saving
#         except Fbought.DoesNotExist:
#             # Handle the case where the specified Fbought instance does not exist
#             return render(request, 'myapp/ff.html', {'error': 'The specified food item does not exist.'})
    
#     return render(request, 'myapp/ff.html', {})











def remaining_food(request):
    current_date = timezone.now().date()  # Automatically get the current date
    pass
    # Get all distinct food items that have been bought
    # food_items = Fbought.objects.values_list('fbought', flat=True).distinct()
    # print(food_items,"xxxxx------------------>")
    
    # remaining_foods = []

    # for food_item in food_items:
    #     # Calculate the total bought amount of the food item until the current date
    #     total_bought = Fbought.objects.filter(fbought=food_item, date__lte=current_date).aggregate(total=Sum('fbamount'))['total'] or 0

    #     # Calculate the total consumed amount of the food item until the current date
    #     total_consumed = Fconsumed.objects.filter(fconsumed=food_item, date__lte=current_date).aggregate(total=Sum('fcamount'))['total'] or 0

    #     # Calculate the remaining amount
    #     remaining = total_bought - total_consumed

    #     remaining_foods.append({
    #         'food_item': food_item,
    #         'remaining': remaining
    #     })

    # return render(request, 'myapp/index.html', {
    #     'remaining_foods': remaining_foods,
    #     'date': current_date
    # })




def viewdetails_expiry(request):
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

        #for remaining food part 
  

    return render(request, 'myapp/viewdetails.html', {'bought_details': bought

    })





def category_view(request):
    categories = Food.objects.values('food_category').distinct()
    return render(request, 'fb.html', {'categories': categories})


def cal_count(request):
    categories = Food.objects.values('food_name').distinct()
    return render(request,'caloriecal.html',{'categories':categories})
 
#   bought_data



# def insert_ffreeze(request):
#     ffbought = request.POST['ffbought']
#     flfreeze = request.POST['flfreeze']
#     flnfreeze = request.POST['flnfreeze']
#     ff= Ffreezer( ffbought=ffbought, ffreeze= flfreeze,fnfreeze=flnfreeze)
#     ff.save()
#     return render(request,'myapp/ff.html',{})





def insert_foods_cal(request):
    fveg=request.POST['fveg']  #food
    fveg_c=request.POST['veg_count']
    ffruit=request.POST['ffruit']   #food
    ffruit_c=request.POST['fruit_count']
    fcarbs=request.POST['fcarb']    #food 
    fcarbs_c=request.POST['carbs_count']
    fprotein=request.POST['fprotein']  #food
    fprotein_c=request.POST['protein_count']

    fveg_obj = Food.objects.get(food_name=fveg)
   
    ffruit_obj = Food.objects.get(food_name=ffruit)
    fcarbs_obj = Food.objects.get(food_name=fcarbs)
    fprotein_obj = Food.objects.get(food_name=fprotein)


    fveg_cal = fveg_obj.food_calorie
    ffruit_cal = ffruit_obj.food_calorie
    fcarbs_cal = fcarbs_obj.food_calorie
    fprotein_cal = fprotein_obj.food_calorie

    total_fveg_cal =  int(fveg_cal) * int(fveg_c)
    total_ffruit_cal = int(ffruit_cal) * int(ffruit_c)
    total_fprotein_cal = int(fprotein_cal) * int(fprotein_c)
    total_fcarbs_cal = int(fcarbs_cal) * int(fcarbs_c)

# caloriecal

    print(total_fcarbs_cal,total_ffruit_cal,total_fprotein_cal,total_fveg_cal)
    return redirect('calcount')
    # return render(request,'myapp/caloriecal.html',{})


    
#  return redirect('fb')  # Redirect to the fb page or another page after saving
#     return render(request, 'myapp/fb.html', {})