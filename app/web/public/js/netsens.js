var arrayConstructor = [].constructor;
var objectConstructor = {}.constructor;

function timeConvert(time){
	var date = new Date(time*1000);
	var minutes = "0" + date.getMinutes();
	var seconds = "0" + date.getSeconds();
	var newTime = date.getDate() + '/' + date.getMonth() + ' ' + date.getHours() + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
	return newTime;
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

// will return undefined if not found; you could return a default instead
function findElement(arr, propName, propValue) {
	for (var i=0; i < arr.length; i++)
		if (arr[i][propName] == propValue)
			return arr[i];
}


/*function uploadFile(){
	console.log("upload");
	var f = document.getElementById('file').files[0];
    var fd = new FormData();
    fd.append("file", f);
    var config = { headers: { 'Content-Type': undefined },
                         };
    $http.post('/playback', fd, config).success(() => {
            });
	alert("hello");
}*/

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

/*function buildHtmlTable(selector,devices) {
	var columns = addAllColumnHeaders(devices, selector);
	for (var i = 0; i < devices.length; i++) {
		var row$ = $('<tr/>');
		var cellValue = devices[i].networkId;
		cellValue = devices[i].networkId;
		row$.append($('<td/>').html(cellValue));

		cellValue = devices[i].vendor;
		row$.append($('<td/>').html(cellValue));
		
		cellValue = devices[i].ip;
		row$.append($('<td/>').html(cellValue));
		
		cellValue = JSON.stringify(devices[i].extraData);
		row$.append($('<td/>').html(cellValue));
		
		cellValue = devices[i].mac;
		row$.append($('<td/>').html(cellValue));

		row$.append($('<td/>').html(timeConvert(devices[i].firstTimeSeen)));
		
		cellValue = devices[i].id;
		row$.append($('<td/>').html(cellValue));
		
		row$.append($('<td/>').html(timeConvert(devices[i].lastTimeSeen)));
		
		
		//cellValue = devices[i].dhcpFingerPrint;
		//if (cellValue == null){
		//	cellValue ="";
		//}
		//row$.append($('<td/>').html(cellValue.toString()));

		$(selector).append(row$);
		}
}

// Adds a header row to the table and returns the set of columns.
function addAllColumnHeaders(devices, selector) {
	var columnSet = [];
	var headerTr$ = $('<thead style="background-color:#25a9af; color:white;"/>');
	headerTr$.append($('<tr/>'));
  /*for (var i = 0; i < devices.length; i++) {
    var rowHash = devices[i];
    for (var key in rowHash) {
      if ($.inArray(key, columnSet) == -1) {
		if (key != "isClosed" && key != "hits" && key != "arpHits" && key != "dhcpHits" && key!="dhcpFingerPrint"){
        columnSet.push(key);
        headerTr$.append($('<th/>').html(key));
		}
      }
    }
  }*//*
  headerTr$.append($('<th/>').html('networkId'));
  headerTr$.append($('<th/>').html('vendor'));
  headerTr$.append($('<th/>').html('ip'));
  headerTr$.append($('<th/>').html('ExtraData'));
  headerTr$.append($('<th/>').html('Mac'));
  headerTr$.append($('<th/>').html('FirstTimeSeen'));
  headerTr$.append($('<th/>').html('id'));
  headerTr$.append($('<th/>').html('LastTimeSeen'));
  $(selector).append(headerTr$);
  return columnSet;
}*/

function buildHtmlTable(selector,objects) {
	var columns = addAllColumnHeaders(objects, selector);
	for (var i = 0; i < objects.length; i++) {
		var row$ = $('<tr/>');
		for (var j =0; j< columns.length -1; j++){
			if (objects[i][columns[j]] != null)
				var cellValue = objects[i][columns[j]].toString();
			else
				var cellValue = "";
			if (columns[j]=="lastPacketTime" || columns[j]=="lastUpdateTime" || columns[j]=="createTime")
				cellValue=timeConvert(cellValue);
			row$.append($('<td/>').html(cellValue));
		}
		if (selector == '#ListenersTable' && objects[i][columns[6]] == 0){
			row$.append($('<td/>').html('<button id="Connect_' + objects[i][columns[3]] +'_' +objects[i][columns[8]]+'" onclick="Connect(this)">Connect</button>'));
		}
		else if (selector == '#ListenersTable'){
			row$.append($('<td/>').html('<button id="Disconnect_' + objects[i][columns[3]] +'_' +objects[i][columns[8]]+'" onclick="Disconnect()">Disconnect</button>'));

		}
		else{
			var cellValue = objects[i][columns[columns.length - 1]];
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
	for (var i = 0; i < objects.length; i++) {
		var rowHash = objects[i];
		for (var key in rowHash) {
			if ($.inArray(key, columnSet) == -1) {
				columnSet.push(key);
				headerTr$.append($('<th/>').html(key));
			}
		}
	}
	if (selector == '#ListenersTable'){
		columnSet.push('Actions');
		headerTr$.append($('<th/>').html('Actions'));
	}
	$(selector).append(headerTr$);
	return columnSet;
}



function test(d) {
				//	//$("#"+d.id).css('fill','#25a9af');
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
	console.log('Filter');
	console.log(networksFilter);
	d3.select("svg").remove();
	devices = "";
	links = "";
	loadData(networksFilter);
}

function printGraph(networksFilter){
	console.log('PrintGraph');
	console.log(devices);
	console.log(links);
	var svg = d3.select("#content")
.append("svg")
  .attr("width", screen.width - 300)
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
		  if (networksFilter != null)
		  {
			  devices = devices.filter(function(item){
				  if ($.inArray(item.networkId.toString(), networksFilter) != -1)
					return true;
				  return false;
				});
			  links = links.filter(function(item){
				  if ($.inArray(item.networkId.toString(), networksFilter) != -1)
					return true;
				  return false;
				});	  
		  }
          // Initialize the links
          var link = svg
            .selectAll("line")
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
            .append("circle")
              .attr("id", function(d){return d.idx})
			  .attr("r", function(d) {return Math.max(2,Math.min(d.packetCounter.total, (screen.height-280)/devices.length,20))})
   			  .call(dragDrop)
			  .style("stroke", "#25a9af")
			  .style("stroke-width",function(d) {return Math.max(1,Math.min(d.packetCounter.total/50,3))})
			  .style("fill","#ffffff")
			  .style("cursor","pointer")
			  .on ("mouseover", function(d){
				  	$("#"+d.idx).css('fill','#25a9af');
                    div	.transition()
						.duration(200)
						.style("opacity", .9)
                    div	.html(d.mac)
						.style("left", (d.x + d.packetCounter.total) + "px")
					.style("top", (d.y + d.packetCounter.total) + "px");	})
			  .on("mouseout", function(d) {
					$("#"+d.idx).css('fill','#ffffff');
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
              .force("charge", d3.forceManyBody().strength(function(d){return +5}))         // This adds repulsion between nodes. Play with the -400 for the repulsion strength
			  .force("center", d3.forceCenter((screen.width-300) / 2 - 20, (screen.height-280) /2))     // This force attracts nodes to the center of the svg area
              .force("Collide", d3.forceCollide(function(d) {return Math.max(2,Math.min(d.packetCounter.total, (screen.height-280)/devices.length)) * 2 * 1.2}))
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
			 .attr("cx", function (d) { return d.x+10; })
			 .attr("cy", function(d) { return d.y-10; });
	  }
	  
 }
 
 function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send(null);
    return xmlHttp.responseText;
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


/*function loadJSONs(networksFilter){
	loadJSON('js/data/db/Example/devices.json',function(response) {
    devices = JSON.parse(response);
	console.log(devices);
	loadJSON('js/data/db/Example/links.json',function(response) {
    links = JSON.parse(response);
	for (var i = 0; i<links.length; i++) {
    links[i].source = links[i].sourceDeviceIdx;
    links[i].target = links[i].targetDeviceIdx;
    delete links[i].sourceDeviceIdx;
    delete links[i].targetDeviceIdx;
	}
	printGraph(networksFilter);
});
	});
 }
*/
loadData(null);
function loadData(networksFilter){
	networkIds=[];
	devices=[];
	links = [];
	var response = httpGet('/api/overview');
	var obj = JSON.parse(response);
	var networks = obj.networks;
	for (var i = 0; i < networks.length; i++) 
		networkIds.push(networks[i]['uuid'].toString());
	obj = null;
	for (id in networkIds){
		var currId = networkIds[id];
		obj = JSON.parse(httpGet('/api/networks/' + currId));
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
    buildHtmlTable('#devicesTable',devices);
	printGraph(networksFilter);
};
