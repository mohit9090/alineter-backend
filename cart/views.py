from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Models
from cart.models import TestProduct, ProductCart

# Decorators
from accounts.decorators import only_authenticated_user
from cookie.decorators import check_login_cookie


from django.contrib.auth import get_user_model
User = get_user_model()


@check_login_cookie
@only_authenticated_user
def cart(request):
	return render(request, 'cart/cart.html')


@only_authenticated_user
def fetch_cart(request):
	result = {}
	if request.method == 'GET':
		try:
			# # -- FOR TEST --
			# u = User.objects.get(email='trial132@gmail.com')
			# items = ProductCart.objects.filter(user=u)

			items = ProductCart.objects.filter(user=request.user)
		except ProductCart.DoesNotExist:
			result['success'] = False
			result['message'] = 'The Cart for this user Doesn\'t exists'
			return JsonResponse(result, safe=False)
		else:
			data = []
			result['success'] = True
			result['message'] = 'Cart fetched successfully'
			result['data'] = data
			
			if not len(items):
				return JsonResponse(result, safe=False)

			for item in items:
				cart = {}
				product = {}
				price = {}
				
				product['id'] = item.product.id 
				product['name'] = item.product.product_name
				product['img'] = item.product.product_img.url
				
				price['original_price'] = item.product.product_price 
				price['selling_price'] = item.product.product_sellprice
				price['discount'] = item.product.product_discount
				
				product['price'] = price
				cart['product'] = product
				cart['quantity'] = item.quantity 

				data.append(cart)

			result['data'] = data
			return JsonResponse(result, safe=False)

	result['success'] = False
	result['message'] = 'Allowed GET request only'
	return JsonResponse(result, safe=False)


@only_authenticated_user
def update_quantity(request):
	if request.POST:
		result = {}
		pid, quantity = request.POST.get('product_id'), request.POST.get('quantity')
		try:
			product = TestProduct.objects.get(id=pid)
		except TestProduct.DoesNotExist:
			result['success'] = False
			result['message'] = f'Product with id, {pid} doesnot exists'
		else:
			try:
				user_product_cart = ProductCart.objects.get(user=request.user, product=product)
			except ProductCart.DoesNotExist:
				result['success'] = False
				result['message'] = f'Sorry, This product is not available in cart'
			else:
				user_product_cart.quantity = quantity
				user_product_cart.save()
				result['success'] = True
				result['message'] = 'Successfully updated quantity of product in cart'
		return JsonResponse(result, safe=False)
	return HttpResponse("You are not allowed to access this page")

