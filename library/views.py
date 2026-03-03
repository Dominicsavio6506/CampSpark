from django.shortcuts import render
from .models import Book, BorrowRecord
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

def library_home(request):
    dept = request.GET.get('dept')
    books = Book.objects.all()

    if dept:
        books = books.filter(department=dept)

    taken_books = BorrowRecord.objects.filter(
        student=request.user,
        return_date__isnull=True
    ).values_list("book_id", flat=True)

    departments = Book.objects.values_list(
        'department', flat=True
    ).distinct()

    return render(request, "library/home.html", {
        "books": books,
        "taken_books": taken_books,
        "departments": departments
    })


def library_admin_panel(request):
    return render(request, "library/admin_panel.html")


def issue_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # 1️⃣ Prevent duplicate borrow
    if BorrowRecord.objects.filter(
        student=request.user,
        book=book,
        return_date__isnull=True
    ).exists():
        return redirect('library_home')

    # 2️⃣ Limit max 3 active books per user
    active_count = BorrowRecord.objects.filter(
        student=request.user,
        return_date__isnull=True
    ).count()

    if active_count >= 3:
        return redirect('library_home')

    # 3️⃣ Check availability
    if book.available_quantity <= 0:
        return redirect('library_home')

    # 4️⃣ Create borrow record
    BorrowRecord.objects.create(
        student=request.user,
        book=book,
        due_date=timezone.now() + timedelta(days=7)
    )

    # 5️⃣ Reduce stock
    book.available_quantity -= 1
    book.save()

    return redirect('library_home')

def my_books(request):
    records = BorrowRecord.objects.filter(student=request.user)
    return render(request, "library/my_books.html", {"records": records})

def is_library_staff(user):
    return user.is_staff 


@user_passes_test(is_library_staff)
def manage_books(request):
    books = Book.objects.all()

    q = request.GET.get("q")
    dept = request.GET.get("dept")

    if q:
        books = books.filter(title__icontains=q)

    if dept:
        books = books.filter(department=dept)

    departments = Book.objects.values_list(
        "department", flat=True
    ).distinct()

    return render(request,
        "library/manage_books.html",
        {
            "books": books,
            "departments": departments
        })


@user_passes_test(is_library_staff)
def issued_books(request):
    records = BorrowRecord.objects.filter(
        return_date__isnull=True
    )

    student_id = request.GET.get("student_id")

    if student_id:
        try:
            records = records.filter(
                student__id=int(student_id)
            )
        except ValueError:
            records = records.none()

    return render(
        request,
        "library/issued_books.html",
        {
            "records": records
        }
    )

def return_book(request, record_id):
    record = get_object_or_404(
        BorrowRecord,
        id=record_id,
        return_date__isnull=True
    )

    # allow only staff OR owner
    if not (request.user.is_staff or record.student == request.user):
        return redirect('library_home')

    record.return_date = timezone.now()
    record.save()

    book = record.book

    # increase only if not exceeding total
    if book.available_quantity < book.total_quantity:
        book.available_quantity += 1
        book.save()

    return redirect('issued_books' if request.user.is_staff else 'my_books')