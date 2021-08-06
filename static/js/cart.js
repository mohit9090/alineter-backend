
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
const productDataForCheckout = [];

const freezeBody = function() {
	document.body.style.pointerEvents = 'none';
}
const unfreezeBody = function() {
	document.body.style.pointerEvents = 'auto';
}

/* Format Price (Ex- 23 to 23.00) */
const formatPrice = price => price.toFixed(2).toString();

/* Get product index using products id */
const getProductIndexById = pid => productDataForCheckout.findIndex(product => product.id.toString() === pid);

/* Insert Data for checkout */
const insertProductDataForCheckout = function(item) {
	if (!item) return;

	const { product : { id, price } , quantity } = item;
	const addForCheckout = true; // Default is true when page loads

	productDataForCheckout.push({
		id, 
		price,
		quantity,
		checkout: addForCheckout
	});
}

/* Calculate total price for checkout */
const calcTotalObj = function(items) {
	/* Structure of items
		items : [
			[
				{
					original_price: 243,
					...
				},
				2 # Referes to quantity
			]
		]
	*/
	/* if items are empty */
	if (!items.length) return;

	const multiplyQuantity = (oPrice, sPrice, q) => {
		return [
			oPrice * q,
			sPrice * q
		]
	}

	const total = {
		originalPrice: 0,
		sellingPrice: 0,
		discount: 0
	};

	// Update total Object
	items.reduce( (tot, item) => {
		const [ price, quantity ] = item;
		const [ origPrice, sellPrice ] = multiplyQuantity(price.original_price, price.selling_price, quantity)

		tot.originalPrice += origPrice;
		tot.sellingPrice += sellPrice;
		tot.discount += origPrice - sellPrice;
		return tot;
	}, total);

	total.netPrice = total.sellingPrice + SHIPPING_CHARGE;
	total.netDiscount = +formatPrice((total.originalPrice - total.sellingPrice) / total.originalPrice * 100) || 0;

	return total;
};

/* Filter Product data based on some condition and return required fields for checkout */
/* CONDITION: product.checkout should be true,
	 Fields Required are products price and quantity */
const filterProductForCheckout = products => {
	return products
		.filter(product => product.checkout === true)
		.map(product => [product.price, product.quantity]);
}

/* Add product for checkout process */
const addProductToCheckout = function(pid) {
	const productIndex = getProductIndexById(pid);
	if (productIndex === -1) return;

	productDataForCheckout[productIndex].checkout = true;

	if (!productDataForCheckout[productIndex].quantity) {
		// if product is added for checkout but quantity of product is zero	
		updateQuantity(
			document.querySelector(`.item-quantity-counter[data-product-id="${pid}"]`), 
			pid,
			1
		);
		return;
	}

	renderCheckout(productDataForCheckout);
};

/* Remove product from checkout process */
const removeProductFromCheckout = function(pid) {
	const productIndex = getProductIndexById(pid);
	if (productIndex === -1) return;

	productDataForCheckout[productIndex].checkout = false;
	renderCheckout(productDataForCheckout);
}

/* Clear the markup */
const clearMarkup = function(elem) {
	elem.innerHTML = '';
}

/* Insert Markup in given element */
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

const renderCheckout = function(items) {
	const checkoutFilter = filterProductForCheckout(items);
	const total = calcTotalObj(checkoutFilter);

	if (!total) {
		renderError(checkoutContainer, 'Please add Items for checkout.');
		return;
	}

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
};

const renderCart = function(data) {
	/* Markup for Cart heading */
	let markup = `
		<h6 class="heading">${data.length} items in cart</h6>
	`;
	insertMarkup(cartHeading, markup);

	/* Markup for Cart items */
	markup = '';

	data.forEach(item => {
		const { product, quantity } = item;
		insertProductDataForCheckout(item);

		markup += `
			<li class="list-item cart--item row ml-0 mr-0" data-product-id="${product.id}">
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
            <div class="item-quantity-counter d-flex" data-product-id="${product.id}">
              <button class="btn count--btn downcount" data-next="${quantity - 1}"><span class="fa fa-caret-down"></span></button>
              <span class="display align-self-center">${quantity}</span>
              <button class="btn count--btn upcount" data-next="${quantity + 1}"><span class="fa fa-caret-up"></span></button>
            </div>
          </div>
          <div class="item-link--div d-flex flex-wrap text-left">
            <a href="#remove" class="item-link remove">Remove Item</a>
          </div>
        </div>
        
        <div class="item-checkout--wrapper col-2 border-left">
          <div class="add-for-checkout position-relative cy">
            <small class="font-weight-bold">ADD</small>
            <input type="checkbox" ${quantity ? 'checked': ''} data-product-id="${product.id}">
          </div>
        </div>
    	</li>
		`;
	});
	insertMarkup(cartList, markup);

	// Render Checkout
	renderCheckout(productDataForCheckout);
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
};



const updateQuantity = function(elem, productId, newQuantity) {
	freezeBody()

	// update cart model
	const csrftoken = getCookie('csrftoken');
	$.ajax({
		url: '/cart/update/quantity/',
		type: 'POST',
		data: {
			'csrfmiddlewaretoken': csrftoken,
			'product_id': productId,
			'quantity': newQuantity
		},
		complete: function(data) {
			if (data.responseJSON.success) {
				// Update checkbox
				document
					.querySelector(`input[type="checkbox"][data-product-id="${productId}"]`)
					.checked = newQuantity ? true : false;

				// Update Product data
				const productData = productDataForCheckout.find(product => product.id === +productId);
				productData.quantity = newQuantity;
				productData.checkout = newQuantity ? true : false;

				// Update cart quantity display
				elem.querySelector('.display').textContent = productData.quantity;
				elem.querySelector('.upcount').dataset.next = productData.quantity + 1;
				elem.querySelector('.downcount').dataset.next = productData.quantity - 1;

				// Render checkout
				renderCheckout(productDataForCheckout);
			}

		}
	});

	unfreezeBody();
}

const handleClickEvent = function() {
	/* Handle click event on cart list */
	cartList.addEventListener('click', function(e) {
		const elem = e.target;
		const checkbox = elem.closest('input[type="checkbox"]'); // CheckBox
		const countBtn = elem.closest('.count--btn'); // Counter Button

		if (!checkbox && !countBtn) return;

		if (checkbox) {
			/* Add-Remove Items from checkout */
			const productID = checkbox.dataset.productId;
			return (checkbox.checked)
				?	addProductToCheckout(productID)
				: removeProductFromCheckout(productID);
		}

		if (countBtn) {
			/* Increase quantity of products */
			const parentElem = countBtn.closest('.item-quantity-counter');
			const productID = +parentElem.dataset.productId;
			const updateToQuantity = +countBtn.dataset.next;
			
			if (isNaN(updateToQuantity) || updateToQuantity < 0) return;

			// Update quantity display and model
			updateQuantity(parentElem, productID, updateToQuantity);
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
	handleClickEvent();
}
init();
