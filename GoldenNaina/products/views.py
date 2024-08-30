from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Product, Category, Theme_model, ProductReview, Wishlist, ProductImages, Stock, PopularSearch
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from django.db.models import Avg
from .forms import ProductReviewForm
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView


def Products(request):
    featured_products = Product.objects.order_by('priority')[:4]
    latest_products = Product.objects.order_by('-id')[:4]
    offer_themes = Theme_model.objects.all()
    categories = Category.objects.all()[5:]
    if request.user.is_authenticated:
        wishlist_products = Wishlist.objects.filter(user=request.user).values_list('product', flat=True)
    else:
        wishlist_products = []
    
    context = {
      'featured_products': featured_products,
        'latest_products': latest_products,
        'offer_themes': offer_themes,
        'categories': categories,
        'wishlist_products': wishlist_products,

    }
    return render(request, 'index.html', context) 


def ProductList(request):
    page = request.GET.get('page', 1)
    sort_option = request.GET.get('sort', 'default')

    product_list = Product.objects.all()
    total_products_count = Product.objects.all().count()
    
    if sort_option == 'low_to_high':
        product_list = product_list.order_by('price')
    elif sort_option == 'high_to_low':
        product_list = product_list.order_by('-price')
    else:
        product_list = product_list.order_by('-priority')
    
    product_paginator = Paginator(product_list, 20)  # Show 4 products per page.
    product_list = product_paginator.get_page(page)
    
    context = {
        'products': product_list,
        'sort_option': sort_option,
        'total_products_count': total_products_count,
    }
    return render(request, 'product_list.html', context)

def Product_Detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    p_images = product.product_images.all() 
    products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    get_percentage = product.get_percentage()
    stocks = Stock.objects.filter(product=product)

    context = {
        'product': product,
        'p_images': p_images,
        'get_percentage': get_percentage,
        'products': products,
        'stocks': stocks,
    }
    return render(request, 'product_detail.html', context)

def tag_list(request, tag_slug=None):
   products = Product.objects.filter(tag__slug=tag_slug).order_by('-priority')
   tag = None
   if tag_slug:
      tag = get_object_or_404(Tag, slug=tag_slug)
      products = products.filter(tag__in=[tag])
      context = {
         'products': products,
         'tag': tag
      }
      return render(request, 'tags.html', context)
   

# products navbar category 
def womens(request):
    sort_option = request.GET.get('sort', 'default')
    page = request.GET.get('page', 1)

    if sort_option == 'low_to_high':
        women_products = Product.objects.filter(category=2).order_by('price')
    elif sort_option == 'high_to_low':
        women_products = Product.objects.filter(category=2).order_by('-price')
    else:
        women_products = Product.objects.filter(category=2)
    
    paginator = Paginator(women_products, 16)  
    women_products = paginator.get_page(page)
    
    context = {
        'women_products': women_products,
        'sort_option': sort_option,
    }
    return render(request, 'women.html', context)

def mens(request):
    sort_option = request.GET.get('sort', 'default')
    page = request.GET.get('page', 1)
    
    if sort_option == 'low_to_high':
        men_products = Product.objects.filter(category=1).order_by('price')
    elif sort_option == 'high_to_low':
        men_products = Product.objects.filter(category=1).order_by('-price')
    else:
        men_products = Product.objects.filter(category=1)
    
    paginator = Paginator(men_products, 16)  # Show 4 products per page.
    men_products = paginator.get_page(page)
    
    context = {
        'men_products': men_products,
        'sort_option': sort_option,
    }
    return render(request, 'men.html', context)


def watches(request):
    sort_option = request.GET.get('sort', 'default')
    page = request.GET.get('page', 1)

    if sort_option == 'low_to_high':
        watch_products = Product.objects.filter(category=3).order_by('price')
    elif sort_option == 'high_to_low':
        watch_products = Product.objects.filter(category=3).order_by('-price')
    else:
        watch_products = Product.objects.filter(category=3)

    paginator = Paginator(watch_products, 16)  # Show 4 products per page.
    watch_products = paginator.get_page(page)

    context = {
        'watch_products': watch_products,
        'sort_option': sort_option,
    }
    return render(request, 'watches.html', context)

