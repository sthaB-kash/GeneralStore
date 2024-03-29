
# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import Product, Supplier, Students, Customer, Bill, Particulars, Notification
from django.contrib import messages
from django.db.models import Q
import json
# for User forms
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .serializer import ProductSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# prevent from accessing page without login
from django.contrib.auth.decorators import login_required

from datetime import datetime, date
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar


class ProductList(APIView):

    def get(self, request):
        products = Product.objects.all()
        all_products = ProductSerializer(products, many=True)
        return Response(all_products.data)

    def post(self):
        pass


def home_page(request):
    home_page_suppliers = Supplier.objects.all()
    home_page_products = Product.objects.all()
    return render(request, 'homepage.html', {'suppliers': home_page_suppliers, 'products': home_page_products })


def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            print(user)
            messages.success(request, 'User account successfully created for \'' + user + '\'')
            return redirect('login')
    context = {
        'form': form
    }
    return render(request, "Register.html", context)


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if request.POST.get('superuser_login'):
                if user.is_superuser:
                    return redirect('register')
                else:
                    messages.info(request, "Username or  Password is invalid")
                    return render(request, 'login.html', {'superuser_login': True})
            else:
                login(request, user)
                # print(user)
                request.session['user_id'] = user.id
                request.session['user_email'] = user.email
                return redirect('/')
        else:
            messages.info(request, "Username or  Password is invalid")
    context = {}
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    try:
        del request.session['user_id']
        del request.session['user_email']
    except KeyError:
        pass
    return redirect('login')


@login_required(login_url='login')
def index(request):
    try:
        all_products = Product.objects.all()
        all_suppliers = Supplier.objects.all()
        no_of_suppliers = all_suppliers.count()
        sn = all_products.count()
        # customers = Bill.objects.all()


        get_major_notification(0)
        notification = Notification.objects.filter(unread=True).count()

        return render(request, "index.html", {'products': all_products, 'sn': sn, 'suppliers': all_suppliers,
                                              'no_of_suppliers': no_of_suppliers, 'notification': notification})
    except:
        return render(request, "index.html")


def notification(request):
    try:
        key = int(request.GET.get('key'))
        notification_title = Notification.objects.get(pk=key).des
        if key == 1:
            n_products = Product.objects.filter(pk__in=get_major_notification(1))
        elif key == 2:
            n_products = Product.objects.filter(pk__in=get_major_notification(2))
        elif key == 5:
            n_products = Product.objects.filter(pk__in=get_major_notification(5))
        print("low qty:", low_qty_id)
        return render(request, "selected_notification.html", {'products': n_products, 'title': notification_title})
    except:
        pass
    get_major_notification(0)
    notifi = Notification.objects.filter(unread=True)
    return render(request, "notification.html", {'notification': notifi})


def users(request):
    if request.method == "POST":
        user_updated_status = False
        user = json.loads(request.POST.get('user'))
        fname = user['fname']
        lname = user['lname']
        email = user['email']
        active = user['active']
        privilege = user['privilege']
        print(fname,lname,email,active,privilege)
        update_user = User.objects.get(id=int(user['id']))
        update_user.first_name = fname
        update_user.last_name = lname
        update_user.email = email
        update_user.is_active = active
        update_user.is_staff = privilege
        update_user.save()
        user_updated_status = True

        return JsonResponse({'success': user_updated_status}, safe=False)
    else:
        try:
            user_id = int(request.GET.get('user_id'))
            print(user_id)
            requested_user = User.objects.values().get(id=user_id)
            return render(request, "selectedUser.html", {'user': requested_user})
        except:
            pass
        registered_users = User.objects.all()
        return render(request, "RegisteredUsers.html", {'users': registered_users})


def search(request):
    search_query = request.GET['data']
    sn = 0
    if search_query:
        result = Product.objects.all().filter(Q(pname__icontains=search_query) | Q(category__icontains=search_query)
                                               | Q(pid__icontains=search_query)) # | Q(supplier.sname__icontains=search_query))
        sn = result.count()
    else:
        result = Product.objects.all()
        sn = result.count()
    # return JsonResponse(list(result), safe=False)
    return render(request, "search_response.html", {'products': result, 'sn': sn})


def show_details(request):
    search_id = request.GET['id']
    # print(search_id)
    product = Product.objects.get(id=search_id)
    return render(request, "showDetails.html", {'product': product})


def add_product(request):
    p_id = request.POST.get("inputId")
    p_name = request.POST.get("inputName")
    qty = request.POST.get("inputQty")
    category = request.POST.get("inputCategory")
    mfd = request.POST.get("inputMfd")
    exp = request.POST.get("inputDexp")
    price = request.POST.get("inputPrice")
    total_price = float(qty)*float(price)

    supplier_name = request.POST.get("inputSupplierName")
    supplier = Supplier.objects.all()
    sid = 0
    for s in supplier:
        if s.sname == supplier_name:
            sid = s.id
            break

    if sid == 0:
        email = request.POST.get("inputEmail")
        contact = request.POST.get("inputContact")
        address = request.POST.get("inputAddress")
        new_supplier = Supplier.objects.create(sname=supplier_name, address=address, email=email, contact=contact)
        sid = new_supplier.id

    Product.objects.create(pid=p_id, pname=p_name, category=category, price=price, qty=qty,
                           total_price=total_price, mfd=mfd, exp=exp, supplier_id=sid)
    messages.success(request, 'Product Added Successfully.')

    product_added_notification = Notification(des='Product Added: ' + p_name)
    product_added_notification.save()
    return redirect('/')


