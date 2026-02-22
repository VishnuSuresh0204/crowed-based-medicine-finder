from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.db.models import Q
import datetime

# --- AUTHENTICATION ---

def index(request):
    return render(request, 'index.html')

def login_view(request):
    msg = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.user_type == 'admin':
                login(request, user)
                return redirect('/admin_home/')
                
            elif user.user_type == 'pharmacy':
                try:
                    pharmacy = Pharmacy.objects.get(login=user)
                    if pharmacy.status == 'approve':
                        login(request, user)
                        request.session['pid'] = pharmacy.id
                        return redirect('/pharmacy_home/')
                    elif pharmacy.status == 'reject':
                        msg = "Your account is rejected"
                    elif pharmacy.status == 'block':
                        msg = "Your account is blocked"
                    else:
                        msg = "Wait for approval"
                except Pharmacy.DoesNotExist:
                    msg = "Pharmacy profile not found"
            
            elif user.user_type == 'user':
                try:
                    u_obj = User.objects.get(login=user)
                    login(request, user)
                    request.session['uid'] = u_obj.id
                    return redirect('/user_home/')
                except User.DoesNotExist:
                    msg = "User profile not found"

            elif user.user_type == 'delivery':
                try:
                    db = DeliveryBoy.objects.get(login=user)
                    if db.status == 'active':
                        login(request, user)
                        request.session['db_id'] = db.id
                        return redirect('/delivery_home/')
                    else:
                        msg = "Account Inactive"
                except:
                    msg = "Profile not found"

        else:
            msg = "Invalid Credentials"
    return render(request, 'login.html', {'msg': msg})

def user_reg(request):
    msg = ""
    if request.method == 'POST':
        name = request.POST.get('name')
        place = request.POST.get('place')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        image = request.FILES.get('image')
        u = request.POST.get('username')
        p = request.POST.get('password')
        if Login.objects.filter(username=u).exists():
            msg = "Username already exists"
        else:
            user = Login.objects.create_user(username=u, password=p, user_type='user', view_password=p)
            User.objects.create(login=user, name=name, place=place, phone=phone, email=email, address=address, image=image)
            return redirect('/login/')
    return render(request, 'user_reg.html', {'msg': msg})

def pharmacy_reg(request):
    msg = ""
    if request.method == 'POST':
        name = request.POST.get('name')
        place = request.POST.get('place')
        location = request.POST.get('location')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        u = request.POST.get('username')
        p = request.POST.get('password')
        image = request.FILES.get('image')
        if Login.objects.filter(username=u).exists():
            msg = "Username already exists"
        else:
            user = Login.objects.create_user(username=u, password=p, user_type='pharmacy', view_password=p)
            Pharmacy.objects.create(login=user, name=name, place=place, location=location, contact_number=contact, email=email, image=image)
            return redirect('/login/')
    return render(request, 'pharmacy_reg.html', {'msg': msg})

def logout_view(request):
    logout(request)
    return redirect('/login/')

def my_invoices(request):
    if 'uid' in request.session:
        user = User.objects.get(id=request.session['uid'])
        history_bookings = Booking.objects.filter(user=user, payment_status='paid').order_by('-date')
        
        history_groups = {}
        for b in history_bookings:
            if b.payment_id not in history_groups:
                history_groups[b.payment_id] = {
                    'items': [],
                    'total': 0,
                    'date': b.date
                }
            history_groups[b.payment_id]['items'].append(b)
            history_groups[b.payment_id]['total'] += b.amount
            
        return render(request, 'user/invoices.html', {'history_groups': history_groups})
    return redirect('/login/')

# --- BILLING VIEWS ---

# --- ADMIN VIEWS ---

