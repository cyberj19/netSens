function httpReq(theUrl,method,data){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( method, theUrl, false ); // false for synchronous request
	xmlHttp.setRequestHeader('Content-Type', 'application/json');
    xmlHttp.send(data);
    return xmlHttp.responseText;
}

function timeConvert(time){
	var date = new Date(time*1000);
	var minutes = "0" + date.getMinutes();
	var seconds = "0" + date.getSeconds();
	var newTime = date.getDate() + '/' + date.getMonth() + ' ' + date.getHours() + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
	return newTime;
}

//Upload pcap file /api/playback
function uploadFile(){	
	var formData = new FormData();
	formData.append('file', $('#file')[0].files[0]);
	$.ajax({
		   url : '/api/playback',
		   type : 'POST',
		   data : formData,
		   processData: false,  // tell jQuery not to process the data
		   contentType: false,  // tell jQuery not to set contentType
		   success : function(data) {
					$("#spinner").css("visibility","visible");
					$("#NetworksTable").css("visibility","hidden");
					sleep(6000).then(() => {
						loadData();
					});
			}
	});
}

function clearNetwork(networkId){
	var response = httpReq('/api/networks/' + networkId + '/clear',"POST",null);
	var obj = JSON.parse(response);
	if (JSON.stringify(obj) == "{\"success\":true}")
	{
		$("#spinner").css("visibility","visible");
		$("#NetworksTable").css("visibility","hidden");
		sleep(6000).then(() => {
			loadData();
		});
	}
	else
		alert('Error Clearing Network');

}

function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

function removeNetwork(networkId){
	var response = httpReq('/api/networks/' + networkId + '/remove',"POST",null);
	var obj = JSON.parse(response);

	if (JSON.stringify(obj) == "{\"success\":true}")
	{
		$("#spinner").css("visibility","visible");
		$("#NetworksTable").css("visibility","hidden");
		sleep(6000).then(() => {
			loadData();
		});
	}
	else
		alert('Error Removing Network');

}

function renameNetwork(networkId){
	var name= $('#rename').val();
	var response = httpReq('/api/networks/' + networkId + '/rename/' + name,'POST',"{\"name\":\""+name+"\"}");
		var obj = JSON.parse(response);
	if (JSON.stringify(obj) == "{\"success\":true}")
	{
		$("#spinner").css("visibility","visible");
		$("#NetworksTable").css("visibility","hidden");
		$('#renameModalClose').click();
		sleep(6000).then(() => {
			loadData();
		});
	}
	else
		alert('Error Removing Network');
}

function buildHtmlTable(selector,objects) {
	var columns = addAllColumnHeaders(objects, selector);
	for (var i = 0; i < objects.length; i++) {
		var row$ = $('<tr/>');
		for (var j =0; j< columns.length; j++){
			if (objects[i][columns[j]] != null)
				var cellValue = objects[i][columns[j]];
			else
				var cellValue = "-";
			if (columns[j]=="createTime" || columns[j]=="lastUpdateTime")
				cellValue=timeConvert(cellValue);
			else if (columns[j] == "Actions" ){
				cellValue = "<div class=\'dropdown\'><button class=\'btn btn-default dropdown-toggle\' type=\'button\' id=\'menu1\' data-toggle=\'dropdown\' style='font-size:11px;font-weight:700;cursor:pointer;padding-top:0px;padding-bottom:0px;padding-left:0px;'>Actions<span class=\'caret\'></span></button><ul class=\'dropdown-menu\' role=\'menu\' aria-labelledby=\'actions\' style='min-width:100px;'><li role=\'presentation\'><label style='font-size:11px;cursor:pointer;margin-left:10px;' data-toggle='modal' data-target='#renameModal' data-networkid=\'" + objects[i]['uuid'] + "\'>Rename</label></li><li role=\'presentation\'><label style='font-size:11px;cursor:pointer;margin-left:10px;' onclick=\"clearNetwork(\'" + objects[i]['uuid'] + "\')\">Clear</label></li><li role=\'presentation\'><label style='font-size:11px;cursor:pointer;margin-left:10px;' onclick=\"removeNetwork(\'" + objects[i]['uuid'] + "\')\">Remove</label></li></ul></div>";

			}
			else
				cellValue = cellValue.toString();
			row$.append($('<td/>').html(cellValue));
		}
		$(selector).append(row$);
	}
}

function addAllColumnHeaders(objects, selector) {
	var columnSet = [];
	var headerTr$ = $('<thead style="background-color:#25a9af; color:white;"/>');
	headerTr$.append($('<tr/>'));
	columnSet=['name','uuid','deviceCount','linkCount','packetCount','createTime','lastUpdateTime','Actions']
	for (var col in columnSet){
		headerTr$.append($('<th/>').html(columnSet[col]));
	}

	$(selector).append(headerTr$);
	
	return columnSet;
}

function loadJSON(file,callback) {
	var xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open('GET', file, true); // Replace 'my_data' with the path to your file
    xobj.onreadystatechange = function () {
		if (xobj.readyState == 4 && xobj.status == "200") {
            callback(xobj.responseText);
        }
    };
    xobj.send(null);
 }
 
$(document).ready(function(){
	var $form = $('form');
	$form.submit(function(){
		$.post($(this).attr('action'), $(this).serialize(), function(response){
            // do something here on success
			},'json');
		return false;
	});
});

var listeners="";
var networks="";
loadData();

$('#renameModal').on('show.bs.modal', function (event) {
	var button = $(event.relatedTarget);
	var modal = $(this);
	modal.find('.modal-title').text('Network Info ' + button.context.dataset.networkid);
	modal.find('#renameModalSubmit').attr('onClick','renameNetwork(\'' + button.context.dataset.networkid + '\')');
	});

function loadData(){
	var response = httpReq('/api/overview',"GET",null);
	var obj = JSON.parse(response);
	networks = obj.networks;
	$("#NetworksTable").empty();
	buildHtmlTable('#NetworksTable',networks);
	$("#spinner").css("visibility","hidden");
	$("#NetworksTable").css("visibility","visible");

}	
//function Connect(btn){
//	console.log(btn.id);
//    $.post("/api/sensors/" + btn.id.substr(8,17) + "/"+btn.id.substr(26)+"/connect",
//    {},function(data,status){alert("Data: " + data + "\nStatus: " + status);}
//	);
//};
  
//function Disconnect(btn){
//	alert('in');
//	console.log(btn.id);
//    $.post("/api/sensors/" + btn.id.substr(8,17) + "/"+btn.id.substr(26)+ "/guid/disconnect",
//    {}//,
//    //function(data,status){
//      //alert("Data: " + data + "\nStatus: " + status);}
//	);
//};
