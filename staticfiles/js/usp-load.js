  

const uspContainer = document.getElementById("usp-wrapper")

//jsonUSP is derived from js/usp-data.js
const usp_icons = JSON.parse(jsonUSP)


const [run_man, truck, cotton_fabric, india, personalised] = usp_icons;

const uspList = [
  {
    icon:run_man,
    tag:'All Moment Ready',
    textColor:'text-blue'
  },
  {
    icon:truck,
    tag:'Free shipping of all products',
    textColor:''
  },
  {
    icon:cotton_fabric,
    tag:'Moisturised cotton fabric',
    textColor:''
  },
  {
    icon:india,
    tag:'Made in India',
    textColor:''
  },
  {
    icon:personalised,
    tag:'Personalised modern designs',
    textColor:''
  }
];



function mapUSP(uspList) {
  let usp_div = "";

  uspList.forEach( usp => {
    usp_div += `<div class="card text-center usp-box reveal__from-bottom mx-auto ${detectMob() ? 'mobile-device' : '' }" onclick="animateIcon(this)">
      <div class="card-body">
        <div class="my-auto">
          <div class="mx-auto icon-filler">
            <!--icon-->
            ${usp.icon}
          </div><br>
          <small class="txt-primary usp-tag">${usp.tag}</small>
        </div>
      </div>
    </div>`;
  });

  return usp_div;
};



function getUSP_DIV() {
  let uspIconsElem = document.querySelectorAll(".usp-box");
  
  /* 
    Opening Object into Array List using Spread Operator and returning it
  */
  return [...uspIconsElem];
}

function animateIcon(icon) {
  /*
    Animate Icons on clicking them and remove animation after some specific interval
  */
  let uspIcons = getUSP_DIV();
  
  /*If "clicked" class is already there them remove it first */
  uspIcons.forEach(u_icon => {
    if(classContains(u_icon, "clicked")) {
      removeClass(u_icon, ["clicked"]);
    }
  });

  addClass(icon, ["clicked"])
  setTimeout(function() {
    removeClass(icon, ["clicked"]);
  }, 700);
};  


function constructUSP() {
  let usp_html;

  // Loading animation before USP Loads
  uspContainer.innerHTML = `
      <div class="w-100 cube-spinner-md">
        <div class="spinner">
          <div class="cube cube-1"></div>
          <div class="cube cube-2"></div>
        </div>
      </div> 
  `;

  usp_html = mapUSP(uspList);

  uspContainer.innerHTML = usp_html;

};
constructUSP();


