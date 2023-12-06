from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import View,CreateView,FormView,TemplateView,DetailView,ListView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from ecommapp.forms import SignUpForm,SignInForm,CartForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from ecommapp.models import Products,Cart


# Create your views here.
class SignUpView(CreateView):
    template_name="register.html"
    form_class=SignUpForm
    model=User
    success_url=reverse_lazy("log")
class SignInView(FormView):
    template_name="login.html"
    form_class=SignInForm
    def post(self,request,*args,**kwargs):
        form=SignInForm(request.POST) 
        if form.is_valid():
            uname = form.cleaned_data.get("username")
            psw = form.cleaned_data.get("password")
            user = authenticate(request,username = uname,password = psw)
            if user:
                login(request,user)
                msg="Login Sccessful"
                messages.success(request,msg)
                # return render(request,'signin.html')
                return redirect('home')
            else:
                msg="Invalid Credentials"
                messages.error(request,msg)
                return render(request,'signin.html') 
class HomeView(TemplateView):
    template_name="home.html" 

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)   
        all_products=Products.objects.all()
        context["Products"]=all_products
        return context
    
class ProductDetailView(DetailView):
    model=Products
    template_name="productdetail.html"
    pk_url_kwarg="id"
    context_object_name="product"

class AddToCartView(FormView): 
    template_name="addtocart.html"
    form_class=CartForm

    def get(self,request, *args, **kwargs):
        id=kwargs.get("id")
        # print(id)
        product=Products.objects.get(id=id)
        form=CartForm()
        return render(request,self.template_name,{"form":form,"product":product})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("id")
        user=request.user
        product=Products.objects.get(id=id)
        quantity=request.POST.get("quantity")
        Cart.objects.create(user=user,product=product,quantity=quantity)
        return redirect("home")
class CartView(ListView):
    model=Cart
    Template_name="cartview.html"
    cotext_object_name="cart"
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


