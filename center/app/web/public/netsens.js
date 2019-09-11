var arrayConstructor = [].constructor;
var objectConstructor = {}.constructor;

function redirect(){
	window.location.replace("sources.html");
}

function timeConvert(time){
	var date = new Date(time*1000);
	var minutes = "0" + date.getMinutes();
	var seconds = "0" + date.getSeconds();
	var newTime = date.getDate() + '/' + date.getMonth()+'/' + date.getYear().toString().substr(-2) + ' ' + date.getHours() + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
	return newTime;
}

var networkIds=[];
var networkNames=[];
var networks = [];
var devices=[];
var selectedDevice ="";
var links = [];
var networksFilter;
var comboTree1;
loadData(null);
combo();
function combo(){
	if (comboTree1)
		comboTree1.resetLookup();
	comboTree1 = $('#NetworkIds').comboTree({
		source : networks,
		isMultiple: true
	});
}

//modal - click on device
$('#exampleModal').on('show.bs.modal', function (event) {
	var button = $(event.relatedTarget);
	var modal = $(this);
	modal.find('.modal-title').text('Device Info ' + selectedDevice.mac);
	$("#label_id").text(selectedDevice.id);
	$("#label_id2").text(selectedDevice.mac);
	$("#label_id3").text(selectedDevice.ip);
	$("#label_id4").text(selectedDevice.vendor);
	$("#label_id5").text(JSON.stringify(selectedDevice.extraData));
	$("#label_id6").text(selectedDevice.dhcpFingerPrint);
	$("#label_id7").text(timeConvert(selectedDevice.firstTimeSeen));
	$("#label_id8").text(timeConvert(selectedDevice.lastTimeSeen));
});

$('#commentModal').on('show.bs.modal', function (event) {
	var button = $(event.relatedTarget);
	selectedDevice = findElement(devices,"uuid",button.context.dataset.device);
	var modal = $(this);
	modal.find('.modal-title').text('Device Info ' + selectedDevice.uuid);
	modal.find('#modalSubmit').attr('onClick','deviceComment(\'' + selectedDevice.networkId + '\',\'' +selectedDevice.uuid + '\')');
	});


// will return undefined if not found; you could return a default instead
function findElement(arr, propName, propValue) {
	for (var i=0; i < arr.length; i++)
		if (arr[i][propName] == propValue)
			return arr[i];
}

function isNeighborLink(node, link) {
	return link.target.uuid === node.uuid || link.source.uuid === node.uuid;
}

function getNodeColor(node, neighbors) {
	if (Array.isArray(neighbors) && neighbors.indexOf(node.uuid) > -1) 
		if (node.role == "gateway")
			return 'url(#gatewaySelectedImage)'
		else
			return 'url(#desktopSelectedImage)'
	if (node.role == "gateway")
		return 'url(#gatewayImage)';
	return 'url(#desktopImage)';
}

/*function getTooltip(node){
	var str="";
	console.log(node);
	if (node.hostname != null)
		str+= ' Hostname: '+node.hostname;
	if (node.ip != null)
		str+= ' IP: '+node.ip;
	if (node.mac != null)
		str+= ' MAC: '+node.mac;
	console.log(str);
	return str;
	
}*/

function getNodeColor(node) {
	if (node.role == "gateway")
		return 'url(#gatewayImage)';
	return 'url(#desktopImage)';
}

function getNodeSelectedColor(node) {
	if (node.role == "gateway")
		return 'url(#gatewaySelectedImage)';
	return 'url(#desktopSelectedImage)';
}

function getLinkColor(node, link) {
	if (node == null)
		return '#a3b2b8';
	return isNeighborLink(node, link) ? 'green' : '#a3b2b8';
}

function getNeighbors(node) {
	return links.reduce(function (neighbors, link) {
		if (link.target.uuid === node.uuid) 
			neighbors.push(link.source.uuid)
		else if (link.source.uuid === node.uuid)
			neighbors.push(link.target.uuid)
		return neighbors
		},
		[node.uuid]
	  )
}