def edit_product(request, pid):
    product = Product.objects.get(id=pid)
    supplier = Supplier.objects.get(id=product.supplier_id)
    return render(request, "EditProduct.html", {'product': product, 'supplier': supplier})


def update_product(request, pid):
    product = Product.objects.get(id=pid)

    sid = Product.objects.get(id=pid).supplier_id
    product.pid = request.POST.get("inputId")
    product.pname = request.POST.get("inputName")
    product.qty = request.POST.get("inputQty")
    product.category = request.POST.get("inputCategory")
    product.mfd = request.POST.get("inputMfd")
    product.exp = request.POST.get("inputDexp")
    product.price = request.POST.get("inputPrice")
    product.total_price = float(request.POST.get("inputQty")) * float(request.POST.get("inputPrice"))

    try:
        if int(request.POST.get("noSupplier")) != 0:
            product.supplier.sname = request.POST.get("inputSupplierName")
            product.supplier.email = request.POST.get("inputEmail")
            product.supplier.contact = request.POST.get("inputContact")
            product.supplier.address = request.POST.get("inputAddress")
    except TypeError:
        pass
    product.save()
    messages.success(request, 'Product Updated Successfully.')
    product_updated_notification = Notification(des=product.pname + ' is updated.')
    product_updated_notification.save()
    return redirect('/')


def delete_product(request, pid):
    product = Product.objects.get(id=pid)
    product.delete()
    messages.success(request, "Product Deleted Successfully.")
    product_deleted_notification = Notification(des=product.pname + ' is deleted.')
    product_deleted_notification.save()
    return redirect('/')


def deduct_qty(request):
    bill = json.loads(request.POST.get('bill'))
    # print(bill)
    # print(type(bill))
    # for item in bill['particulars']:
    #     print(item)
    #     print(type(item))
    success = False
    try:
        # customer's details
        name = bill['name']
        address = bill['address']
        contact = bill['contact']
        c1 = Customer(name=name, address=address, contact=contact)
        # print(f"customer--> name:{name}, address:{address}, contact:{contact}")
        c1.save()

        # bill details
        amount = bill['total_amt']
        discount = bill['discount']
        paid_amount = bill['grant_total']
        sold_by = bill['sold_by']
        # print(f"bill-->{amount} {discount} {paid_amount} {sold_by}")
        b1 = Bill(customer=c1, amount=amount, discount=discount, paid_amount=paid_amount, sold_by=User.objects.get(username=sold_by))
        b1.save()
        # print(b1)

        # particulars
        items = bill['particulars']
        # print(items)
        # print(items[0]['item'])
        p1 = Particulars(bill=b1, purchase_items=items)
        p1.save()

        # deduct qty of sold product
        for product in bill['particulars']:
            sold_product = Product.objects.get(pname=product['item'])
            sold_product.qty = sold_product.qty - int(product['qty'])
            sold_product.save()
        success = True
    except:
        pass
    # return JsonResponse({'value': request.POST.get('csrfmiddlewaretoken')}, safe=False)
    return JsonResponse({'success': success}, safe=False)


def updated_products(request):
    prod = Product.objects.all()
    print(prod)
    return render(request, "all_products.html", {'products': prod})


def products(request):
    # if 'value' in request.GET:
    print(request.GET.get("term"))
    qs = Product.objects.filter(pname__icontains=request.GET.get('term'))
    product = list()
    for p in qs:
        product.append(p.pname)
    return JsonResponse(product, safe=False)


def test1(request):
    return HttpResponse("<h1>ok</h1>")


def suppliers(request):
    # if 'value' in request.GET:
    print(request.GET.get("term"))
    qs = Supplier.objects.filter(sname__icontains=request.GET.get('term'))
    supplier = list()
    for s in qs:
        supplier.append(s.sname)
    return JsonResponse(supplier, safe=False)


def auto_fill_supplier_info(request):
    try:
        qs = Supplier.objects.values().get(sname=request.GET.get('name'))
        # print(qs)
        return JsonResponse(qs, safe=False)
    except:
        return JsonResponse({}, safe=False)


def get_product_details(request):
    print(request.GET.get('name'))
    all_products = list(Product.objects.values())
    return JsonResponse(all_products, safe=False)


def get_qty_and_price(request):
    try:
        qs = Product.objects.values('pname', 'price', 'qty').get(pname=request.GET.get('product'))
        # print(qs)
        return JsonResponse(qs, safe=False)
    except:
        return JsonResponse({'false': 0}, safe=False)


