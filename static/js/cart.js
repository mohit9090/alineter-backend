
const cartContainer = document.querySelector('.cart--div');
const cartHeading = cartContainer.querySelector('.heading--div');
const cartList = cartContainer.querySelector('.cart--list');

const checkoutContainer = document.querySelector('.checkout-container > .checkout--div');
const checkoutTotalPrice = checkoutContainer.querySelector('.price--item_total > .price--item_value');
const checkoutDiscount = checkoutContainer.querySelector('.price--item_discount > .price--item_value');
const checkoutShipping = checkoutContainer.querySelector('.price--item_shipping > .price--item_value')
const checkoutNetPrice = checkoutContainer.querySelector('.price--item_net > .price--item_value');
const checkoutNetDiscount = checkoutContainer.querySelector('.price--item_net .price--item_discount');

let SHIPPING_CHARGE = 30; // Default

// Format Price (Ex- 23 to 23.00)
const formatPrice = price => price.toFixed(2).toString();

const clearMarkup = function(elem) {
	elem.innerHTML = '';
}

const insertMarkup = function(elem, markup) {
	if (!elem) return;

	clearMarkup(elem)
	elem.insertAdjacentHTML('beforeend', markup);
}

const renderSpinner = function(elem) {
	if (!elem) return;

	const markup = `
		<div class="w-100" style="transform:scale(0.5);-webkit-transform:scale(0.5)">
        	<div class="spinner">
          		<div class="cube cube-1"></div>
          		<div class="cube cube-2"></div>
        	</div>
     	</div>
	`;
	insertMarkup(elem, markup);
}

const renderError = function(elem, error='Something Went Wrong') {
	if (!elem) return;

	const markup = `
		<div>
			<p>${error}</p>
		</div>
	`;
	insertMarkup(elem, markup);
}

const calcTotalObj = function(items) {
	if (!items.length) return;

	const total = {
		originalPrice: 0,
		sellingPrice: 0,
		discount: 0
	};

	// Update total Object
	items.reduce( (tot, item) => {
		tot.originalPrice += item.original_price;
		tot.sellingPrice += item.selling_price;
		tot.discount += item.original_price - item.selling_price;
		return tot;
	}, total);

	total.netPrice = total.sellingPrice + SHIPPING_CHARGE;
	total.netDiscount = +formatPrice((total.originalPrice - total.sellingPrice) / total.originalPrice * 100) || 0;

	return total;
}

const renderCheckout = function(items) {

	const total = calcTotalObj(items);

	if (!total) return renderError(checkoutContainer, 'Please add Items for checkout.');

	const markup = `
		<div class="heading--div">
      <h6 class="heading">Order summary</h6>
    </div>
    
    <div class="price--div">
      <ul class="list price--list">
        <li class="list-item price--item price--item_total">
          <span class="price--item_name">Total</span>
          <span class="price--item_value inr">${formatPrice(total.originalPrice)}</span>
        </li>
        <li class="list-item price--item price--item_discount">
          <span class="price--item_name">Discount</span>
          <span class="price--item_value inr discount">${formatPrice(total.discount)}</span>
        </li>
        <li class="list-item price--item price--item_shipping">
          <span class="price--item_name">Shipping</span>
          <span class="price--item_value inr">${formatPrice(SHIPPING_CHARGE)}</span>
        </li>
        <li class="list-item price--item price--item_net">
          <span class="price--item_name">Net Total<span class="badge badge-warning ml-2 price--item_discount">Saved ${formatPrice(total.netDiscount)}%</span></span>
          <span class="price--item_value inr">${formatPrice(total.netPrice)}</span>
        </li>
      </ul>
    </div>

    <div class="checkout--btn--div">
      <button type="button" class="btn btn-i-primary w-100 checkout-btn">
        <div class="d-flex justify-content-center">
          <span>Checkout</span>
        </div>
      </button>
    </div>

    <div class="promocode--div">
      <div class="heading--div">
        <h6 class="heading">Promotional Code</h6>
      </div>
      <div class="promocode-applied--div">
        <ul class="list promocode--list">
          <li class="list-item promocode--item d-flex">
            <button class="btn cancel-code-btn">&times;</button>
            <span class="promocode align-self-center">dsgfudsy7832vwq81</span>
          </li>
          <li class="list-item promocode--item d-flex">
            <button class="btn cancel-code-btn">&times;</button>
            <span class="promocode align-self-center">77wgfudsy7832vwasd</span>
          </li>
        </ul>
      </div>

      <div class="promocode--form">
        <div class="input-group">
          <input type="text" class="form-control coupon-code--input" name="coupon-code"spellcheck="false" placeholder="Enter Coupon Code">
           <div class="input-group-append">
             <button type="button" class="btn btn-i-primary apply-code-btn">
              <div class="d-flex justify-content-center">
                <span>Apply</span>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
	`;

	insertMarkup(checkoutContainer, markup);
	
}

const renderCart = function(data) {
	/* Markup for Cart heading */
	let markup = `
		<h6 class="heading">${data.length} items in cart</h6>
	`;
	insertMarkup(cartHeading, markup);

	/* Markup for Cart items */
	markup = '';
	const productPrice = [];

	data.forEach(item => {
		const { product } = item;
		productPrice.push(product.price);

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
              <span class="price-new inr">${formatPrice(product.price.selling_price)}</span>
              <span class="price-original inr">${formatPrice(product.price.original_price)}</span>
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
	});
	insertMarkup(cartList, markup);

	// Render Checkout
	renderCheckout(productPrice);
}

const fetchCart = function(url) {

	$.ajax({
		url: url,
		type: 'GET',
		complete: function(data) {
			const response = data.responseJSON;
			
			// responseData is undefined
			if (!response) 
				return renderError(cartList)

			// fetch was unsuccessfull
			if (!response.success)
				return renderError(cartList, response.message)

			// cart is empty
			if (!response.data.length)
				return renderError(cartList, 'Your Cart is empty. SHOP NOW')

			renderCart(response.data)
		}
	})
}

const handleLoadEvent = function() {
	window.addEventListener('load', function() {
		const fetchCartURL = '/cart/fetch-cart/';
		fetchCart(fetchCartURL);
	})	
}

const init = function() {
	renderSpinner(cartList);
	renderSpinner(checkoutContainer);
	handleLoadEvent();
}
init();
