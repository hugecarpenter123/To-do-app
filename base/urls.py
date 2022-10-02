from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, CustomRegisterView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login', CustomLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page='login'), name='logout'),
    path('register', CustomRegisterView.as_view(), name='register'),

    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:id>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='update'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='delete'),
]