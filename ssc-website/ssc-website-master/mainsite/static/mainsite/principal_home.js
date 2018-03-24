$(document).ready(function() {
  var noticeNum = $('#notice-board > div').length;
  var delay = 250;
  $('#notice-board > div').hide();
  $('#notice-board div').each(function(i) {
    $(this).delay((i++) * delay).fadeTo(1000, 1); 
  });
});
