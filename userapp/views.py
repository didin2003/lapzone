from django.shortcuts import render ,redirect,get_object_or_404
from . models import Reg_tbl ,Pro_tbl,Rent_tbl,cart_tbl,sell_tbl,service_tbl,rental_tbl,sell_pro_tbl,customer_tbl
from django .contrib import messages
from django .contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse
import json
from django.db.models import Count


def index (request):
    return render(request,"index.html")
def reg (request):
    if request.method=='POST':
        fnm = request.POST.get('fn')
        mob = request.POST.get('mb')
        eml = request.POST.get('em')
        psw = request.POST.get('ps')
        cpsw = request.POST.get('cps')
        ads  = request.POST.get('ad')
        pin  = request.POST.get('pin')
        if psw!=cpsw:
            return render(request,"registration.html",{'error': "Passwords not Matching"})
        obj = Reg_tbl.objects.create(fname=fnm,mobile=mob,email=eml,pssw=psw,cpssw=cpsw,add=ads,pincode=pin)
        obj.save()
        if obj:
            return redirect("/")
        else:
            return render(request,"registration.html")
    return render(request,"registration.html")
def log (request):
    if request.method=='POST':
        un = request.POST.get('usname')
        ps = request.POST.get('psword')
        obj = Reg_tbl.objects.filter(fname=un,pssw=ps)
        if obj:
            request.session['usn'] = un
            request.session['psa'] = ps
            for m in obj:
                idno = m.id
                request.session['idl'] = idno
                return redirect("/")
        else:
            msg = "Invalid Credentails........"
            request.session['usn'] = ''
            request.session['psa'] = ''
            return render(request,"login.html",{"error":msg})
    return render(request,"login.html")
def clogin(request):
    if 'idl' in request.session:
        del request.session['idl']
        return redirect('/')
    else:
        return render(request,"login.html")

def logout_view(request):
    logout(request)
    return redirect("/")

def product (request):
    if request.method=='POST':
        prd = request.POST.get('prname')
        prc = request.POST.get('prprice')
        pic = request.FILES.get('primage')
        des = request.POST.get('prdetails')
        obj = Pro_tbl.objects.create(pnm=prd,prc=prc,pim=pic,des=des)
        obj.save()
        if obj:
            msg = "Details Uploded Sucessfully....."
            return render(request,"product.html",{"success":msg})
        else:
            return render(request, "product.html", {"error": "Please upload an image!"})
    return render(request,"product.html")

def product2(request):
    obj = Pro_tbl.objects.all()
    return render(request,"product2.html",{"data":obj})


def sell_reg(request):
    if request.method=='POST':
        slm = request.POST.get('sn')
        smob = request.POST.get('smb')
        seml = request.POST.get('sem')
        spsw = request.POST.get('sps')
        scpsw = request.POST.get('scps')
        if spsw!=scpsw:
            return render(request,"sellerreg.html",{'error':"Password not Matching"})
        obj = sell_tbl.objects.create(sname=slm,smobile=smob,semail=seml,spssw=spsw,scpssw=scpsw)
        obj.save()
        if obj:
            return render(request,"sellerlog.html")
        else:
            return render(request,"sellerreg.html")
    return render(request,"sellerreg.html")
    
def sell_log(request):
    if request.method=='POST':
        sellername= request.POST.get('selname')
        sellerpass= request.POST.get('selpas')
        obj = sell_tbl.objects.filter(sname=sellername,spssw=sellerpass)
        if obj:
            request.session['slm'] = sellername
            request.session['sps'] = sellerpass
            for m in obj:
                sidno = m.id
                request.session['ids'] = sidno
                return render(request,"product.html") 
        else:
            msg = "Invalid Credentails.."
            request.session['slm'] = ''
            request.session['sps'] = ''
            return render(request,"sellerlog.html",{'error':msg})
    return render(request,"sellerlog.html")

def seller_pro_det(request):
    obj = Pro_tbl.objects.all()
    return render(request,"prodetails.html",{'details':obj})

def buy(request, pid):
    product = get_object_or_404(Pro_tbl, id=pid)
    cid = request.session.get('idl')  

    if not cid:
        messages.error(request, "You must be logged in to make a purchase.")
        return redirect('login')  

    customer = get_object_or_404(Reg_tbl, id=cid)

    if request.method == "POST":
        customer_order = customer_tbl.objects.create(product=product, user=customer)
        return redirect('pay', order_id=customer_order.id)

    return render(request, "buynow.html", {'customer': customer, 'product': product})


def payment(request, order_id):  # Use order_id instead of pid
    order = get_object_or_404(customer_tbl, id=order_id)  # Fetch order
    return render(request, "payment.html", {'order': order})  # Pass order



