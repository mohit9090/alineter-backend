
const cartContainer = document.querySelector('.cart--div');
const cartHeading = cartContainer.querySelector('.heading--div');
const cartList = cartContainer.querySelector('.cart--list');

const clearMarkup = function(elem) {
	elem.innerHTML = '';
}

const insertMarkup = function(elem, markup) {
	if (elem) {
		clearMarkup(elem)
		elem.insertAdjacentHTML('beforeend', markup);
	}
}

const renderSpinner = function() {
	const markup = `
		<div class="w-100" style="transform:scale(0.5);-webkit-transform:scale(0.5)">
        	<div class="spinner">
          		<div class="cube cube-1"></div>
          		<div class="cube cube-2"></div>
        	</div>
     	</div>
	`;
	insertMarkup(cartList, markup);
}

const renderError = function(error='Something Went Wrong') {
	const markup = `
		<div>
			<p>${error}</p>
		</div>
	`;
	insertMarkup(cartList, markup);
}

const renderCart = function(data) {
	/* Markup for Cart heading */
	let markup = `
		<h6 class="heading">${data.length} items in cart</h6>
	`;
	insertMarkup(cartHeading, markup);

	/* Markup for Cart items */
	markup = '';
	data.forEach(item => {
		const { product } = item;
		markup += `
			<li class="list-item cart--item row ml-0 mr-0" data-product-id=${product.id}>
                <div class="item-img--wrapper col-3 border-right">
                  <div class="item-img--div cy position-relative">
                    <a href="#product">
                    	<img src="${product.img}" class="item-img img-contain" alt="${product.name}">
                    </a>
                  </div>
                </div>
                
                <div class="item-detail--wrapper col-7">
                  <div class="item-detail d-flex flex-column text-left">
                    <a href="#product" class="item-name">${product.name}</a>
                    <span class="item-price">
                      <span class="price-tag">Price:</span>
                      <span class="price-new inr">${product.price.selling_price}</span>
                      <span class="price-original inr">${product.price.original_price}</span>
                      <span class="badge badge-dark">${product.price.discount}% off</span>
                    </span>
                  </div>
                  <div class="item-quantity d-flex flex-wrap text-left">
                    <span class="heading">Quantity:</span>
                    <div class="item-quantity-counter d-flex">
                      <button class="btn count--btn upcount"><span class="fa fa-caret-down"></span></button>
                      <span class="display align-self-center">${item.quantity}</span>
                      <button class="btn count--btn downcount"><span class="fa fa-caret-up"></span></button>
                    </div>
                  </div>
                  <div class="item-link--div d-flex flex-wrap text-left">
                    <a href="#remove" class="item-link remove">Remove Item</a>
                  </div>
                </div>
                
                <div class="item-checkout--wrapper col-2 border-left">
                  <div class="add-for-checkout position-relative cy">
                    <small class="font-weight-bold">ADD</small>
                    <input type="checkbox" name="" checked>
                  </div>
                </div>
            </li>
		`;

		insertMarkup(cartList, markup);
	})
}

const fetchCart = function(url) {
	renderSpinner();

	$.ajax({
		url: url,
		type: 'GET',
		complete: function(data) {
			const response = data.responseJSON;
			
			// responseData is undefined
			if (!response) 
				return renderError()

			// fetch was unsuccessfull
			if (!response.success)
				return renderError(response.message)

			// cart is empty
			if (!response.data.length)
				return renderError('Your Cart is empty. SHOP NOW')

			renderCart(response.data)
		}
	})
}


window.addEventListener('load', function() {
	const fetchCartURL = '/cart/fetch-cart/';
	fetchCart(fetchCartURL);
})