from typing import Any, Dict
from django.db.models.query import QuerySet
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login

from women.forms import *
from .models import *
from .utils import *

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.



class WomenHome(DataMixin, ListView):
    
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
   

    def get_context_data(self, *, object_list=None, **kwargs ):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")


        return dict(list(context.items()) + list(c_def.items()))
    
    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')


# def index(request):
#     posts = Women.objects.all()
#     cats = Category.objects.all()

#     context = {
#         'posts': posts, 
#         'cats': cats,
#         'menu':menu, 
#         'title': 'ГЛАВНАЯ',
#         'cat_selected' : 0, 
#     }

#     return render(request, 'women/index.html', context= context)

def about(request):
    return render(request, 'women/about.html',  {'menu':menu,'title': 'КАТЕГОРИИ'})

class AddPage(LoginRequiredMixin, DataMixin, CreateView):

    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs ):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")

        return dict(list(context.items()) + list(c_def.items()))

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
    
#             form.save()
#             return redirect("home")
           

#     else:
#         form = AddPostForm()

#     return render(request, 'women/addpage.html', {'form': form, 'menu':menu, 'title':'Добавление статьи'})

def contact(request):
    return HttpResponse('СТраница контакты')


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs ):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])

        return dict(list(context.items()) + list(c_def.items()))

    

# def showpost(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)

#     context = {
#         'post': post,
#         'menu':menu, 
#         'title': post.title,
#         'cat_selected' : post.cat_id,
        
#     }

#     return render(request, 'women/post.html', context=context)





def pageNotFound(request, exception):
    return HttpResponseNotFound(f"СТраница не найдена")


class WomenCategory(DataMixin, ListView):
    
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs ):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория' + str(c.name),
                                      cat_selected=c.pk)

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

# def show_category(request, cat_slug):

#     category = get_object_or_404(Category, slug=cat_slug)
#     posts_in_category = Women.objects.filter(cat=category)
    
#     cats = Category.objects.all()

#     if len(posts_in_category) == 0:
#         raise Http404()

#     context = {
#         'posts': posts_in_category, 
#         'cats': cats,
#         'menu':menu, 
#         'title': 'ГЛАВНАЯ',
#     }

#     return render(request, 'women/index.html', context= context)




class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()) )
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()) )
    
    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')