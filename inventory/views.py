from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Medicine
from .forms import MedicineForm


@login_required
def dashboard(request):

    medicines = Medicine.objects.all()

    today = timezone.now().date()

    total_medicines = medicines.count()

    low_stock = medicines.filter(
        quantity__lte=10
    ).count()

    expired = medicines.filter(
        expiry_date__lt=today
    ).count()

    expiring_soon = medicines.filter(
        expiry_date__gte=today,
        expiry_date__lte=today + timezone.timedelta(days=30)
    ).count()

    return render(request, 'inventory/dashboard.html', {
        'total_medicines': total_medicines,
        'low_stock': low_stock,
        'expired': expired,
        'expiring_soon': expiring_soon,
    })

@login_required
def medicine_list(request):

    medicines = Medicine.objects.all()

    search = request.GET.get('search')
    category = request.GET.get('category')

    if search:
        medicines = medicines.filter(
            name__icontains=search
        )

    if category:
        medicines = medicines.filter(
            category=category
        )

    categories = Medicine.objects.values_list(
        'category',
        flat=True
    ).distinct()

    today = timezone.now().date()

    return render(request, 'inventory/medicine_list.html', {
        'medicines': medicines,
        'categories': categories,
        'search': search,
        'selected_category': category,
        'today': today,
    })


@login_required
def add_medicine(request):

    if request.method == 'POST':

        form = MedicineForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('medicine_list')

    else:
        form = MedicineForm()

    return render(request, 'inventory/add_medicine.html', {
        'form': form
    })


@login_required
def edit_medicine(request, id):

    medicine = Medicine.objects.get(id=id)

    if request.method == 'POST':

        form = MedicineForm(
            request.POST,
            instance=medicine
        )

        if form.is_valid():
            form.save()
            return redirect('medicine_list')

    else:
        form = MedicineForm(
            instance=medicine
        )

    return render(request, 'inventory/edit_medicine.html', {
        'form': form,
        'medicine': medicine
    })


@login_required
def delete_medicine(request, id):

    medicine = Medicine.objects.get(id=id)

    if request.method == 'POST':

        medicine.delete()

        return redirect('medicine_list')

    return render(request, 'inventory/delete_medicine.html', {
        'medicine': medicine
    })