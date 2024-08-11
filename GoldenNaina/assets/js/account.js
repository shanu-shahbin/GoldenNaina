const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});




$(document).ready(function() {
  console.log("Document ready"); // Check if document ready is triggered

  // Attach click event to the button
  $(document).on('click', ".add-to-wishlist", function (){
    console.log("Button clicked"); // Check if the button click event is triggered
    var product_id = $(this).data("product-item");
    console.log("Product ID:", product_id); // Check if product ID is correctly retrieved
  });
});