def qrcode_billing(request):

    def capture():
        cap = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cap.set(3, 340)
        cap.set(4, 280)
        while True:
            ret, frame = cap.read()
            decodedObj = pyzbar.decode(frame)
            for obj in decodedObj:
                print("data:", obj.data.decode())
                cv2.putText(frame, str(obj.data), (50, 50), font, 0.9, (255, 0, 0), 3, cv2.LINE_AA)
            if decodedObj:
                return render(request, "qty.html")
                break
            cv2.imshow('Billing-QR code', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    try:
        capture()
    except ConnectionAbortedError:
        pass


def make_bill(request):
    return JsonResponse({'success': True}, safe=False)


def customer_receipt(request):
    bill = Bill.objects.values().get(id=request.GET.get('id'))
    customer = Customer.objects.values().get(id=bill['customer_id'])
    particulars = Particulars.objects.values().get(bill=bill['id'])
    # particulars = json.loads('{particulars:'+str(receipt.purchase_items)+'}')
    # print(particulars)
    # print(type(particulars))
    return JsonResponse({'receipt': bill, 'customer': customer, 'particulars': particulars}, safe=False)


def product_transaction_supplier(request):
    n_p = Product.objects.all().count()
    nt = Bill.objects.all().count()
    ns = Supplier.objects.all().count()
    return JsonResponse({'np': n_p, 'nt': nt, 'ns': ns}, safe=False)


def customer_details(request):
    date = datetime.now().strftime("%Y-%m-%d")
    data = request.GET.get('data')
    #
    if request.GET.get('customer_search') == '1':
        # print("search")
        customers = Bill.objects.filter(customer__name__startswith=request.GET.get('data'))
        return render(request, "customer_search.html", {'customers': customers, 'no': customers.count()})
    elif data:
        # print("inside date")
        customers = Bill.objects.filter(date__startswith=request.GET.get('data'))
        date = request.GET.get('data')
    else:
        customers = Bill.objects.all()
        # print("all")

    return render(request, "customer_details.html", {'customers': customers, 'date': date, 'no': customers.count()})


def reports(request):
    return render(request, "all_reports.html")


def get_major_notification(key):
    # check for expiry date
    text = ''
    today = datetime.now().date()
    product_expiry = Product.objects.all().values('id', 'exp', 'qty')
    product_expiry_id = list()
    expired_product_id = list()
    low_qty_id = list()
    for product in product_expiry:
        diff = product['exp'] - today
        if (diff.days <= 55) and (diff.days > 0):
            product_expiry_id.append(product['id'])
        elif diff.days <= 0:
            expired_product_id.append(product['id'])
        else:
            pass

        low_qty_value = 20
        if product['qty'] < 20:
            low_qty_id.append(product['id'])

    print(product_expiry_id)
    print(expired_product_id)
    product_near_expiry_date = len(product_expiry_id)

    if product_near_expiry_date > 0:
        msg = Notification.objects.get(id=1)
        msg.des = str(product_near_expiry_date) + ' Products are near expiry date.'
        msg.save()

    expired_product = len(expired_product_id)
    if expired_product > 0:
        msg = Notification.objects.get(id=2)
        if expired_product > 1:
            text = ' Products have been expired.'
        else:
            text = ' Product has been expired.'
        msg.des = str(expired_product) + text
        msg.save()

    low_qty = len(low_qty_id)
    if low_qty > 0:
        msg = Notification.objects.get(id=5)
        if low_qty > 1:
            text = ' Product has QTY less than 20'
        else:
            text = ' Products have QTY less than 20'
        msg.des = str(low_qty) + text
        msg.save()

    if key == 1:
        return product_expiry_id
    elif key == 2:
        return expired_product_id
    elif key == 5:
        return low_qty_id


def curd(request):
    students = Students.objects.all()
    return render(request, "curd.html", {'students': students})


def add(request):
    return render(request, "addNew.html")


def insert(request):
    s_name = request.POST.get("name")
    s_semester = request.POST.get("semester")
    s_program = request.POST.get("program")
    student = Students.objects.create(name=s_name, semester=int(s_semester), program=s_program)
    # student.save()
    messages.success(request, 'Record Saved Successfully.')

    students = Students.objects.all()
    # return render(request, "curd.html", {"students": students})
    return redirect('/curd')


def details(request, sid):
    response = '<h1>Looking for student\'s details having id: %s</h1>'
    # return HttpResponse(response % sid)
    std = Students.objects.get(id=sid)
    return render(request, "stdEdit.html", {"std": std})


def std_delete(request, sid):
    std = Students.objects.get(id=sid)
    std.delete()
    # return render(request, "stdDelete.html", {"std": std})
    return redirect('/curd')


def update(request, sid):
    # std = Students.objects.get(id=sid)
    s_name = request.POST.get("name")
    s_semester = request.POST.get("semester")
    s_program = request.POST.get("program")
    student = Students(id=sid, name=s_name, semester=int(s_semester), program=s_program)
    student.save()
    students = Students.objects.all()
    # return render(request, "curd.html", {"students": students})
    return redirect('/curd')


product_expiry_id = list()
expired_product_id = list()
low_qty_id = list()