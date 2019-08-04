var arrayConstructor = [].constructor;
var objectConstructor = {}.constructor;

$('#exampleModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget);
  //var devdata = button.data('whatever');
  var modal = $(this);
  console.log(selectedDevice);
  modal.find('.modal-title').text('Device Info ' + selectedDevice.mac);
  $("#label_id").text(selectedDevice.id);
  $("#label_id2").text(selectedDevice.mac);
  $("#label_id3").text(selectedDevice.ip);
  $("#label_id4").text(selectedDevice.vendor);
  $("#label_id5").text(JSON.stringify(selectedDevice.extraData));
  $("#label_id6").text(selectedDevice.dhcpFingerPrint);
  
  var fistdate = new Date(selectedDevice.firstTimeSeen*1000);
		var minutes = "0" + fistdate.getMinutes();
		var seconds = "0" + fistdate.getSeconds();
		var fistdatecellValue = fistdate.getDate() + '/' + fistdate.getMonth() + ' ' + fistdate.getHours() + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
  
  $("#label_id7").text(fistdatecellValue);
    
  var lastdate = new Date(selectedDevice.lastTimeSeen*1000);
		var minutes = "0" + lastdate.getMinutes();
		var seconds = "0" + lastdate.getSeconds();
		var lastdatecellValue = lastdate.getDate() + '/' + lastdate.getMonth() + ' ' + lastdate.getHours() + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
  
  $("#label_id8").text(lastdatecellValue);
});

function findElement(arr, propName, propValue) {
  for (var i=0; i < arr.length; i++)
    if (arr[i][propName] == propValue)
      return arr[i];

  // will return undefined if not found; you could return a default instead
}


function buildHtmlTable(selector,devices) {
  var columns = addAllColumnHeaders(devices, selector);
  for (var i = 0; i < devices.length; i++) {
    var row$ = $('<tr/>');
	var cellValue = devices[i].networkId;
	cellValue = devices[i].networkId;
	row$.append($('<td/>').html(cellValue));

	cellValue = devices[i].id;
	row$.append($('<td/>').html(cellValue));
	
	var date = new Date(devices[i].firstTimeSeen*1000);
	var minutes = "0" + date.getMinutes();
	var seconds = "0" + date.getSeconds();

	cellValue = date.getDate() + '/' + date.getMonth() + ' ' + date.getHours() + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
	row$.append($('<td/>').html(cellValue));
	
	var date = new Date(devices[i].lastTimeSeen*1000);
	var minutes = "0" + date.getMinutes();
	var seconds = "0" + date.getSeconds();

	cellValue = date.getDate() + '/' + date.getMonth() + ' ' + date.getHours() + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
	row$.append($('<td/>').html(cellValue));
	
	cellValue = devices[i].ip;
	row$.append($('<td/>').html(cellValue));
	
	cellValue = devices[i].mac;
	row$.append($('<td/>').html(cellValue));
	
	cellValue = devices[i].vendor;
	row$.append($('<td/>').html(cellValue));
	
	cellValue = JSON.stringify(devices[i].extraData);
	row$.append($('<td/>').html(cellValue));
	
	//cellValue = devices[i].dhcpFingerPrint;
	//if (cellValue == null){
	//	cellValue ="";
	//}
	//row$.append($('<td/>').html(cellValue.toString()));

	$(selector).append(row$);
	}
}
// Adds a header row to the table and returns the set of columns.
// Need to do union of keys from all records as some records may not contain
// all records.
function addAllColumnHeaders(devices, selector) {
  var columnSet = [];
  
  var headerTr$ = $('<thead style="background-color:#25a9af; color:white;"/>');
  headerTr$.append($('<tr/>'));

  for (var i = 0; i < devices.length; i++) {
    var rowHash = devices[i];
    for (var key in rowHash) {
      if ($.inArray(key, columnSet) == -1) {
		if (key != "isClosed" && key != "hits" && key != "arpHits" && key != "dhcpHits" && key!="dhcpFingerPrint"){
        columnSet.push(key);
        headerTr$.append($('<th/>').html(key));
		}
      }
    }
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
            // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
            callback(xobj.responseText);
          }
    };
    xobj.send(null);
 }
var devices="";
var selectedDevice ="";
loadJSON('devices1.json',function(response) {
    devices = JSON.parse(response);
	console.log(devices);
    loadJSON('links.json',function(response) {
    var links = JSON.parse(response);
	console.log(links);
    const urlParams = new URLSearchParams(window.location.search);
    const myParam = urlParams.get('device');
    console.log(myParam);
    buildHtmlTable('#devicesTable',devices);
    console.log(myParam);

	
// append the svg object to the body of the page
var svg = d3.select("#devicesGraph")
.append("svg")
  .attr("width", screen.width - 300)
  .attr("height", screen.height - 280);

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
              .attr("id", function(d){return d.id})
			  .attr("r", function(d) {return Math.max(6,Math.min(d.hits, 500/devices.length))})
              .style("stroke", "#25a9af")
			  .style("stroke-width",function(d) {return Math.max(1,d.hits/20)})
			  .style("fill","#ffffff")
			  .style("cursor","pointer")
              .on("mouseover", function(d) {
					$("#"+d.id).css('fill','#25a9af');
                    div.transition()
                        .duration(200)
                        .style("opacity", .9)
                    div	.html(d.mac)
                        .style("left", (d.x + d.hits) + "px")
                        .style("top", (d.y + d.hits) + "px");
						
                    })
                .on("mouseout", function(d) {
					$("#"+d.id).css('fill','#ffffff');
                    div.transition()
                        .duration(500)
                        .style("opacity", 0);
                })
                .on("click",function(d) {
				selectedDevice = findElement(devices,"mac",d.mac);
				$("#btnt").click();
                });

          // Let's list the force we wanna apply on the network
          var simulation = d3.forceSimulation(devices)                 // Force algorithm is applied to data.nodes
              .force("link", d3.forceLink()                               // This force provides links between nodes
                    .id(function(d) {return d.id; })                     // This provide  the id of a node
                    .links(links)                                    // and this the list of links
              )
              //.force("charge", d3.forceManyBody().strength(function(d){return 0}))         // This adds repulsion between nodes. Play with the -400 for the repulsion strength
              .force("center", d3.forceCenter((screen.width-300) / 2 - 20, (screen.height-280) /2))     // This force attracts nodes to the center of the svg area
              .force("Collide", d3.forceCollide(function(d) {return Math.max(10,Math.min(d.hits, 1000/devices.length)) + 20}))
              .nodes(devices)
              .on("tick", ticked);


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
          });

});
