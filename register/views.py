from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def register(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['pass1']
		confirm_password = request.POST['pass2']
		if password != confirm_password:
			messages.warning(request, "Password is not matching")
			return render(request, 'register/register.html')

		try:
			if User.objects.get(username=email):
				messages.warning(request, 'Email is taken')
				return render(request, 'register/register.html')

		except Exception as identifier:
			pass


		myuser = User.objects.create_user(email, email, password)
		myuser.save()
		messages.info(request, 'Signup SuccessFull! Please Login')
		return redirect('/login/')

	return render(request, 'register/register.html')

def handlelogin(request):
	if request.method == 'POST':
		username = request.POST['username']
		userpassword = request.POST['pass1']
		myuser = authenticate(username=username, password=userpassword)

		if myuser is not None:
			login(request, myuser)
			messages.success(request, 'Login Success')
			return redirect('/')
		else:
			messages.error(request, 'Something went wrong')
			return redirect('/login/')



	return render(request, 'register/login.html')

def handlelogout(request):
	logout(request)
	return redirect('/') 