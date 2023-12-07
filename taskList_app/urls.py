from django.urls import path

from taskList_app import views


urlpatterns = [
    path('', views.home, name="home"),
    path('how-it-works/', views.howitworks, name="how-it-works"),
    path('login/', views.loginPage, name="login"),
    path('signup/', views.signupPage, name="signup"),
    path('logout/', views.logoutPage, name="logout"),
    path('all-tasks/', views.allTasks, name="all-task"),
    path('add-task/', views.addTask, name="add-task"),
    path('delete-task/<int:task_id>', views.deleteTask, name="delete-task"),
    path('edit-task/<int:task_id>', views.editTask, name="edit-task"),
]