def accessories(request):
    sort_option = request.GET.get('sort', 'default')
    page = request.GET.get('page', 1)

    if sort_option == 'low_to_high':
        accessories_products = Product.objects.filter(category=4).order_by('price')
    elif sort_option == 'high_to_low':
        accessories_products = Product.objects.filter(category=4).order_by('-price')
    else:
        accessories_products = Product.objects.filter(category=4)

    paginator = Paginator(accessories_products, 16)  # Show 4 products per page.
    accessories_products = paginator.get_page(page)

    context = {
        'accessories_products': accessories_products,
        'sort_option': sort_option,
    }
    return render(request, 'accessories.html', context)

def Beauty(request):
    sort_option = request.GET.get('sort', 'default')
    page = request.GET.get('page', 1)

    if sort_option == 'low_to_high':
        Beauty_products = Product.objects.filter(category=5).order_by('price')
    elif sort_option == 'high_to_low':
        Beauty_products = Product.objects.filter(category=5).order_by('-price')
    else:
        Beauty_products = Product.objects.filter(category=5)

    paginator = Paginator(Beauty_products, 16)  # Show 4 products per page.
    Beauty_products = paginator.get_page(page)

    context = {
        'Beauty_products': Beauty_products,
        'sort_option': sort_option,
    }
    return render(request, 'Beauty.html', context)


# other category views
class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_option = self.request.GET.get('sort', 'default')
        page = self.request.GET.get('page', 1)
        
        if sort_option == 'low_to_high':
            products = self.object.product_set.all().order_by('price')
        elif sort_option == 'high_to_low':
            products = self.object.product_set.all().order_by('-price')
        else:
            products = self.object.product_set.all()
        
        paginator = Paginator(products, 16)  # Show 4 products per page.
        products = paginator.get_page(page)
        
        context['products'] = products
        context['sort_option'] = sort_option
        return context

@login_required
def reviews(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = ProductReview.objects.filter(product=product).order_by('-date')
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    review_form = ProductReviewForm()

    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
    else:
        form = ProductReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': average_rating,
        'review_form': form,
    }
    return render(request, 'reviews.html', context)

@require_POST
def ajax_add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    user = request.user
    
    rating = request.POST.get('rating')
    review_text = request.POST.get('review')
    
    if not rating or not review_text:
        return JsonResponse({'error': 'Rating and review text are required'}, status=400)

    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            raise ValueError("Invalid rating")
    except ValueError:
        return JsonResponse({'error': 'Invalid rating value'}, status=400)

    review = ProductReview.objects.create(
        product=product,
        user=user,
        rating=rating,
        review=review_text
    )
    
    context = {
        'user': user.username,
        'review': review_text,
        'rating': rating,
    }
    
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))['rating']
    
    return JsonResponse({
        'context': context,
        'boolean': True,
        'average_rating': round(average_rating, 1) if average_rating else 0
    })

def search(request):
    popular_searches = PopularSearch.objects.all()
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user)[:3]
    else:
        wishlist = []  # Empty list if the user is not authenticated

    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).order_by('-priority')
    else:
        products = Product.objects.none()  # Return an empty queryset if query is None or empty

    context = {
        'products': products,
        'query': query,
        'wishlist': wishlist,
        'popular_searches': popular_searches,
    }
    return render(request, 'search.html', context)



# wishlist views

@login_required
def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(product=product, user=request.user)

    if created:
        # The item was added to the wishlist
        context = {
            'bool': True,
        }
    else:
        # The item was already in the wishlist, so we remove it
        wishlist.delete()
        context = {
            'bool': False,
        }

    return JsonResponse(context)

@login_required
def remove_from_wishlist(request):
    product_id = request.GET.get('id')
    
    # Attempt to get the product or return a 404 error if not found
    product = get_object_or_404(Product, id=product_id)
    
    # Get the wishlist item to remove
    wishlist_item = Wishlist.objects.filter(product=product, user=request.user).first()
    
    if wishlist_item:
        wishlist_item.delete()
        context = {
            'bool': True,  # Success
        }
    else:
        context = {
            'bool': False,  # Item wasn't found in the wishlist
        }
        
    return JsonResponse(context)

@login_required
def wishlist_view(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist': wishlist,
    }
    return render(request, 'wishlist.html', context)


# size chart

def size_chart(request):
    return render(request, 'size_chart.html')