from app.models import *
page = Page.objects.create()
staff_page = Page.objects.create(url_pathname="staff-page")
user = User.objects.create(email="superuser@email.com", page=page)
user.is_superuser = True
user.set_password("password")
user.save()
staff_user = User.objects.create(email="staff@email.com", page=staff_page)
staff_user.set_password("password")
staff_user.save()
EmailEntry.objects.create(email="email1@email.com", page=page)
EmailEntry.objects.create(email="email2@email.com", page=staff_page)