function reloadTable(){
	//spinner
	loadData(networksFilter,false);
}
function runPlugin(networkId,devUUID,pluginUUID){
	var response = httpReq('/api/networks/' + networkId + '/devices/' + devUUID + '/plugins/' + pluginUUID,"POST",null);
	var obj = JSON.parse(response);
	if (JSON.stringify(obj) == "{\"success\":true}")
	{
		sleep(5000).then(() => {
			reloadTable();
		});
	}
	else
		alert('b');
}

function analyzeDevice(){
	alert('analyzeDevice - GET');
}

function closeDevice(networkId,idx){
	var response = httpReq('/api/networks/' + networkId + '/devices/' + idx + '/close',"POST",null);
	var obj = JSON.parse(response);
	if (JSON.stringify(obj) == "{\"success\":true}")
	{
		sleep(5000).then(() => {
			loadData(networksFilter,false);
		});
		alert('s');
	}
	else
		alert('b');
}

function deviceComment(networkId,uuid){
	var comment= $('#comment').val();
	var response = httpReq('/api/networks/' + networkId + '/devices/' + uuid + '/comment','POST','{"comment":"' + comment + '"}');
	var obj = JSON.parse(response);

	if (JSON.stringify(obj) == "{\"success\":true}")
	{
		
		$("#spinner").css("visibility","visible");
		$("#devicesTable").css("visibility","hidden");
		$('#commentModalClose').click();
		sleep(5000).then(() => {
			loadData(networksFilter,false);
		});
		
	}
	else
		alert('b');
}

function buildHtmlTable(selector,objects) {
	var columns = addAllColumnHeaders(objects, selector);
	for (var i = 0; i < objects.length; i++) {
		var flag = 0;
		var row$ = $('<tr/>');
		for (var j =0; j< columns.length; j++){
			if (objects[i][columns[j]] != null)
				var cellValue = objects[i][columns[j]];
			else
				var cellValue = "-";
			if ((columns[j]=="mac" && cellValue != "-") || (columns[j]=="ip" && flag==0)) 
			{
				cellValue = '<a id="tab_'+objects[i]['uuid']+'" href="javascript:goToNode(\'' + objects[i]['uuid'] + '\');">' + cellValue + '</a>';
				flag = 1;
			}
			else if (columns[j]=="firstTimeSeen" || columns[j]=="lastTimeSeen")
				cellValue=timeConvert(cellValue);
			else if (columns[j] == "packetCounter"){
				cellValue = cellValue['total'];
				cellValue = JSON.stringify(cellValue);

			}
			else if (columns[j] == "extraData" ){
				var data='';
				for (var src in cellValue){
					data += src +' : '+JSON.stringify(cellValue[src]) + '<br/>';
				}
				cellValue=data;
			}
			else if (columns[j] == "Actions" ){
				cellValue = "<div class=\'dropdown\'><button class=\'btn btn-default dropdown-toggle\' type=\'button\' id=\'menu1\' data-toggle=\'dropdown\' style='font-size:11px;font-weight:700;cursor:pointer;padding-top:0px;padding-bottom:0px;padding-left:0px;'>Actions<span class=\'caret\'></span></button><ul class=\'dropdown-menu\' role=\'menu\' aria-labelledby=\'actions\' style='min-width:100px;'><li role=\'presentation\'><label style='font-size:11px;cursor:pointer;margin-left:10px;' onclick=\"runPlugin(\'" + objects[i]['networkId'] + "\',\'" + objects[i]['uuid'] + "\',\'vendor-123\')\">Get Vendor</label></li><li role=\'presentation\'><label style='font-size:11px;cursor:pointer;margin-left:10px;' onclick=\"runPlugin(\'" + objects[i]['networkId'] + "\',\'" + objects[i]['uuid'] + "\',\'plugin-fb-123\')\">Verify Fingerprint</label></li><li role=\'presentation\'><label style='font-size:11px;cursor:pointer;margin-left:10px;' onclick=\"closeDevice(\'" + objects[i]['networkId'] + "\',\'" + objects[i]['idx'] + "\')\">Close</label></li><li role=\'presentation\'><label style='font-size:11px;cursor:pointer;margin-left:10px;' onclick=\"analyzeDevice(\'" + objects[i]['networkId'] + "\',\'" + objects[i]['uuid'] + "\')\">Analyze</label></li><li role=\'presentation\'><label style='font-size:11px;cursor:pointer;margin-left:10px;' data-toggle='modal' data-target='#commentModal' data-device=\'" + objects[i]['uuid'] + "\'>Comment</label></li></ul></div>";
				cellValue = "<div class=\'dropdown\'><button class=\'btn btn-default dropdown-toggle\' type=\'button\' id=\'menu1\' data-toggle=\'dropdown\' style='font-size:11px;font-weight:700;cursor:pointer;padding-top:0px;padding-bottom:0px;padding-left:0px;'>Actions<span class=\'caret\'></span></button><ul class=\'dropdown-menu\' role=\'menu\' aria-labelledby=\'actions\' style='min-width:100px;'><li role=\'presentation\'><label style='font-size:11px;cursor:pointer;margin-left:10px;' onclick=\"runPlugin(\'" + objects[i]['networkId'] + "\',\'" + objects[i]['uuid'] + "\',\'vendor-123\')\">Get Vendor</label></li><li role=\'presentation\'><label style='font-size:11px;cursor:pointer;margin-left:10px;' onclick=\"runPlugin(\'" + objects[i]['networkId'] + "\',\'" + objects[i]['uuid'] + "\',\'plugin-fb-123\')\">Verify Fingerprint</label></li><li role=\'presentation\'><label style='font-size:11px;cursor:pointer;margin-left:10px;' onclick=\"closeDevice(\'" + objects[i]['networkId'] + "\',\'" + objects[i]['idx'] + "\')\">Close</label></li><li role=\'presentation\'><label style='font-size:11px;cursor:pointer;margin-left:10px;' onclick=\"analyzeDevice(\'" + objects[i]['networkId'] + "\',\'" + objects[i]['uuid'] + "\')\">Analyze</label></li><li role=\'presentation\'><label style='font-size:11px;cursor:pointer;margin-left:10px;' data-toggle='modal' data-target='#commentModal' data-device=\'" + objects[i]['uuid'] + "\'>Comment</label></li></ul></div>";
			}
			else
				cellValue = cellValue.toString();
			row$.append($('<td/>').html(cellValue));
		}
		$(selector).append(row$);
	}
}

