$(document).ready(function() {
  var noticeNum = $('#notice-board > div').length;
  var delay = 250;
  $('#notice-board > div').hide();
  $('#notice-board div').each(function(i) {
    $(this).delay((i++) * delay).fadeTo(1000, 1); 
  });

  $(window).resize(function () {
    fixLayout();  
  });

  fixLayout();

});

function fixLayout() {
  if ($(window).width() < 768) {
    $('.rss').addClass('btn-lg btn-block')
  } else {
    $('.rss').removeClass('btn-lg btn-block')
  } 
}