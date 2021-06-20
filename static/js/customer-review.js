
const reviewsContainer = document.querySelector("#reviews-container .row");
const showMoreBtn = document.querySelector(".show-more-btn--div");

const moreReviewOverlayElem = document.getElementById("more-reviews-overlay");
const reviewsNavElem = document.querySelector(".reviews-nav");
const moreReviewsContainer = document.getElementById("more-reviews-container");
const moreReviewsContainer__row = document.querySelector("#more-reviews-container > .row");



// For setting the data for jsonReviews
let jsonReviewers;
function setReviewsData(responseData) {
	jsonReviewers = responseData;
}

/////////////////////////////////////////////////////////////////////////////////////////
/* ---------------------------- RENDERING RESPONSE ----------------------------------- */
/////////////////////////////////////////////////////////////////////////////////////////


function renderResponse() {

	var reviewers = jsonReviewers
	
	/* Actual number of reviews */
	const totalReviews = reviewers.length;


	/* Get At most 6 reviews, PS: Dont make it more than 6 */
	const max_reviews = 6;
	reviewers.splice(max_reviews, reviewers.length-max_reviews);


	/* Reviewers array is sorted by the length of review content in ascending order */
	reviewers.sort( function(a, b) {
		return sortbyLength(a, b, 0);
	});


	/*
		map smallest element with largest and store it
		order = [1, 2, 3, 4, 5, 6]
		reoder = [1, 6, 2, 5, 3, 4]
	*/
	const reorder_reviewers = [];
	for(i=0, j=reviewers.length-1; i<reviewers.length, j>=0; i++, j--) {
		if(i > j) {
			break;
		} else {
			if(i == j) {
				/* Both refers the same element so push it once */
				reorder_reviewers.push(reviewers[i])
			} else {
				/* Both refers two different element so push both of them */
				reorder_reviewers.push(reviewers[i]);
				reorder_reviewers.push(reviewers[j]);
			}
		}
	}

	/* Reassign reviewers to reorder_reviewers */
	reviewers = reorder_reviewers;


	const header = [
		// Header Selection
		/*
		   if only 1,2 or 3 reviews are there 
		*/
		`
		<div class="col-12 col-reviews">
			<div class="d-flex flex-column p-0">
		`,
		/*
		   if only 4 reviews are there 
		*/

		`
		<div class="col-lg-6 col-md-6 col-sm-12 col-reviews">
			<div class="d-flex flex-column">
		`,
		/*
		   if only 5 or 6 reviews are there 
		*/

		`
		<div class="col-lg-4 col-md-6 col-sm-12 col-reviews">
			<div class="d-flex flex-column flex-grow">
		`,

	];

	const footer = [
		`
			</div>
		</div>
		`
	];


	//Destructuring Header
	const [open_div_1, open_div_2, open_div_3] = header;

	//Destructuring Footer
	const [close_div] = footer;

	//Destructuring Reviewers
	const [firstReviewer, secondReviewer, thirdReviewer, fourthReviewer, fifthReviewer, sixthReviewer] = reviewers;

	// NOTE: addRatingStar() is defined in utility.js

	function mapReviews(rev_set, additional_class) {
		let reviews = ""
		rev_set.forEach( reviewer => {
			if(reviewer !== null && reviewer !== undefined) {
				reviews = reviews + `<div class="review-box rounded ${additional_class}">
	            <div class="card review-card border-0">
	              <div class="card-header">
	                <div class="d-flex justify-content-between">
	                  <div class="d-flex flex-column">
	                    <small class="reviewer-name">${reviewer.name}</small>
	                    <div class="d-flex">` + 
	                    
	                    addRatingStar(reviewer.review.rating)

	                     + `</div>
	                  </div>
	                  <div class="reviewer-pic-wrapper">
	                    <img src="${reviewer.img}" class="reviewer-pic rounded-circle" width=50 height=50/>
	                  </div>
	                </div>
	              </div>
	              <div class="card-body">
	                <p class="card-text text-cultured reviewer-says">${reviewer.review.content}</p>
	              </div>
	            </div>
	          </div>`
			}
		});

		return reviews;
	}

	function recursiveMapping(set, times, open_div) {
		let reviewsHTML = ""; 

		for(var i=0; i<times; i++) {
			let reviews = mapReviews(set[i], "w-100");
			reviewsHTML = reviewsHTML + open_div + reviews + close_div;	
		};

		reviewsContainer.innerHTML = reviewsHTML;
	}

	function constructReviews(numOfReviews) {
		if(numOfReviews == 1 || numOfReviews == 2 || numOfReviews == 3) {
			/*
				Map All Reviews to a string reviews
			*/
			let reviews = mapReviews(reviewers, "normal-wrapper");
			/*
				Display the string reviews in the markup document
			*/

			// setTimeout(function() {
			// 	reviewsContainer.innerHTML = open_div_1 + reviews + close_div;
			// },5000);
			reviewsContainer.innerHTML = open_div_1 + reviews + close_div;

		} else if(numOfReviews == 4) {
			/* 
				Four reviews will be divided into two sets
			*/
			let firstSet = [], secondSet = [];
			
			firstSet.push(firstReviewer, secondReviewer);
			secondSet.push(thirdReviewer, fourthReviewer);

			let set = [firstSet, secondSet];
			/*
				Recursively map the sets to add reviews
			*/
			recursiveMapping(set, set.length, open_div_2);
			
		} else if(numOfReviews > 4) {
			/* 
				Six reviews will be divided into three sets
			*/
			let firstSet = [], secondSet = [], thirdSet = [];
			
			firstSet.push(firstReviewer, secondReviewer);
			secondSet.push(thirdReviewer, fourthReviewer);
			thirdSet.push(fifthReviewer, sixthReviewer);

			let set = [firstSet, secondSet, thirdSet];

			recursiveMapping(set, set.length, open_div_3);

		} else {
			/*
				No Reviewers are there i.e. numOfReviews = 0
			*/
			document.getElementById("testimonial").innerHTML = `<div class="no-reviewer-wrapper text-center">
	            <h3 class="txt-light">There are no Reviews</h3>
	            <p class="lead txt-primary">Be the FIRST One to </p>
	            <a href="{% url 'company:write_about_us' %}" class="btn show-more-btn reveal__from-bottom"><span class="fa fa-pencil"></span>&nbsp;&nbsp;Write About Us</a>
	          </div>`;
		}
	}

	function buildShowMoreBtn() {
		if(reviewers.length >= 4) {
			showMoreBtn.innerHTML = `<a href="javascript:void(0)" class="btn show-more-btn reveal__from-bottom" onclick="show_more__Reviews()">Show More</a>`;
		} else {
			showMoreBtn.innerHTML = "";
		}
	}

	function displayReviews() {
		/* Number of Reviews that are actually shown */
		var shownReviews = reviewers.length;

		// Loading animation before Testimonial Loads
		reviewsContainer.innerHTML = `
	    <div class="w-100 cube-spinner-md">
	      <div class="spinner">
	        <div class="cube cube-1"></div>
	        <div class="cube cube-2" style="background-color:#FEFEFE"></div>
	      </div>
	    </div> 
		`;
		
		showMoreBtn.innerHTML = `
	    <div class="w-100 cube-spinner-md">
	      <div class="spinner">
	        <div class="cube cube-1"></div>
	        <div class="cube cube-2" style="background-color:#FEFEFE"></div>
	      </div>
	    </div> 
		`;

		constructReviews(shownReviews);
		buildShowMoreBtn();
	}

	displayReviews();
}