def cart(request,idn):
    product = Pro_tbl.objects.get(id=idn)
    cid = request.session['idl']
    customer = Reg_tbl.objects.get(id=cid)
    cartitem,created = cart_tbl.objects.get_or_create(product=product,customer=customer)
    if not created:
        cartitem.qty+=1
        cartitem.save()
    messages.success(request,"item added to cart..")
    return redirect("/product2")

def viewcart(request):
    cid = request.session['idl']
    cobj = Reg_tbl.objects.get(id=cid)
    cartobj = cart_tbl.objects.filter(customer=cobj)
    if cartobj:
        totalprice = 0
        for m in cartobj:
            pro = m.product.prc*m.qty
            totalprice = totalprice+pro
        return render(request,"cart.html",{'cart':cartobj,'total':totalprice})
    else:
        return render(request,"cart.html",{'info':"your cart is empty.."})


def cartdelete(request,pid):
    product = cart_tbl.objects.get(id=pid)
    product.delete()
    return redirect("/viewcart")

def cartpayment(request):
    cid = request.session.get('idl')
    cobj = Reg_tbl.objects.get(id=cid)
    cartobj = cart_tbl.objects.filter(customer=cobj)
    totalprice = sum(m.product.prc * m.qty for m in cartobj)
    return render(request, "payment2.html", {'cart': cartobj, 'total': totalprice})

def rent (request):
    if request.method=='POST':
        rprd = request.POST.get('rprname')
        rprc = request.POST.get('rprprice')
        rpic = request.FILES.get('rprimage')
        rdes = request.POST.get('rprdetails')
        obj = Rent_tbl.objects.create(rpnm=rprd,rprc=rprc,rpim=rpic,rdes=rdes)
        obj.save()
        if obj:
            msg = "Details Uploded Sucessfully....."
            return render(request,"rent.html",{"success":msg})
        else:
            return render(request, "rent.html", {"error": "Please upload an image!"})
    return render(request,"rent.html")

def rent2 (request):
    obj = Rent_tbl.objects.all()
    return render(request,"rent2.html",{'ren':obj})


def rent_book(request, idb):
    selected_rent = get_object_or_404(Rent_tbl, id=idb)
    all_rentals = Rent_tbl.objects.all()
    
    if request.method == 'POST':
        full_name = request.POST.get('rn')
        rental_item = request.POST.get("rpnm")
        address = request.POST.get('radd')
        aadhar = request.POST.get('raa')
        mobile = request.POST.get('rm')
        date = request.POST.get('rd')
        months = int(request.POST.get('rmo', 1)) 
        
        
        final_amount = selected_rent.rprc * months 
        base_amount = selected_rent.rprc
    
        obj = rental_tbl.objects.create(
            rname=full_name, 
            ritem = rental_item,
            raddress=address, 
            raadhar=aadhar, 
            rmobile=mobile, 
            rdate=date, 
            rmonths=months,
            ramount=final_amount,
            rprice = base_amount
        )
        obj.save()

        if obj:
            return render(request, "rentbooked.html", {
                "success": "Booking successful!", 
                "selected_rent": selected_rent,
                "final_amount": final_amount  
            })
        else:
            return render(request, "rentbook.html", {
                "error": "All fields are required.", 
                "selected_rent": selected_rent
            })

    return render(request, "rentbook.html", {
        'selected_rent': selected_rent, 
        'rent': all_rentals, 
        'months': range(1, 13)
    })

def rentpayment(request):
    cid = request.session.get('idl')
    return render(request,"payment3.html")




def edit (request,ide):
    obj = Pro_tbl.objects.get(id=ide)
    return render(request,"prodetails2.html",{'product':obj})

def pro_delete(request,prid):
    productdelete = Pro_tbl.objects.get(id=prid)
    productdelete.delete()
    return redirect("prodetails")


def update (request,ide):
    obj = Pro_tbl.objects.get(id=ide)
    if request.method=='POST':
        product_pnm = request.POST.get('proname')
        product_prc = request.POST.get('proprice')
        product_des = request.POST.get('prodes')
        obb = Pro_tbl.objects.filter(id=ide)
        obb.update(pnm=product_pnm,prc=product_prc,des=product_des)
        return redirect("prodetails")
    return render(request,"product2.html",{'product':obj})


def admin_log(request):
    if request.method=='POST':
        admin_name = request.POST.get('adname')
        admin_pass = request.POST.get('adpass')
        if admin_name=='laptop' and admin_pass=='123':
            return render(request,"admin.html")
        else:
            msg = "Invalid Login"
            return render(request,"adminlog.html",{'error':msg})
    return render(request,"adminlog.html")

