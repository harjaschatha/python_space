function sort(limit){
	var lec=document.getElementById('select_lecture');
	var tut=document.getElementById('select_tutorial');
	var prc=document.getElementById('select_practical');
	lec=lec.checked;
	tut=tut.checked;
	prc=prc.checked;
	var cleared={};
	var uncleared={};	
		for (var student in jsonstr){
			var total=0.0;
			var count=0;
			if(lec){
				total+=jsonstr[student]['lecture'];
				count+=1;
				}
			if(tut){
				total+=jsonstr[student]['tutorial'];
				count+=1;
				}
			if(prc){
				total+=jsonstr[student]['practical'];
				count+=1;
				}
			total/=count;
			if (total<limit){
				uncleared[student]={'lecture':jsonstr[student]['lecture'],
						'tutorial':jsonstr[student]['tutorial'],
						'practical':jsonstr[student]['practical']};
				}
			if (total>=limit){
				cleared[student]={'lecture':jsonstr[student]['lecture'],
						'tutorial':jsonstr[student]['tutorial'],
						'practical':jsonstr[student]['practical']};
				}

			}
		document.getElementById('sorted_table').getElementsByTagName('tbody')[0].innerHTML='';




		for (var student in uncleared){
			var row=document.createElement('tr');
			var td_n=document.createElement('td');
			var td_l=document.createElement('td');
			var td_t=document.createElement('td');
			var td_p=document.createElement('td');
			td_l.innerHTML=jsonstr[student]['lecture'];
			td_t.innerHTML=jsonstr[student]['tutorial'];
			td_p.innerHTML=jsonstr[student]['practical'];
			td_n.innerHTML=student;
			row.appendChild(td_n);
			 row.appendChild(td_l);
			 row.appendChild(td_t);
			 row.appendChild(td_p);
			 $('#sorted_table tbody').append(row);
		}  
}

$(document).ready(function (){

	for (var student in jsonstr){
		var row=document.createElement('tr');
		var td_n=document.createElement('td');
		var td_l=document.createElement('td');
		var td_t=document.createElement('td');
		var td_p=document.createElement('td');
		td_l.innerHTML=jsonstr[student]['lecture'];
		td_t.innerHTML=jsonstr[student]['tutorial'];
		td_p.innerHTML=jsonstr[student]['practical'];
		td_n.innerHTML=student;
		row.appendChild(td_n);
		row.appendChild(td_l);
		row.appendChild(td_t);
		row.appendChild(td_p);
		$('#sorted_table tbody').append(row);
	}  
	$('#sort_click').on('click',function (){
		var filter=$('#filter').val();
		filter*1;
		sort(filter);
		})
})


