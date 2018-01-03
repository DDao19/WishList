from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^main$', views.index, name="landing"),
    url(r'^login$', views.login, name="login"),
    url(r'^register$', views.register, name="register"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^dashboard$', views.dashboard, name="dashboard"),
    url(r'^wish_items/create$', views.add, name="add"),
    url(r'^create$', views.create, name="create"),
    url(r'^delete/(?P<id>\d+)$', views.delete, name="delete"),
    url(r'^wish_items/(?P<id>\d+)$', views.user, name="user"),
    url(r'^remove/(?P<id>\d+)$', views.remove, name="remove"),
    url(r'^add_wishlist/(?P<id>\d+)$', views.add_wishlist, name="add_wishlist"),
]