function goToNode(nodeUUID){
	console.log('a');
	console.log(links);
	//reset colors
	for (l in links)
	{
		$("#" + links[l].uuid).css('stroke', function () { return getLinkColor(null,links[l]) });
	}
	for (d in devices)
	{
		$("#" + devices[d].uuid).css('fill', function () { return getNodeColor(devices[d]) });
	}
	console.log('b');
	$('body,html').animate({scrollTop: 80}, 1000);
	console.log('c');
	var device = findElement(devices,"uuid",nodeUUID);
	console.log('d');
	console.log(device);
	$("#" + nodeUUID).css('fill', function (n) { return getNodeSelectedColor(device)});
	console.log('e');
	for (l in links)
	{
		$("#" + links[l].uuid).css('stroke', function () { return getLinkColor(device,links[l]) });
	}
	console.log('f');
	
	//$("#" + aaa).click();
}
// Adds a header row to the table and returns the set of columns.
function addAllColumnHeaders(objects, selector) {
	var columnSet = [];
	var headerTr$ = $('<thead style="background-color:#25a9af; color:white;"/>');
	headerTr$.append($('<tr/>'));
	columnSet=['mac','ip','firstTimeSeen','lastTimeSeen','packetCounter','role','hostname','extraData','Actions']
	for (var col in columnSet){
		headerTr$.append($('<th/>').html(columnSet[col]));
	}

	$(selector).append(headerTr$);
	
	return columnSet;
}


function test(d) {
                    div	.transition()
						.duration(200)
						.style("opacity", .9)
                    div	.html(d.mac)
						.style("left", (d.x + d.hits) + "px")
						.style("top", (d.y + d.hits) + "px");		
                    };

function loadJSON(file,callback) {
    var xobj = new XMLHttpRequest();
        xobj.overrideMimeType("application/json");
    xobj.open('GET', file, true); // Replace 'my_data' with the path to your file
    xobj.onreadystatechange = function () {
          if (xobj.readyState == 4 && xobj.status == "200") {
            // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
            callback(xobj.responseText);
          }
    };
    xobj.send(null);
 }
 
