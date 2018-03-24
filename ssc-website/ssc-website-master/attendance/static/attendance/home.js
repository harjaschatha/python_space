$(document).ready(function() { 
    $('#selectorForm').ajaxForm({ 
        dataType:  'json',  
        success:   processJson 
    }); 
});
function processJson(data) { 
    // 'data' is the json object returned from the server 
    $('#namecloud ol').html('');
    var nc=$('#namecloud ol');

    $('#namecloud p').css('display', 'inherit');
    
    for(var i=0,maximum=data.length;i<maximum;i+=1) {
        nc.append("<li><a href='"+student_att+data[i].id+"'>"+data[i].name+"</a></li>");
    }
}
