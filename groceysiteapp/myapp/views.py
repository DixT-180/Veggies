from django.shortcuts import render,redirect

from .models import Fbought, Fconsumed,Ffreezer,Food
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.db.models import Max
from django.db import IntegrityError

from django.core.paginator import Paginator

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
        food_obj = Food.objects.filter(food_name=item['fbought']).first()
        if food_obj:
            food_obj.food_category = item['fcategory']
            food_obj.save()
        else:
            Food.objects.create(food_name=item['fbought'], food_category=item['fcategory'])
    

    paginator = Paginator(food_items, 10)  # Show 10 food items per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'myapp/index.html', {
        'remaining_foods': result,
        'date': current_date,
        'bought_data': bought,
        "freezer_data":freezed,
        "page_obj": page_obj
    

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
        

    
        # Handle the checkbox for freeze
        freeze = request.POST.get('ffreeze') == 'on'
        if fcat=='new':
            new_cat = request.POST.get('new_category','')
            fcat=new_cat
            fb_ = Fbought(fbought=fbought, fbamount=fbamount, date=date, freeze=freeze,fcategory=fcat)
            fb_.save()
        else:
            fb_ = Fbought(fbought=fbought, fbamount=fbamount, date=date, freeze=freeze,fcategory=fcat)
            fb_.save()

        try:
            # Check if the food item already exists
            if not Food.objects.filter(food_name=fbought).exists():
                # Save to Food only if it doesn't exist
                food_ = Food(food_category=fcat)
                food_.save()
            else:
                print(f"Food item '{fbought}' already exists.")

        except IntegrityError as e:
            # Handle duplicate entry error
            print(f"IntegrityError: {e}")
           



        return redirect('fb')  
    return render(request, 'myapp/fb.html', {})

def foodcat(request):
    return render(request,"myapp/foodcat.html")



def insert_food_cat(request):
    if request.method == "POST":
        food_name = request.POST.get('food_name', '')
        food_cat = request.POST.get('food_cat', '')
        fcals = request.POST.get('fcals', '')
        fprice = request.POST.get('fprice', '')
        try:
            food_ = Food(food_name=food_name, food_category=food_cat, food_calorie=fcals, fprice=fprice)
            food_.save()




        except IntegrityError as e:
            # Handle duplicate entry error
            print(f"IntegrityError: {e}")
     
        
        return redirect('foodcat')  #
    return render(request, 'myapp/caloriecal.html', {})





from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    

    fetched_objs = [bought_expiry,consumed,freezed,foods]
    tables_page = ['page','consumed_page','freezer_page','foods_page']

    obj_list=[]
    i=0
    for item in tables_page:
       
        page = request.GET.get(item,1)
        print(item)
        paginator = Paginator(fetched_objs[i], 10)
        i=i+1
    
        try:
            objects = paginator.page(page)
        
        except PageNotAnInteger:
        # If the page is not an integer, show the first page
            objects = paginator.page(1)
        except EmptyPage:
        # If the page is out of range, show the last existing page
            objects = paginator.page(paginator.num_pages)
        obj_list.append(objects)

    print(obj_list,'see here')

    

    


    return render(request, 'myapp/viewdetails.html', {'bought_expiry': bought_expiry,'bought_data': bought,"freezer_data":freezed,"foods":foods,"objects":obj_list[0],'consumed_pg': obj_list[1],'freezer_pg':obj_list[2],'foods_pg':obj_list[3]

    })

    ###################################################3
    page = request.GET.get('page', 1)  # Get the page number from the request

    paginator = Paginator(bought_expiry, 10)  # Show 10 objects per page

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        # If the page is not an integer, show the first page
        objects = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, show the last existing page
        objects = paginator.page(paginator.num_pages)
    print(objects,'xxx-------------->')



    return render(request, 'myapp/viewdetails.html', {'bought_expiry': bought_expiry,'bought_data': bought, 'consumed_data': consumed,"freezer_data":freezed,"foods":foods,"objects":objects

    })




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
  
    new_fbought=request.POST['nfbought']
    new_ffreeze = request.POST.get('nffreeze') == 'on'
 
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
            # fbought_instance = Fbought.objects.get(fbought=fbought_name)

            new_fz = request.POST.get('flfreeze')
            new_nfz = request.POST.get('flnfreeze')

            fz.ffbought = fbought_name
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


def insert_ffreeze(request):
    ffbought = request.POST['ffbought']
    flfreeze = request.POST['flfreeze']
    flnfreeze = request.POST['flnfreeze']
    ff= Ffreezer( ffbought=ffbought, ffreeze= flfreeze,fnfreeze=flnfreeze)
    ff.save()
    return render(request,'myapp/ff.html',{})




def viewdetails_expiry(request):
    bought = Fbought.objects.all()

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
 






from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Food

def insert_foods_cal(request):
    if request.method == 'POST':
        try:
            fveg = request.POST.get('fveg', '').strip()
            fveg_c = request.POST.get('veg_count', '').strip()
            ffruit = request.POST.get('ffruit', '').strip()
            ffruit_c = request.POST.get('fruit_count', '').strip()
            fcarbs = request.POST.get('fcarb', '').strip()
            fcarbs_c = request.POST.get('carbs_count', '').strip()
            fprotein = request.POST.get('fprotein', '').strip()
            fprotein_c = request.POST.get('protein_count', '').strip()

            # Check if any value is empty
            if not all([fveg, fveg_c, ffruit, ffruit_c, fcarbs, fcarbs_c, fprotein, fprotein_c]):
                raise ValueError("All fields must be filled.")

            # Get Food objects
            fveg_obj = Food.objects.get(food_name=fveg)
            ffruit_obj = Food.objects.get(food_name=ffruit)
            fcarbs_obj = Food.objects.get(food_name=fcarbs)
            fprotein_obj = Food.objects.get(food_name=fprotein)

            # Get calorie values
            fveg_cal = fveg_obj.food_calorie
            ffruit_cal = ffruit_obj.food_calorie
            fcarbs_cal = fcarbs_obj.food_calorie
            fprotein_cal = fprotein_obj.food_calorie

            # Calculate total calories
            total_fveg_cal = float(fveg_cal) * float(fveg_c)
            total_ffruit_cal = float(ffruit_cal) * float(ffruit_c)
            total_fprotein_cal = float(fprotein_cal) * float(fprotein_c)
            total_fcarbs_cal = float(fcarbs_cal) * float(fcarbs_c)
            totals_ = total_fveg_cal + total_ffruit_cal + total_fprotein_cal + total_fcarbs_cal

            return render(request, 'myapp/index.html', {'totals': totals_})
        
        except ValueError as e:
            messages.error(request, "enter calories first")
            return redirect('index')  # Redirect to the form page

        except Food.DoesNotExist:
            messages.error(request, 'One or more food items are not found. Please enter valid food items.')
            return redirect('index')

        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {str(e)}')
            return redirect('index')

    # If not POST request, render the form
    return render(request, 'myapp/index.html')
