from django.urls import path
from .views import *
urlpatterns = [
    path("upload/",upload_file,name="upload_file"),
    path("",get_file_data,name="get_file_data"),
    path("search/",get_searched_data,name="get_searched_data")
    # path("admin/", admin.site.urls),
    # path("",include("app.urls"))
]