def admin_log(request):
    if request.method == 'POST':
        admin_name = request.POST.get('adname', '').strip()
        admin_pass = request.POST.get('adpass', '').strip()

        if admin_name == 'laptop' and admin_pass == '123':
            # Count Achieved Values
            total_sales = customer_tbl.objects.count()
            total_rentals = rental_tbl.objects.count()
            total_services = service_tbl.objects.count()
            total_users = Reg_tbl.objects.count()
            total_products = Pro_tbl.objects.count()

            
            target_sales = 50
            target_rentals = 50
            target_services = 50
            target_overall = (target_sales + target_rentals + target_services)  

            # Calculate Overall Achieved
            overall_achieved = total_sales + total_rentals + total_services

            # Prepare Data for Charts (Achieved vs Target)
            sales_labels = ["Achieved", "Remaining"]
            sales_values = [total_sales, max(0, target_sales - total_sales)]

            rental_labels = ["Achieved", "Remaining"]
            rental_values = [total_rentals, max(0, target_rentals - total_rentals)]

            service_labels = ["Achieved", "Remaining"]
            service_values = [total_services, max(0, target_services - total_services)]

            overall_labels = ["Achieved", "Remaining"]
            overall_values = [overall_achieved, max(0, target_overall - overall_achieved)]

            context = {
                'total_sales': total_sales,
                'total_rentals': total_rentals,
                'total_services': total_services,
                'total_users': total_users,
                'total_products': total_products,
                'sales_labels': json.dumps(sales_labels),
                'sales_values': json.dumps(sales_values),
                'rental_labels': json.dumps(rental_labels),
                'rental_values': json.dumps(rental_values),
                'service_labels': json.dumps(service_labels),
                'service_values': json.dumps(service_values),
                'overall_labels': json.dumps(overall_labels),
                'overall_values': json.dumps(overall_values),
            }

            return render(request, "admin.html", context)
        else:
            return render(request, "adminlog.html", {'error': "Invalid Login"})

    return render(request, "adminlog.html")

def adm_logout(request):
    return redirect("adminlog")

def reg_cus_view(request):
    obj = Reg_tbl.objects.all()
    return render(request,"reg_cus_data.html",{'data':obj})

def reg_pro_view(request):
    objp = Pro_tbl.objects.all()
    return render(request,"reg_pro_data.html",{'pdata':objp})

def reg_cus_edit(request,idc):
    obj = Reg_tbl.objects.get(id=idc)
    if request.method=='POST':
        cuname = request.POST.get('cn')
        cumobile = request.POST.get('cm')
        cuemail = request.POST.get('ce')
        cupass = request.POST.get('cp')
        cucpass = request.POST.get('ccp')
        obb = Reg_tbl.objects.filter(id=idc)
        obb.update(fname=cuname,mobile=cumobile,email=cuemail,pssw=cupass,cpssw=cucpass)
        return redirect("reg_cus")
    return render(request,"reg_cus_data2.html",{'edit':obj})

def reg_cus_delete(request,idc):
    obj = Reg_tbl.objects.filter(id=idc)
    obj.delete()
    return redirect("reg_cus")

def reg_pro_edit(request,idp):
    obj = Pro_tbl.objects.get(id=idp)
    if request.method=='POST':
        prn = request.POST.get('pn')
        prp = request.POST.get('pp')
        prd = request.POST.get('pd')
        obb = Pro_tbl.objects.filter(id=idp)
        obb.update(pnm=prn,prc=prp,des=prd)
        return redirect('reg_pro')
    return render(request,"reg_pro_data2.html",{'edit':obj})

def service_book(request):
    if request.method=='POST':
        itname = request.POST.get('itn')
        issue = request.POST.get('iss')
        address = request.POST.get('adr')
        mobile = request.POST.get('mbnum')
        date = request.POST.get('dt')
        cuname = request.POST.get('scu')
        obj = service_tbl.objects.create(item=itname,issues=issue,address=address,mobile=mobile,date=date,name=cuname)
        obj.save()
        if obj :
            return render(request,"servicebook.html")
        else:
            return render(request,"service.html")

    return render(request,"service.html")

def reg_ser_view(request):
    obj = service_tbl.objects.all()
    return render(request,"reg_ser_data.html",{'service':obj})

def reg_rent_view (request):
    obj = rental_tbl.objects.all()
    return render(request,"reg_rent_data.html",{'rent':obj})

def reg_buy_view(request):
    obj = customer_tbl.objects.all()
    return render(request,"reg_buy_data.html",{'buy':obj})



def view_seller_pro(request):
    sid = request.session['ids']
    sobj = sell_tbl.objects.get(id=sid)
    sellobj = sell_pro_tbl.objects.filter(seller=sobj)
    if sellobj:
        return render(request,"sellcart.html",{'scart':sellobj})
    else:
        return render(request,"sellcart.html",{'info':"NO PRODUCTS ADDED"})
    
def tech_assin(request):
    return render (request,"service_tech_assign.html")

def my_orders(request):
    bid = request.session['idl']
    bobj = Reg_tbl.objects.get(id=bid)
    orders = customer_tbl.objects.filter(user=bobj)
    if orders:
        return render(request,"orders.html",{'orders':orders})

    return render (request,"orders.html",{'error': "NO ORDERS.."})
    
