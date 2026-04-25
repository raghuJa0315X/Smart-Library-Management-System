from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('researcher', 'Researcher'),
        ('librarian', 'Librarian'),
        ('admin', 'Administrator'),
    ]
    # The fields id, username (Name), role, date_joined (Created At), and status
    # define the core systematic structure requested.
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    status = models.CharField(max_length=20, default='active')
    phone = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    institution_id = models.CharField(max_length=50, unique=True, null=True)


class LibraryBook(models.Model):
    isbn = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    edition = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    shelf_location = models.CharField(max_length=100)
    barcode = models.CharField(max_length=100, unique=True)
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)
    purchase_date = models.DateField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.CharField(max_length=20, default='available')

    def __str__(self):
        return f"{self.title} by {self.author}"

class BookCopy(models.Model):
    book = models.ForeignKey(LibraryBook, on_delete=models.CASCADE, related_name='copies')
    copy_number = models.IntegerField()
    barcode = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default='available') # Available, Issued, Reserved, Maintenance
    condition = models.CharField(max_length=50, default='good')

class Borrowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(LibraryBook, on_delete=models.CASCADE)
    copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    renewal_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='issued') # issued, returned, overdue

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(LibraryBook, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='pending') # pending, fulfilled, cancelled, expired
    queue_position = models.IntegerField()
    reserved_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    fulfilled_date = models.DateTimeField(null=True, blank=True)

class Fine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default='unpaid') # unpaid, paid, waived
    paid_date = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50) # due_date, overdue, reservation, fine
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class DigitalResource(models.Model):
    book = models.ForeignKey(LibraryBook, on_delete=models.SET_NULL, null=True, blank=True)
    file_url = models.URLField()
    format = models.CharField(max_length=20) # PDF, EPUB
    access_expiry = models.DateTimeField(null=True, blank=True)
    download_allowed = models.BooleanField(default=False)

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    details = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)