function applyFilters(){
	var networksFilter = [];
	var networksNames = $("#NetworkIds").val().replace(' ','').split(',');
	for (netN in networksNames)
	{
		for (net in networks)
		{
			if (networksNames[netN] == networks[net]["name"])
				networksFilter.push(networks[net]["uuid"])
		}
	}
	$("#svg").empty();
	devices = "";
	links = "";
	loadData(networksFilter);
}

function printGraph(networksFilter){
	var svg = d3.select("#devicesGraph")
		.append("svg")
		.attr("id","gs")
		//.attr("width", window.innerWidth- 252 - 75)
		//.attr("height", 450)
	    .attr("viewBox", [0, 0, window.innerWidth - 252 - 75, 350]);

	var dragDrop = d3.drag().on('start', function (node) {
		node.fx = node.x
		node.fy = node.y
		}).on('drag', function (node) {
			simulation.alphaTarget(0.3).restart()
			node.fx = d3.event.x
			node.fy = d3.event.y
			}).on('end', function (node) {
				if (!d3.event.active) {
					simulation.alphaTarget(0)
					}
				node.fx = null
				node.fy = null
				})  
			// Initialize the links
			var link = svg.selectAll("line")
				.data(links)
				.enter()
				.append("line")
					.attr("id", function(l){return l.uuid})
					.style("stroke", "#a3b2b8")
					.style("stroke-width", "2")
			var div = d3.select("#devicesGraph").append("div")
				.attr("class", "device-tooltip")
					.style("opacity", 0);
          // Initialize the nodes
			var node = svg
				.selectAll("circle")
				.data(devices)
				.enter()
				.append("circle")
					.attr("id", function(d){return d.uuid})
					.attr("r", function(d) {return Math.max(8,Math.min(d.packetCounter.total, 450/devices.length,14))})
				.call(dragDrop)
					.style("stroke", "#25a9af")
					.style("stroke-width",function(d) {return Math.min(Math.max(1,Math.pow(d.packetCounter.total,-5)),3)})
			  
			  .attr("fill",function (n) { return getNodeColor(n) })
			  .style("cursor","pointer")
			  .on ("mouseover", function(d){
				  	var str="";
					if (d.hostname != null)
						str+= ' Hostname: '+d.hostname;
					else
						str+= ' Hostname: - '
					if (d.ip != null)
						str+= ' <br>IP: '+d.ip;
					else
						str+= ' <br>IP: - '
					if (d.mac != null)
						str+= ' <br>MAC: '+d.mac;
					else 
						str+= ' <br>MAC: - '
                    div	.transition()
						.duration(200)
						.style("opacity", .9)
                    //div	.html("Hostname: "+d.hostname + " IP: "+ d.ip + " MAC:" +d.mac)
					div .html(str)
					.style("left", (d.x + d.packetCounter.total) + "px")
					.style("top", (d.y + d.packetCounter.total) + "px");	})
			  .on("mouseout", function(d) {
                    div.transition()
                        .duration(500)
                        .style("opacity", 0);
                })
			  .on("click",selectNode);
			  
          // Let's list the force we wanna apply on the network
          var simulation = d3.forceSimulation(devices)                 // Force algorithm is applied to data.nodes
              .force("link", d3.forceLink()                               // This force provides links between nodes
					.id(function(d) {return d.uuid; })                     // This provide  the id of a node
                    .links(links)                                    // and this the list of links
              )
			  .force("charge", d3.forceManyBody().strength(80).distanceMax(300).distanceMin(80))
			  .force("center", d3.forceCenter((window.innerWidth- 252 - 54) / 2, 350 / 2))     // This force attracts nodes to the center of the svg area
              .force("collide", d3.forceCollide(20).strength(1).iterations(100))
			  .nodes(devices)
              .on("tick", ticked);
			  function selectNode(selectedNode) {
				node.style('fill',function (n) { return getNodeColor(selectNode) });
				var neighbors = getNeighbors(selectedNode);
				$("#" + selectedNode.uuid).css('fill', function (n) { return getNodeSelectedColor(selectNode) });
				link.style('stroke', function (l) { return getLinkColor(selectedNode, l) });
			  }
			
			var gs = document.querySelector( '#gs' );
			var ns = 'http://www.w3.org/2000/svg';
			
			var fo = document.getElementById("fo");
			if (fo)
			{
				var child = document.getElementById("ad");
				fo.removeChild(ad);
				gs.removeChild(fo);
			}
			
			var foreignObject = document.createElementNS( ns, 'foreignObject');
			foreignObject.setAttribute("id", "fo");
			foreignObject.setAttribute('height', 300);
			foreignObject.setAttribute('width', '100%');
			
			filtersName = "All Networks";
			console.log(networksFilter);
			if (networksFilter)
			{
				filtersName = [];
				for (netN in networksFilter)
				{
					for (net in networks)
					{
						if (networksFilter[netN] == networks[net]["uuid"])
							filtersName.push(networks[net]["name"])
					}
				}
			}
			
			//var ad = document.createElement('div');
			//ad.setAttribute("id", "ad");
			//ad.innerHTML = '<div id="filters" class="row" style="visibility:visible"><div class="col-lg-6"><label style="font-size:11px;font-weight:700;margin-bottom:0px;">Filters</label><input type="text" id="NetworkIds" style="font-size:11px;" placeholder="' + filtersName.toString() +'"/></div><div class="col-lg-2"><button onclick="applyFilters()" style="font-size: 11px;font-weight: 700;height: 28px;margin-top: 28px;" class="btn btn-primary">Apply</button></div></div>';	
			//foreignObject.appendChild( ad );
			//gs.appendChild(foreignObject);
			//combo();
				
          // This function is run at each iteration of the force algorithm, updating the nodes position.
	  function ticked() {
		link
			.attr("x1", function(d) { return d.source.x + 10; })
			.attr("y1", function(d) { return d.source.y - 10; })
			.attr("x2", function(d) { return d.target.x + 10 ; })
			.attr("y2", function(d) { return d.target.y - 10; });

		node
			 .attr("x", function (d) { return d.x+10; })
			 .attr("y", function(d) { return d.y-10; })
			 .attr("cx", function (d) { return d.x+10; })
			 .attr("cy", function(d) { return d.y-10; });
	  }

	  
 }
 