////////////////////////////////////////////////////////////////////////////////////////////
/* ---------------------------------- SHOW MORE REVIEWS --------------------------------- */
////////////////////////////////////////////////////////////////////////////////////////////


function sortbyLength(a, b, type) {
	/*
		type = 0 --> Ascending Order
		type = 1 --> Descending Order

		Arrange the Customer Reviews according to the review content length,
		that may be ascending or desceneding
	*/
	if(a.review.content.length < b.review.content.length) {
		/*
			type === 0 then second statement will execute
			type === 1 then first statement will execute 
			Here for ascending(type=0) it should return -1,
			and for descending(type=1) it should return 1
		*/
		return type ? 1 : -1;
	}
	if(a.review.content.length > b.review.content.length) {
		/*
			Here for ascending(type=0) it should return 1,
			and for descending(type=1) it should return -1
		*/
		return type ? -1 : 1;
	}
	return 0;
}



function toggleReviewOverlay(toggle_state) {
	/*
		toggle_state = 1 (true) => Show
		toggle_state = 0 (false) => Hide
	*/

	moreReviewOverlayElem.style.width = (toggle_state) ? "100%" : "0";
	
	//Restrict the body to scroll when overlay effect is turned on
	document.body.style.overflowY = (toggle_state) ? "hidden" : "auto";
}

