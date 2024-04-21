from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib import messages
from .models import Product, Order, Cart, UserProfile, Feedback, Advertisement, ForumPost, ForumComment, Category, UserProfile, ForumTopic
from .forms import OrderForm, FeedbackForm, ForumPostForm, ForumCommentForm, UserProfileForm, AdvertisementForm
from django.db.models import Q
from django.http import JsonResponse



def index(request):
    return render(request, 'app/index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login') 

def product_list(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    
    products = Product.objects.filter(
        Q(name__icontains=q)|
        Q(description__icontains = q) 
        )
    
    if q.isdigit():
        products = Product.objects.filter(category=q)
    
    
    category = Category.objects.all()

    context = {'products': products, 'category':category}
    return render(request, 'app/product_list.html', context )

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'app/product_detail.html', {'product': product})

@login_required

def add_to_cart(request, product_id):
    user = request.user
    product = get_object_or_404(Product, pk=product_id)
    print("one")

    cart_item = Cart.objects.filter(user=user, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        Cart(user=user, product_id=product_id, quantity=1).save()

    return redirect('product_list')


@login_required
def cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)

    shipping_amount = 10.00
    amount = 0
    totalamount = 0
    for p in cart:
        value = p.quantity * p.product.price
        amount = amount + value
    totalamount = amount + 10

    print(totalamount)

    context = {'cart': cart, 'totalamount':totalamount, 'shipping_amount':shipping_amount}

    return render(request, 'app/cart.html', context)



@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    # if not cart_items:
    #     return redirect('empty_cart_page')

    total_amount = sum(item.total_cost for item in cart_items)
    print(total_amount)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total_amount
            order.save()
            cart_items.delete()  
            return redirect('order_list')
    else:
        form = OrderForm()

    context = {
        'form': form,
        'total_amount': total_amount  
    }
    return render(request, 'app/checkout.html', context)

@login_required
def order_detail(request, id):
    order = get_object_or_404(Order, pk=id, user=request.user)
    print(order.products.all())
    products = list(order.products.all())
    print(products)
    context = {'order': order, 'products': products}
    return render(request, 'app/order_detail.html', context)

def order_list(request):
    # orders = Order.objects.all()
    orders = Order.objects.filter(user=request.user)
    return render(request, 'app/order_list.html', {'orders': orders})


@login_required
def add_feedback(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.product = product
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('product_detail', product_id=product.id)
    else:
        form = FeedbackForm()
    return render(request, 'app/add_feedback.html', {'form': form, 'product': product})

def forum(request, room_id=None):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    posts = ForumPost.objects.filter(
        Q(title__icontains=q)|
        Q(content__icontains = q) 
        )

    topics = ForumTopic.objects.all()

    if room_id:
        room_posts = ForumPost.objects.filter(room_id=id)
        context = {'posts': room_posts, 'topics': topics, 'selected_room_id': room_id}
    else:
        context = {'posts': posts, 'topics': topics}

    context = {'posts': posts, 'topics':topics}
    
    return render(request, 'app/forum.html', context)

def forum_room(request, pk):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    

    discuss = ForumPost.objects.get(id=pk)

    topics = ForumTopic.objects.all()


    context = {'discuss':discuss, 'topics':topics}
    
    
    return render(request, 'app/forum_room.html', context)

@login_required
def add_forum_post(request):
    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('forum')
    else:
        form = ForumPostForm()
    return render(request, 'app/add_forum_post.html', {'form': form})

@login_required
def add_forum_comment(request, post_id):
    post = get_object_or_404(ForumPost, pk=post_id)
    if request.method == 'POST':
        form = ForumCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('forum')
    else:
        form = ForumCommentForm()
    return render(request, 'app/add_forum_comment.html', {'form': form, 'post': post})

def forum_post_detail(request, post_id):
    post = get_object_or_404(ForumPost, pk=post_id)
    return render(request, 'forum_post_detail.html', {'post': post})

@login_required
def user_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'app/user_profile.html', {'form': form, 'user_profile': user_profile})

@login_required
def add_feedback(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.product = product
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('product_detail', product_id=product.id)
    else:
        form = FeedbackForm()
    return render(request, 'app/add_feedback.html', {'form': form, 'product': product})

@login_required
def create_advertisement(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Advertisement created successfully.')
            return redirect('advertisement_list')
    else:
        form = AdvertisementForm()
    return render(request, 'app/create_advertisement.html', {'form': form})

def advertisement_list(request):
    advertisements = Advertisement.objects.all()
    return render(request, 'app/advertisement_list.html', {'advertisements': advertisements})