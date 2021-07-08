const faqContainer = document.querySelector('.all-faqs');

const faqs = [
	{
		question: 'How will I know that my order is placed?',
		answer: `As soon as you place the order you’ll receive a confirmation mail saying that your order is placed. If you've not received your mail within the next five minutes of placing the order then probably your order is not placed.`
	},
	{
		question: 'How will I know if my product is outbound to arrive today?',
		answer: `Time is precious; therefore we all like to keep things planned. Hence, we won’t ruin your schedule. You will receive a notification from us on the day of the delivery of your order to keep you informed.`
	},
	{
		question: 'When will I receive my order?',
		answer: `You must be really excited to flaunt your new look and make others jealous. And the wait isn’t any long either. It will take us maximum of 5-6 days to hand you your ordered clothes.`
	},
	{
		question: 'What are the payment options?',
		answer: `Enter your answer here. Be thoughtful, write clearly and concisely, and consider adding written as well as visual examples. Go over what you’ve written to make sure that if it was the first time you were visiting the site, you’d understand your answer.`
	},
	{
		question: 'Are my personal details safe?',
		answer: `Privacy is a concern for each one of us. We have got your data all secured with data encryption, and our SSL certification helps us do that. So, you can sit back, relax and order your favorite clothes from Alineter.`
	},
	{
		question: 'What if my order is delayed?',
		answer: `It’s highly unlikely that your order will be delayed. Generally the delivery time of an order is around 5-6 days. But even if it is late then please give it a day more. If the order still does not arrive then reach us at <a href="mailto:support@alineter.com" >support@alineter.com</a> or call us at <a href="tel:8895738760" >+91 8895738760</a>.`
	},
	{
		question: 'What is your return policy?',
		answer: `Enter your answer here. Be thoughtful, write clearly and concisely, and consider adding written as well as visual examples. Go over what you’ve written to make sure that if it was the first time you were visiting the site, you’d understand your answer.`
	},
	{
		question: 'When will I receive my refund?',
		answer: `Customers are always our first priority. After you’ve applied for a return and we’ve confirmed your request; we will automatically initiate your refund. If you’ve paid from your bank account or any online payment methods then you will receive your refund amount within 5-6 working days. If you’ve paid for the order through COD method, then one of our delivery men will come to your given address to return the paid amount. (Check the Returns Policy for complete details)
            If the amount isn’t back to you within the aforesaid days, then contact us at <a href="mailto:support@alineter.com" >support@alineter.com</a> or give a call on <a href="tel:8895738760" >+91 8895738760</a>.`
	},
	{
		question: 'Why is there no COD?',
		answer: `We totally get you that Cash on Delivery is by far the most popular payment method. But for the past months Covid-19 has made it difficult. We are putting your health as our utmost priority; hence, not accepting physical payments to avoid the spreading of virus. And on the bright side, this supports our initiative for a digital India.`
	},
];



const renderFaq = function(faqs) {
	let faq_html = '';

	faqs.forEach( faq => {
		faq_html += `
			<div class="faq-wrapper faq">
	          <div class="policy-head--s2 question reveal__from-bottom">
	            <h1>${faq.question}</h1>
	          </div>
	          <div class="policy-body answer reveal__from-bottom">
	            <p>${faq.answer}</p>
	          </div>
	        </div>
	    `
	});

	faqContainer.insertAdjacentHTML('beforeend', faq_html);

}

const renderError = function(elem, err) {
	elem.style.fontSize = '0.7rem';
	elem.style.color = 'white';
	faqContainer.insertAdjacentHTML('beforeend', err);
}


const fetchFaq = function(url) {	
	renderFaq(faqs); // Default FAQs

	$.ajax({
		url: url,
		type: 'POST',
		data: {
			'csrfmiddlewaretoken': csrftoken
		},
		complete:function(data) {
			const responseData = data.responseJSON;
			responseData ? renderFaq(responseData) : renderError(faqContainer, 'Problem Fetching More FAQs')
		}
	})
};

window.addEventListener('load', function() {
	csrftoken = getCookie('csrftoken');

	const fetchFaqURL = '/company/fetch-faq/';
	fetchFaq(fetchFaqURL);
})