
# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import Product, Supplier, Students
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
        return render(request, "index.html", {'products': all_products, 'sn': sn, 'suppliers': all_suppliers, 'no_of_suppliers': no_of_suppliers})
    except:
        return render(request, "index.html")


def test(request):
    return render(request, "msg.html")


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

    if int(request.POST.get("noSupplier")) != 0:
        product.supplier.sname = request.POST.get("inputSupplierName")
        product.supplier.email = request.POST.get("inputEmail")
        product.supplier.contact = request.POST.get("inputContact")
        product.supplier.address = request.POST.get("inputAddress")
    product.save()
    messages.success(request, 'Product Updated Successfully.')
    return redirect('/')


def delete_product(request, pid):
    product = Product.objects.get(id=pid)
    product.delete()
    messages.success(request, "Product Deleted Successfully.")
    return redirect('/')


def deduct_qty(request):
    bill = json.loads(request.POST.get('bill'))
    print(bill)
    print(type(bill))
    for item in bill['particulars']:
        print(item)
        print(type(item))
    return JsonResponse({'value': request.POST.get('csrfmiddlewaretoken')}, safe=False)


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