function httpReq(theUrl,method,data){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( method, theUrl, false ); // false for synchronous request
	xmlHttp.setRequestHeader('Content-Type', 'application/json');
    xmlHttp.send(data);
    return xmlHttp.responseText;
}

function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

function loadData(networksFilter,updateGraph = true){
	networkIds=[];
	networkNames=[];
	devices=[];
	links = [];
	var response = httpReq('/api/overview',"GET",null);
	var obj = JSON.parse(response);
	networks = obj.networks;
	for (var i = 0; i < networks.length; i++)
	{
		if (networksFilter != null)
		{
			if (networksFilter.includes(networks[i]['uuid'].toString())){
				networkNames.push(networks[i]['uuid'].toString());
				networkIds.push(networks[i]['uuid'].toString());
			}
		}
		else{
			networkIds.push(networks[i]['uuid'].toString());
			networkNames.push(networks[i]['uuid'].toString());
		}
	}
	obj = null;
	for (id in networkIds){
		var currId = networkIds[id];
		obj = JSON.parse(httpReq('/api/networks/' + currId,"GET",null));
		for (dev in obj.network.devices)
		{
			devices.push(obj.network.devices[dev]);
		}
		for (lnk in obj.network.links)
		{
			links.push(obj.network.links[lnk]);
		}
	}

 for (var i = 0; i<links.length; i++){
    links[i].source = links[i].sourceDeviceUUID;
    links[i].target = links[i].targetDeviceUUID;
    delete links[i].sourceDeviceUUID;
    delete links[i].targetDeviceUUID;
 }

	$("#devicesTable").empty();
	

	if (devices.length > 0)
	{
		buildHtmlTable('#devicesTable',devices);
		if (updateGraph)
		{
			$("#devicesGraph").empty();
			printGraph(networksFilter);
		}
		$("#devicesGraph").css("visibility","visible");
		$("#devicesTable").css("visibility","visible");
		$("#filters").css("visibility","visible");
		$("#spinner").css("visibility","hidden");
	}
	else
	{
		$("#devicesGraph").html("No Data. Consider changing your filter.");
		$("#devicesGraph").css("visibility","visible");
		$("#spinner").css("visibility","hidden");
	}
};




