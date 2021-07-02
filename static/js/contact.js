
const contactForm = document.querySelector('#contact-us-form')
const contactBtn = document.querySelector('.contact-btn');
const contactBtnDiv = document.querySelector('#contact-btn--div');

function validate_contactpage() {
	const fulfilledFields = document.querySelectorAll(".user-input[data-fulfill='true']");
	const allRequiredFields = document.querySelectorAll("#contact-us-form .user-input[required]");

	//loader before submitting or rejecting the form
  	contactBtnDiv.innerHTML += `<div class="spinner-border text-light spinner-border-sm my-auto ml-2"></div>`;

  	if (fulfilledFields.length === allRequiredFields.length) {
		setTimeout(function(){
      		contactForm.submit();
    	}, 700);
  	} else {
  		setTimeout(function() {
  			contactBtnDiv.innerHTML = '<span>Submit</span>' ;
  			slideUp();
  			return false;
  		}, 400)
  	}
}
