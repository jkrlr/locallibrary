import datetime
from django.db import models
from django.http import request, Http404
from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from catalog.forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Create your views here.


def index(request):
    """View function for home page of site."""

    # Generate count of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(
        status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of visits to the view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


# Generic Views for model Book

class BookListView(generic.ListView):
    model = Book
    paginate_by = 5


class BookDetailView(generic.DetailView):
    model = Book

# def book_detail_view(request,primary_key):
#     try:
#         book=Book.objects.get(pk=primary_key)
#     except Book.DoesNotExist:
#         raise Http404('Book does not exist')

#     return render(request, 'catalog/book_detail.html', context={'book':book})


def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/book_detail.html', context={'book': book})




# Generic Views for model Author

class AuthorListView(generic.ListView):
    model=Author

class AuthorDetailView(generic.DetailView):
    model=Author

def author_detail_view(request,primary_key):
    author=get_object_or_404(Author,pk=primary_key)
    return render(request,'catalog/author_detail.html',context={'author':author})




# On loan View of books for a user

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model=BookInstance
    template_name='catalog/bookinstance_list_borrowed_user.html'
    paginated_by=10

    def get_queryset(self):
        return  BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksAllListView(PermissionRequiredMixin,generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""

    permission_required = 'catalog.can_mark_returned'
    model=BookInstance
    template_name='catalog/bookinstance_list_borrowed_all.html'
    paginated_by=10
    
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
    
    
    

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this a POST request then process the Form data
    if request.method == 'POST':
        
        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)
        
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            book_instance.due_back= form.cleaned_data['renewal_date']
            book_instance.save()
            
            # redirect ot new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))
        

    # If this is a GET (or any other method) create the default form
    else:
        proposed_renewal_date=datetime.date.today()+datetime.timedelta(weeks=3)
        form=RenewBookForm(initial={'renewal_date':proposed_renewal_date})
    
    context={
        'form':form,
        'book_instance': book_instance,
    }
    
    return render(request,'catalog/book_renew_librarian.html',context)




class AuthorCreate(CreateView,PermissionRequiredMixin):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']
    initial = {'date_of_death':'11/06/2080'} 
    
class AuthorUpdate(UpdateView,PermissionRequiredMixin):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = '__all__'    
    
class AuthorDelete(DeleteView,PermissionRequiredMixin):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(CreateView,PermissionRequiredMixin):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    fields = ['title','author','summary','isbn','genre','language']

class BookUpdate(UpdateView,PermissionRequiredMixin):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    fields = ['title','author','summary','isbn','genre','language']
    
class BookDelete(DeleteView,PermissionRequiredMixin):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    success_url = reverse_lazy('books')
