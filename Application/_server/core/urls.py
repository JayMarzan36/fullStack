from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.index, name="index"),
    path("graph", view=views.getNotesForGraph, name="graph"),
    path("notes/", view=views.note, name="note"),
    path("getnotes/", view=views.getNotes, name="getNotes"),
]
