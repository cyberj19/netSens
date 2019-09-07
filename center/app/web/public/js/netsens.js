var arrayConstructor = [].constructor;
var objectConstructor = {}.constructor;

function timeConvert(time){
	var date = new Date(time*1000);
	var minutes = "0" + date.getMinutes();
	var seconds = "0" + date.getSeconds();
	var newTime = date.getDate() + '/' + date.getMonth()+'/' + date.getYear().toString().substr(-2) + ' ' + date.getHours() + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
	return newTime;
}

var networkIds=[];
var devices=[];
var selectedDevice ="";
var links = [];
var comboTree1, comboTree2;

jQuery(document).ready(function($) {
		comboTree1 = $('#NetworkIds').comboTree({
			source : devices,
			isMultiple: true
		});
});

loadData(null);

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
	return link.target.id === node.id || link.source.id === node.id
}

function getNodeColor(node, neighbors) {
	if (Array.isArray(neighbors) && neighbors.indexOf(node.id) > -1) 
		return 'red'
	return 'green';
}

function getLinkColor(node, link) {
	return isNeighborLink(node, link) ? 'green' : 'yellow'
}

function getNeighbors(node) {
	return links.reduce(function (neighbors, link) {
		if (link.target.id === node.id) 
			neighbors.push(link.source.id)
		else if (link.source.id === node.id)
			neighbors.push(link.target.id)
		return neighbors
		},
		[node.id]
	  )
}

function runPlugin(networkId,devUUID,pluginUUID){
	var response = httpReq('/api/networks/' + networkId + '/devices/' + devUUID + '/plugins/' + pluginUUID,"POST",null);
	var obj = JSON.parse(response);
	console.log('response');
	console.log(obj);
}

function analyzeDevice(){
	alert('analyzeDevice - GET');
}

function closeDevice(networkId,idx){
	var response = httpReq('/api/networks/' + networkId + '/devices/' + idx + '/close',"POST",null);
	var obj = JSON.parse(response);

}

function deviceComment(networkId,uuid){
	var comment= $('#comment').val();
	var response = httpReq('/api/networks/' + networkId + '/devices/' + uuid + '/comment','POST','{"comment":"' + comment + '"}');
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
			if (columns[j]=="firstTimeSeen" || columns[j]=="lastTimeSeen")
				cellValue=timeConvert(cellValue);
			else if (columns[j] == "packetCounter"){
				cellValue = cellValue['total'];
				cellValue = JSON.stringify(cellValue);

			}
			else if (columns[j] == "extraData" ){
				var data='';
				for (var src in cellValue){
					console.log(cellValue);
					console.log(src);
					data += src +' : '+JSON.stringify(cellValue[src]);
				}
				cellValue=data;
			}
			else if (columns[j] == "Actions" ){
				cellValue = "<div class=\'dropdown\'><button class=\'btn btn-default dropdown-toggle\' type=\'button\' id=\'menu1\' data-toggle=\'dropdown\' style='font-size:11px;font-weight:700;cursor:pointer;padding-top:0px;padding-bottom:0px;padding-left:0px;'>Actions<span class=\'caret\'></span></button><ul class=\'dropdown-menu\' role=\'menu\' aria-labelledby=\'actions\' style='min-width:100px;'><li role=\'presentation\'><label style='font-size:11px;cursor:pointer;margin-left:10px;' onclick=\"runPlugin(\'" + objects[i]['networkId'] + "\',\'" + objects[i]['uuid'] + "\',\'vendor-123\')\">Get Vendor</label></li><li role=\'presentation\'><label style='font-size:11px;cursor:pointer;margin-left:10px;' onclick=\"runPlugin(\'" + objects[i]['networkId'] + "\',\'" + objects[i]['uuid'] + "\',\'plugin-fb-123\')\">Verify Fingerprint</label></li><li role=\'presentation\'><label style='font-size:11px;cursor:pointer;margin-left:10px;' onclick=\"closeDevice(\'" + objects[i]['networkId'] + "\',\'" + objects[i]['idx'] + "\')\">Close</label></li><li role=\'presentation\'><label style='font-size:11px;cursor:pointer;margin-left:10px;' onclick=\"analyzeDevice(\'" + objects[i]['networkId'] + "\',\'" + objects[i]['uuid'] + "\')\">Analyze</label></li><li role=\'presentation\'><label style='font-size:11px;cursor:pointer;margin-left:10px;' data-toggle='modal' data-target='#commentModal' data-device=\'" + objects[i]['uuid'] + "\'>Comment</label></li></ul></div>";
			}
			else
				cellValue = cellValue.toString();
			row$.append($('<td/>').html(cellValue));
		}
		$(selector).append(row$);
	}
}

