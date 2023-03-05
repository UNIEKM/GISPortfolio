// ////---------------------------
// * JavaScript/ Menu icon toggle/ Menu will appear/disappear on click with .active class in @media section 
// * Inspired: W3S https://www.w3schools.com/jsref/met_element_addeventlistener.asp
// * Owner : Kevin VD
// * Date  : Nov 23 (v1)
// -----------------------------//////
$(document).ready(function ()  {  ///------jQuery drop menu inspired by:jQuery HTML Tutorial: https://www.youtube.com/watch?v=tdwXQRZUiRw w3S: https://www.w3schools.com/howto/howto_css_dropdown.asp
  $('.list_item').hover(function ()  {   ///--Hover over .list_item drops submenu---.ready(function) waits for page to load.
      $(this).children('.sub_drop').slideDown(250);  ///Children are list items in sub drop menu slide down is speed it drops.
  },
        function () {
            $(this).children('.sub_drop').slideUp(250); ///Slide up once pointer is out of menu block (250) is the speed it returns.
        }
  );

});
const toggleButton = document.getElementById('MenuIcon');//   Assign button to a variable "ID"
const NavBarList = document.getElementById('NavList'); //Second variable for navbar list
  toggleButton.addEventListener('click', function() {
    NavBarList.classList.toggle('active');
}) //Now we need an event listener for when user clicks the menu icon, once clicked, run function, selecting and toggle our active class for navlist (hidden in media screen settings)

//Scroll to top button: CREDIT: https://www.w3schools.com/howto/howto_js_scroll_to_top.asp 
// Get the button by id "TopBtn":
let mybutton = document.getElementById("TopBtn");

// When the user scrolls down 150px from the top of the document, show the button.
window.onscroll = function() {scrollFunction()};

function scrollFunction() { //Function to show or hide button depending position of page from top.
  if (document.body.scrollTop > 150 || document.documentElement.scrollTop > 150) {
    mybutton.style.display = "flex"; //once page scrolls past 150px from the top button is displayed
  } else {
    mybutton.style.display = "none"; //before page scrolls past 150px from the top button is not displayed
  }
}

// When the user clicks on the button, scroll to the top of the document using JavaScript topFunction()
function topFunction() {
  document.body.scrollTop = 0; // For Safari **Not sure I need this but w3schools used it****
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera **Not sure I need this but w3schools used it****
}

// var viewer = OpenSeadragon({
//   id: "openseadragon1",
//   prefixUrl: "https://cdnjs.cloudflare.com/ajax/libs/openseadragon/2.4.2/images/",
//   tileSources: "https://openseadragon.github.io/example-images/highsmith/highsmith.dzi"
// });








