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
	var newTime = date.getDate() + '/' + (date.getMonth()+1)+'/' + date. getFullYear().toString()+ ' ' + date.getHours() + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
	return newTime;
}




function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time));
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
			if (columns[j]=="lts")
				cellValue=timeConvert(cellValue);
			else if (columns[j]=="status")
			{
				var d =  Date.now();
				var millis = parseInt(d) / 1000 - parseInt(objects[i]['lts']);
				if (millis<10000)
					cellValue='<img src="img/ok.png" style="height: 20px;">'
				else 
					cellValue='<img src="img/error.png" style="height: 10px;">'
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
	columnSet=['name','lts','status']
	for (var col in columnSet){
		if (columnSet[col] == "lts")
			headerTr$.append($('<th/>').html("lastTimeSeen"));
		else
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



function loadData(){
	var response = httpReq('/api/overview',"GET",null);
	var obj = JSON.parse(response);
	networks = obj.monitor;
	$("#MonitorTable").empty();
	buildHtmlTable('#MonitorTable',networks);
	$("#spinner").css("visibility","hidden");
	$("#MonitorTable").css("visibility","visible");

}	