// Adds a header row to the table and returns the set of columns.
function addAllColumnHeaders(objects, selector) {
	var columnSet = [];
	var headerTr$ = $('<thead style="background-color:#25a9af; color:white;"/>');
	headerTr$.append($('<tr/>'));
	columnSet=['idx','mac','ip','firstTimeSeen','lastTimeSeen','packetCounter','role','hostname','extraData','Actions']
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
	var networksFilter = $("#NetworkIds").val().replace(' ','').split(',');
	d3.select("svg").remove();
	devices = "";
	links = "";
	loadData(networksFilter);
}

function printGraph(){
	var svg = d3.select("#devicesGraph")
		.append("svg")
		.attr("width", screen.width - 327)
		.attr("height", screen.height - 280);
	var dragDrop = d3.drag().on('start', function (node) {
		node.fx = node.x
		node.fy = node.y
		}).on('drag', function (node) {
			simulation.alphaTarget(0.7).restart()
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
				//.append("image")
				//  .attr("xlink:href", "test.png")
				//  .attr("width", function(d) {return Math.max(20,Math.min(d.packetCounter.total, (screen.height-280)/devices.length*5,40))})
				//  .attr("height", function(d) {return Math.max(20,Math.min(d.packetCounter.total, (screen.height-280)/devices.length*5,40))})
				//  .style("border-radius", "50%")
				.append("circle")
					.attr("id", function(d){return d.idx})
					.attr("r", function(d) {return Math.max(6,Math.min(d.packetCounter.total, (screen.height-280)/devices.length,20))})
				.call(dragDrop)
					.style("stroke", "#25a9af")
					.style("stroke-width",function(d) {return Math.max(1,Math.min(d.packetCounter.total/50,3))})
			  
			  .attr("fill","url(#desktopImage)")
			  .style("cursor","pointer")
			  .on ("mouseover", function(d){
				  	$("#"+d.idx).css('fill',"url(#desktopSelectedImage)");
                    div	.transition()
						.duration(200)
						.style("opacity", .9)
                    div	.html(d.mac)
						.style("left", (d.x + d.packetCounter.total) + "px")
					.style("top", (d.y + d.packetCounter.total) + "px");	})
			  .on("mouseout", function(d) {
					$("#"+d.idx).css('fill',"url(#desktopImage)");
                    div.transition()
                        .duration(500)
                        .style("opacity", 0);
                })
				//.on("click",selectNode);
                .on("click",function(d) {
				selectedDevice = findElement(devices,"mac",d.mac);
				$("#btnt").click();
                });
          // Let's list the force we wanna apply on the network
          var simulation = d3.forceSimulation(devices)                 // Force algorithm is applied to data.nodes
              .force("link", d3.forceLink()                               // This force provides links between nodes
                    .id(function(d) {return d.idx; })                     // This provide  the id of a node
                    .links(links)                                    // and this the list of links
              )
              .force("charge", d3.forceManyBody().strength(function(d){return -20}))         // This adds repulsion between nodes. Play with the -400 for the repulsion strength
			  .force("center", d3.forceCenter((screen.width-300) / 2 - 20, (screen.height-280) /2))     // This force attracts nodes to the center of the svg area
              .force("Collide", d3.forceCollide(function(d) {return Math.max(6,Math.min(d.packetCounter.total, (screen.height-280)/devices.length)) * 2 * 1.2}))
              .nodes(devices)
              .on("tick", ticked);
			  function selectNode(selectedNode) {
			    var neighbors = getNeighbors(selectedNode)
			    node.style('fill', function (n) { return getNodeColor(n, neighbors) })
			    link.style('stroke', function (l) { return getLinkColor(selectedNode, l) })
			  }
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

function loadData(networksFilter){
	networkIds=[];
	devices=[];
	links = [];
	var response = httpReq('/api/overview',"GET",null);
	var obj = JSON.parse(response);
	var networks = obj.networks;
	for (var i = 0; i < networks.length; i++)
	{
		if (networksFilter != null)
		{
			if (networksFilter.includes(networks[i]['uuid'].toString()))
				networkIds.push(networks[i]['uuid'].toString());
		}
		else
			networkIds.push(networks[i]['uuid'].toString());
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
    links[i].source = links[i].sourceDeviceIdx;
    links[i].target = links[i].targetDeviceIdx;
    delete links[i].sourceDeviceIdx;
    delete links[i].targetDeviceIdx;
 }

	$("#devicesTable").empty();
	$("#devicesGraph").empty();

	if (devices.length > 0)
	{
		buildHtmlTable('#devicesTable',devices);
		printGraph(networksFilter);
	}
	else
	{
		$("#devicesGraph").html("No Data. Consider changing your filter.");
	}
};




