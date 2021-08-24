from django.urls import path

app_name = 'person'

urlpatterns = [
    path('logout/', BlacklistTokenView.as_view(), name="blacklist")
]