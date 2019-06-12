function findClassName(val){
	switch(val.value) {
	  case '1':
	    return 'Standard I';
	    break;
	  case '2':
	    return 'Standard II';
	    break;
	  case '3':
	    return 'Standard III';
	    break;
	  case '4':
	    return 'Standard IV';
	    break;
	  case '5':
	    return 'Standard V';
	    break;
	  case '6':
	    return 'Standard VI';
	    break;
	  case '7':
	    return 'Standard VII';
	    break;
	  case '8':
	    return 'Standard VIII';
	    break;
	  case '9':
	    return 'Standard IX';
	    break;
	  case '10':
	    return 'Standard X';
	    break;
	  case '11':
	    return 'Standard XI';
	    break;
	  case '12':
	    return 'Standard XII';
	    break;
	  case '13':
	    return 'Nursery';
	    break;
	  case '14':
	    return 'LKG';
	    break;
	  case '15':
	    return 'UKG';
	    break;
	  default: return 'No Class Selected';
	} 
}


function addClass(){
	var newStandard = document.getElementById('newstandard').value;
	var itemList = document.getElementById('items');
	totalSection = document.getElementById('section').value;

	var li = document.createElement('li')
	li.className = 'list-group-item';
	var newClassName = findClassName(newstandard);
	li.appendChild(document.createTextNode(newClassName+' with total '+totalSection+' Section'));
	var deleteBtn = document.createElement('button');
	deleteBtn.className = 'btn-danger float-right delete';
	deleteBtn.onclick = removeClass;
	deleteBtn.appendChild(document.createTextNode('Remove'));
	li.appendChild(deleteBtn);
	itemList.appendChild(li);
}


function removeClass(){
	if(confirm('This class will be deleted')){
		var li=this.parentElement;
		var itemList = document.getElementById('items');
		itemList.removeChild(li);
	}
}

function send_data(){
	session = $('#session').val();
	startdate = $('#startdate').val();
	enddate = $('enddate').val();

	$.ajax({
		data : {
			session : session
		},
		type : 'POST',
		url : '/process'
	})
	.done(function(data){
		if(data.error){
			alert('error!!');
		}else{
			alert('no error!');
		}
	});
}


// function get_data_session(){
// 	session_name = $('#session_name').val();
// 	startdate = $('#startdate').val();;
// 	enddate = $('#enddate').val();
// 	alert(session_name)
// 	$.ajax({
// 		data : {
// 			session_name : session_name,
// 			startdate : startdate,
// 			enddate : enddate
// 		},
// 		type : 'POST',
// 		url : '/process'
// 	})
// 	.done(function(data) {

// 		if (data.error) {
// 			alert(data.startdate);
// 		}
// 		else {
// 			alert(data.enddate);
// 		}

// 	});
// }


















