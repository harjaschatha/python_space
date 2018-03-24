$(document).ready(function() {
  var noticeNum = $('#socs > div').length;
  var delay = 50;
  $('#socs > div').hide();
  $('#socs div').each(function(i) {
    $(this).delay((i++) * delay).fadeTo(1000, 1); 
  });
});