function toggleReviewContent(toggle_state) {
	/*
		toggle_state = 1 (true) => Show
		toggle_state = 0 (false) => Hide
	*/

	const elems = [reviewsNavElem, moreReviewsContainer];
	elems.forEach( elem => {
		elem.style.opacity = (toggle_state) ? "1" : "0";
	});

	//Enable Scrolling of Review Content when it has been displayed
	moreReviewOverlayElem.style.overflowY = (toggle_state) ? "auto" : "hidden";
}

function mapOverlayReviews(all_reviewers) {
	let moreReviews_div = "";

	all_reviewers.forEach(reviewer => {
		moreReviews_div += `<div class="col-lg-4 col-md-6 col-sm-12"><div class="review-box rounded">
            <div class="card review-card border rounded">
              <div class="card-header">
                <div class="d-flex justify-content-between">
                  <div class="d-flex flex-column">
                    <small class="reviewer-name">${reviewer.name}</small>
                    <div class="d-flex">` + 
                    
                    addRatingStar(reviewer.review.rating)

                     + `</div>
                  </div>
                  <div class="reviewer-pic-wrapper">
                    <img src="${reviewer.img}" class="reviewer-pic rounded-circle" width=50 height=50/>
                  </div>
                </div>
              </div>
              <div class="card-body rounded">
                <p class="card-text text-cultured reviewer-says">${reviewer.review.content}</p>
              </div>
            </div>
          </div>
         </div>`
	});

	return moreReviews_div;
}

let toggle_state;

function show_more__Reviews() {
	/*
		Opens the Overlay to show More Reviews By Customer
		toggle_state = 1 means to show 
	*/
	toggle_state = 1;
	toggleReviewOverlay(toggle_state);

	const all_reviewers = jsonReviewers;

	all_reviewers.sort( function(a, b) {
		return sortbyLength(a, b, 1);
	});


	// Loading animation before Testimonial Loads
	moreReviewsContainer__row.innerHTML = `
    <div class="w-100" style="height:100vh">
      <div class="spinner" style="left:50%;top:35%;transform:translate(-50%,-50%);-webkit-transform:translate(-50%,-50%)">
        <div class="cube cube-1"></div>
        <div class="cube cube-2" style="background-color:#FEFEFE"></div>
      </div>
    </div> 
  `;

	let moreReviews_html = ""
	moreReviews_html = mapOverlayReviews(all_reviewers);

	moreReviewsContainer__row.innerHTML = moreReviews_html;

	setTimeout(function() {
		toggleReviewContent(toggle_state);
	}, 300);

}

function close_more__Reviews() {
	/*
		Close the Overlay to hide More Reviews By Customer
		toggle_state = 0 means to hide 
	*/
	toggle_state = 0;
	toggleReviewContent(toggle_state);

	setTimeout(function() {
		toggleReviewOverlay(toggle_state);
	}, 300);
}



const fetchReviews = function(url) {

	csrftoken = getCookie('csrftoken');

	$.ajax({
		url: url,
		type: 'POST',
		data: {
			'csrfmiddlewaretoken': csrftoken
		},
		complete:function(data) {
			const responseData = data.responseJSON;
			setReviewsData(responseData);
			renderResponse();
		}
	})

}

window.addEventListener('load', function() {
	const url = '/company_reviews/';
	fetchReviews(url);
});