def admin_home(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        return render(request, 'admin/home.html')
    return redirect('/login/')

def manage_pharmacy(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        action = request.GET.get('action')
        id = request.GET.get('id')
        if action and id:
            try:
                ph = Pharmacy.objects.get(id=id)
                if action == 'approve':
                    ph.status = 'approve'
                elif action == 'reject':
                    ph.status = 'reject'
                elif action == 'block':
                    ph.status = 'block'
                elif action == 'unblock':
                    ph.status = 'approve'
                ph.save()
                return redirect('/manage_pharmacy/')
            except:
                pass
        
        pharmacies = Pharmacy.objects.all()
        return render(request, 'admin/manage_pharmacy.html', {'pharmacies': pharmacies})
    return redirect('/login/')

def view_users(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        users = User.objects.all()
        return render(request, 'admin/view_users.html', {'users': users})
    return redirect('/login/')

def view_feedbacks(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        feedbacks = Feedback.objects.all()
        return render(request, 'admin/view_feedbacks.html', {'feedbacks': feedbacks})
    return redirect('/login/')

def view_reports(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        reports = Report.objects.all()
        return render(request, 'admin/view_reports.html', {'reports': reports})
    return redirect('/login/')

def admin_view_deliveries(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        bookings = Booking.objects.all().order_by('-date')
        return render(request, 'admin/view_deliveries.html', {'bookings': bookings})
    return redirect('/login/')

def admin_view_pharmacy_delivery_boys(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        id = request.GET.get('id')
        pharmacy = Pharmacy.objects.get(id=id)
        delivery_boys = DeliveryBoy.objects.filter(pharmacy=pharmacy)
        return render(request, 'admin/view_pharmacy_delivery_boys.html', {'pharmacy': pharmacy, 'delivery_boys': delivery_boys})
    return redirect('/login/')

# --- PHARMACY VIEWS ---

def pharmacy_home(request):
    if 'pid' in request.session:
        return render(request, 'pharmacy/home.html')
    return redirect('/login/')

def add_medicine(request):
    msg = ""
    if 'pid' in request.session:
        if request.method == 'POST':
            name = request.POST.get('name')
            details = request.POST.get('details')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            category = request.POST.get('category')
            prescription_required = request.POST.get('prescription_required') == 'on'
            image = request.FILES.get('image')
            pharmacy = Pharmacy.objects.get(id=request.session['pid'])
            Medicine.objects.create(pharmacy=pharmacy, name=name, details=details, price=price, stock=stock, image=image, category=category, prescription_required=prescription_required)
            msg = "Medicine Added"
            return redirect('/manage_medicine/')
        return render(request, 'pharmacy/add_medicine.html', {'msg': msg})
    return redirect('/login/')

def manage_medicine(request):
    if 'pid' in request.session:
        pharmacy = Pharmacy.objects.get(id=request.session['pid'])
        category = request.GET.get('category')
        
        medicines = Medicine.objects.filter(pharmacy=pharmacy)
        
        if category:
            medicines = medicines.filter(category=category)
            
        return render(request, 'pharmacy/manage_medicine.html', {'medicines': medicines})
    return redirect('/login/')

def edit_medicine(request):
    msg = ""
    if 'pid' in request.session:
        id = request.GET.get('id')
        medicine = Medicine.objects.get(id=id)
        if request.method == 'POST':
            medicine.name = request.POST.get('name')
            medicine.details = request.POST.get('details')
            medicine.price = request.POST.get('price')
            medicine.stock = request.POST.get('stock')
            medicine.category = request.POST.get('category')
            medicine.prescription_required = request.POST.get('prescription_required') == 'on'
            if request.FILES.get('image'):
                medicine.image = request.FILES.get('image')
            medicine.save()
            return redirect('/manage_medicine/')
        return render(request, 'pharmacy/edit_medicine.html', {'medicine': medicine, 'msg': msg})
    return redirect('/login/')

def delete_medicine(request):
    if 'pid' in request.session:
        id = request.GET.get('id')
        Medicine.objects.filter(id=id).delete()
        return redirect('/manage_medicine/')
    return redirect('/login/')

def add_delivery_boy(request):
    msg = ""
    if 'pid' in request.session:
        pharmacy = Pharmacy.objects.get(id=request.session['pid'])
        if request.method == 'POST':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            u = request.POST.get('username')
            p = request.POST.get('password')
            if Login.objects.filter(username=u).exists():
                msg = "Username already exists"
            else:
                user = Login.objects.create_user(username=u, password=p, user_type='delivery', view_password=p)
                DeliveryBoy.objects.create(login=user, pharmacy=pharmacy, name=name, phone=phone, email=email)
                return redirect('/view_delivery_boys/')
        return render(request, 'pharmacy/add_delivery_boy.html', {'msg': msg})
    return redirect('/login/')

def view_delivery_boys(request):
    if 'pid' in request.session:
        pharmacy = Pharmacy.objects.get(id=request.session['pid'])
        delivery_boys = DeliveryBoy.objects.filter(pharmacy=pharmacy)
        return render(request, 'pharmacy/view_delivery_boys.html', {'delivery_boys': delivery_boys})
    return redirect('/login/')

def delete_delivery_boy(request):
    if 'pid' in request.session:
        id = request.GET.get('id')
        try:
            db = DeliveryBoy.objects.get(id=id)
            db.login.delete()
            return redirect('/view_delivery_boys/')
        except:
             pass
    return redirect('/login/')

def pharmacy_bookings(request):
    if 'pid' in request.session:
        pharmacy = Pharmacy.objects.get(id=request.session['pid'])
        
        date_str = request.GET.get('date')
        if date_str:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            date = datetime.date.today()
            
        bookings = Booking.objects.filter(medicine__pharmacy=pharmacy, date__date=date)
        return render(request, 'pharmacy/view_bookings.html', {'bookings': bookings, 'date': date.strftime('%Y-%m-%d')})
    return redirect('/login/')

def pharmacy_booking_details(request):
    if 'pid' in request.session:
        id = request.GET.get('id')
        try:
            pharmacy = Pharmacy.objects.get(id=request.session['pid'])
            booking = Booking.objects.get(id=id)
            delivery_boys = DeliveryBoy.objects.filter(pharmacy=pharmacy)
            
            if request.method == 'POST':
                action = request.POST.get('action')
                if action == 'approve':
                    booking.status = 'booked'
                    booking.save()
                elif action == 'reject':
                    booking.status = 'rejected'
                    # Restore stock
                    booking.medicine.stock += booking.quantity
                    booking.medicine.save()
                    booking.save()
                elif action == 'assign':
                    db_id = request.POST.get('delivery_boy')
                    db = DeliveryBoy.objects.get(id=db_id)
                    booking.delivery_boy = db
                    booking.delivery_status = 'pending' 
                    booking.save()
                return redirect(f'/pharmacy_booking_details/?id={id}')
                
            return render(request, 'pharmacy/booking_details.html', {'booking': booking, 'delivery_boys': delivery_boys})
        except:
            pass
        return redirect('/pharmacy_bookings/')
    return redirect('/login/')

def pharmacy_feedbacks(request):
    if 'pid' in request.session:
        pharmacy = Pharmacy.objects.get(id=request.session['pid'])
        feedbacks = Feedback.objects.filter(pharmacy=pharmacy)
        return render(request, 'pharmacy/view_feedbacks.html', {'feedbacks': feedbacks})
    return redirect('/login/')


def pharmacy_profile(request):
    if 'pid' in request.session:
        pharmacy = Pharmacy.objects.get(id=request.session['pid'])
        if request.method == 'POST':
            pharmacy.name = request.POST.get('name')
            pharmacy.place = request.POST.get('place')
            pharmacy.location = request.POST.get('location')
            pharmacy.contact_number = request.POST.get('contact')
            pharmacy.email = request.POST.get('email')
            if request.FILES.get('image'):
                pharmacy.image = request.FILES.get('image')
            pharmacy.save()
            return redirect('/pharmacy_home/')
        return render(request, 'pharmacy/profile.html', {'p': pharmacy})
    return redirect('/login/')

# --- USER VIEWS ---

def user_home(request):
    if 'uid' in request.session:
        return render(request, 'user/home.html')
    return redirect('/login/')

def user_profile(request):
    if 'uid' in request.session:
        user = User.objects.get(id=request.session['uid'])
        if request.method == 'POST':
            user.name = request.POST.get('name')
            user.place = request.POST.get('place')
            user.phone = request.POST.get('phone')
            user.email = request.POST.get('email')
            user.address = request.POST.get('address')
            if request.FILES.get('image'):
                user.image = request.FILES.get('image')
            user.save()
            return redirect('/user_home/')
        return render(request, 'user/profile.html', {'u': user})
    return redirect('/login/')

def view_shops(request):
    if 'uid' in request.session:
        search = request.GET.get('search')
        if search:
            pharmacies = Pharmacy.objects.filter(
                Q(place__icontains=search) | 
                Q(name__icontains=search) |
                Q(medicine__name__icontains=search)
            ).distinct().filter(status='approve')
        else:
            pharmacies = Pharmacy.objects.filter(status='approve')
        return render(request, 'user/view_shops.html', {'pharmacies': pharmacies})
    return redirect('/login/')

def view_medicines(request):
    if 'uid' in request.session:
        id = request.GET.get('id')
        search = request.GET.get('search')
        category = request.GET.get('category')
        pharmacy = None
        
        medicines = Medicine.objects.all()
        
        if id:
            pharmacy = Pharmacy.objects.get(id=id)
            medicines = medicines.filter(pharmacy=pharmacy)
            
        if search:
            medicines = medicines.filter(name__icontains=search)
            
        if category:
            medicines = medicines.filter(category=category)
            
        categories = Medicine.CATEGORY_CHOICES
        return render(request, 'user/view_medicines.html', {'pharmacy': pharmacy, 'medicines': medicines, 'categories': categories})
    return redirect('/login/')

def book_medicine_qty(request):
    msg = ""
    if 'uid' in request.session:
        id = request.GET.get('id')
        medicine = Medicine.objects.get(id=id)
        if request.method == 'POST':
            qty = int(request.POST.get('quantity'))
            address = request.POST.get('address')
            if medicine.stock >= qty:
                # Deduct stock immediately (Reservation)
                medicine.stock -= qty
                medicine.save()
                
                amount = medicine.price * qty
                user = User.objects.get(id=request.session['uid'])
                
                status = 'booked'
                prescription = None
                
                if medicine.prescription_required:
                    status = 'pending_approval'
                    prescription = request.FILES.get('prescription')
                
                Booking.objects.create(user=user, medicine=medicine, quantity=qty, amount=amount, status=status, payment_status='pending', prescription=prescription, address=address)
                return redirect('/my_bookings/')
            else:
                msg = "Out of Stock"
        return render(request, 'user/add_quantity.html', {'medicine': medicine, 'msg': msg})
    return redirect('/login/')

def my_bookings(request):
    if 'uid' in request.session:
        user = User.objects.get(id=request.session['uid'])
        # Active bookings: not paid or not delivered or not confirmed
        active_bookings = Booking.objects.filter(user=user).exclude(payment_status='paid', delivery_status='delivered', user_confirmed=True)
        # History: paid, delivered, and confirmed
        history_bookings = Booking.objects.filter(user=user, payment_status='paid', delivery_status='delivered', user_confirmed=True).order_by('-date')
        
        total_amount = 0
        for b in active_bookings:
            if b.payment_status == 'pending' and b.status == 'booked':
                total_amount += b.amount
        
        # Group history by payment_id
        history_groups = {}
        for b in history_bookings:
            pid = b.payment_id or 'order_'+str(b.id)
            if pid not in history_groups:
                history_groups[pid] = {'date': b.date, 'items': [], 'total': 0}
            history_groups[pid]['items'].append(b)
            history_groups[pid]['total'] += b.amount

        return render(request, 'user/my_bookings.html', {
            'active_bookings': active_bookings, 
            'history_groups': history_groups,
            'total_amount': total_amount
        })
    return redirect('/login/')

def make_payment(request):
    msg = ""
    if 'uid' in request.session:
        user = User.objects.get(id=request.session['uid'])
        if request.method == 'POST':
            pending_bookings = Booking.objects.filter(user=user, payment_status='pending', status='booked')
            if not pending_bookings.exists():
                return redirect('/my_bookings/')
                
            payment_id = 'PAY' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            # Stock is already reserved, just update status
            for b in pending_bookings:
                b.payment_status = 'paid'
                b.status = 'paid'
                b.payment_id = payment_id
                b.save()
            
            return redirect(f'/bill/?pid={payment_id}')
        
        total_amount = sum(b.amount for b in Booking.objects.filter(user=user, payment_status='pending', status='booked'))
        return render(request, 'user/payment.html', {'msg': msg, 'total_amount': total_amount})
    return redirect('/login/')

def bill(request):
    if 'uid' in request.session:
        user = User.objects.get(id=request.session['uid'])
        payment_id = request.GET.get('pid')
        if payment_id == "None": payment_id = None
        
        if payment_id:
            bookings = Booking.objects.filter(user=user, payment_id=payment_id)
        else:
            bookings = Booking.objects.filter(user=user, payment_status='paid').order_by('-date')
            if bookings.exists():
                payment_id = bookings[0].payment_id
                bookings = bookings.filter(payment_id=payment_id)
        
        if not bookings.exists():
            return redirect('/my_invoices/')

        total = sum(b.amount for b in bookings)
        date = bookings[0].date if bookings.exists() else datetime.datetime.now()
        
        return render(request, 'user/bill.html', {'bookings': bookings, 'total': total, 'date': date, 'payment_id': payment_id})
    return redirect('/login/')

def cancel_booking(request):
    if 'uid' in request.session:
        id = request.GET.get('id')
        try:
            booking = Booking.objects.get(id=id)
            if booking.payment_status == 'pending':
                # Restore stock
                medicine = booking.medicine
                medicine.stock += booking.quantity
                medicine.save()
                
                booking.delete()
        except:
            pass
        return redirect('/my_bookings/')
    return redirect('/login/')

def confirm_delivery(request):
    if 'uid' in request.session:
        id = request.GET.get('id')
        try:
            b = Booking.objects.get(id=id)
            if b.delivery_status == 'delivered':
                b.user_confirmed = True
                b.status = 'delivered'
                b.save()
        except:
            pass
        return redirect('/my_bookings/')
    return redirect('/login/')

def user_feedback(request):
    msg = ""
    if 'uid' in request.session:
        id = request.GET.get('id')
        booking_id = request.GET.get('booking_id')
        user = User.objects.get(id=request.session['uid'])
        
        if request.method == 'POST':
            message = request.POST.get('message')
            if booking_id:
                b = Booking.objects.get(id=booking_id)
                Feedback.objects.create(user=user, pharmacy=b.medicine.pharmacy, booking=b, message=message)
            elif id:
                 ph = Pharmacy.objects.get(id=id)
                 Feedback.objects.create(user=user, pharmacy=ph, message=message)
            else:
                 Feedback.objects.create(user=user, message=message)
            return redirect('/user_home/')
        return render(request, 'user/send_feedback.html', {'msg': msg})
    return redirect('/login/')

def user_report(request):
    msg = ""
    if 'uid' in request.session:
        if request.method == 'POST':
            message = request.POST.get('message')
            pharmacy_id = request.GET.get('id')
            user = User.objects.get(id=request.session['uid'])
            if pharmacy_id:
                 ph = Pharmacy.objects.get(id=pharmacy_id)
                 Report.objects.create(user=user, pharmacy=ph, message=message)
            else:
                 msg = "Select a pharmacy to report"
            if not msg:
                return redirect('/user_home/')
        return render(request, 'user/send_report.html', {'msg': msg})
    return redirect('/login/')

# --- DELIVERY VIEWS ---

def delivery_home(request):
    if 'db_id' in request.session:
        return render(request, 'delivery/home.html')
    return redirect('/login/')

def delivery_deliveries(request):
    if 'db_id' in request.session:
        db = DeliveryBoy.objects.get(id=request.session['db_id'])
        bookings = Booking.objects.filter(delivery_boy=db).order_by('-date')
        
        if request.method == 'POST':
            id = request.POST.get('id')
            status = request.POST.get('status')
            try:
                b = Booking.objects.get(id=id)
                b.delivery_status = status
                b.save()
            except:
                pass
            return redirect('/delivery_deliveries/')
            
        return render(request, 'delivery/view_deliveries.html', {'bookings': bookings})
    return redirect('/login/')
