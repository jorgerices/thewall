from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from main.models import Users


def logout(request):
    if 'user' in request.session:
        del request.session['user']
    
    return redirect("/login")
    

def login(request):
    if request.method == "POST":
        print(request.POST)
        user = Users.objects.filter(email=request.POST.get('email', False))
        if user:
            log_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):

                user = {
                    "id" : log_user.id,
                    "first_name": f"{log_user.first_name}",
                    "last_name": f"{log_user.last_name}",
                    "email": log_user.email,
                    "role": log_user.role
                }

                request.session['user'] = user
                messages.success(request, "Logueado correctamente")
                return redirect("/")
            else:
                messages.error(request, "Usuario inexistente o contraseña incorrecta")
        else:
            messages.error(request, "Usuario inexistente o contraseña incorrecta")

        return redirect("/login")
    else:
        return render(request, 'login.html')


def signin(request):
    if request.method == 'GET':
        return redirect('/')
        
    if request.method == "POST":
        errors = Users.objects.user_validator(request.POST)
        
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            
            request.session['register_first_name'] = request.POST['first_name']
            request.session['register_last_name'] = request.POST['last_name']
            request.session['register_email'] =  request.POST['email']
            
            request.session['level_mensaje'] = 'alert-danger'
            return redirect('/')

        else:
            request.session['register_first_name'] = ""
            request.session['register_last_name'] = ""
            request.session['register_email'] = ""

            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password_encrypt = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            role=request.POST['role']

            new_user = Users.objects.create(
                first_name=first_name, last_name=last_name, email=email, password=password_encrypt, role=role
            )

            messages.success(request, "El usuario fue agregado con exito")
            request.session['level_mensaje'] = 'alert-success'
            

            request.session['usuario'] = {
                "id" : new_user.id,
                "first_name": f"{new_user.first_name}",
                "last_name": f"{new_user.last_name}",
                "email": new_user.email
            }
        
        return redirect("/")

    return render(request, 'login.html')