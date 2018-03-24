// function alike(str1, str2){
//   //checks if two strings are alike
//   //true if alphabets are the same.
//   str1 = str1.toLowerCase().replace(' ','').replace('_','');
//   str2 = str2.toLowerCase().replace(' ','').replace('_','');
//   //strings normalized for comparison
//   if(str1==str2){
// 	 return true;
//   }
//   return false;
// }

$(document).ready(function (){
  //get current url
  var location=window.location.href;
  //get the nav bar equivalent
  location=location.split('/')[3];
  // Create a select and append to #menu
  var $select = $('<select id="select-nav" class="form-control" style="color: black;"></select>');
  $select.append('<option value="null">- Select a page -</option>');
  $('nav').append($select);
  // Cycle over menu links
  $('nav a').each(function (){
    var $anchor = $(this);    
    // Create an option
    var $option = $('<option></option>');
    // Option's value is the href's link
    $option.val($anchor.attr('href'));
    // Option's text is the text of the link
    $option.text($anchor.text());
    // Append option to select
    $select.append($option);

  });

  // Adding a slight margin-top to the select
  $select.css('margin-top', '20px');

  // Bind change listener to the select
  $select.change(function(){
    // Go to the select's location
    window.location = $select.val();
  });
});
