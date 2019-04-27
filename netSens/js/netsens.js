function buildHtmlTable(selector,devices) {
  var columns = addAllColumnHeaders(devices, selector);
  for (var i = 0; i < devices.length; i++) {
    var row$ = $('<tr/>');
    for (var colIndex = 0; colIndex < columns.length; colIndex++) {
      var cellValue = devices[i][columns[colIndex]];
	  console.log('in');
	  if ((colIndex == 5) || (colIndex == columns.length - 1))
	  {
		var date = new Date(cellValue*1000);
		var minutes = "0" + date.getMinutes();
		var seconds = "0" + date.getSeconds();

		var cellValue = date.getDate() + '/' + date.getMonth() + ' ' + date.getHours() + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
	  }
      if (cellValue == null) cellValue = "";
      row$.append($('<td/>').html(cellValue));
    }
    $(selector).append(row$);
  }
}

// Adds a header row to the table and returns the set of columns.
// Need to do union of keys from all records as some records may not contain
// all records.
function addAllColumnHeaders(devices, selector) {
  var columnSet = [];
  var headerTr$ = $('<tr/>');

  for (var i = 0; i < devices.length; i++) {
    var rowHash = devices[i];
    for (var key in rowHash) {
      if ($.inArray(key, columnSet) == -1) {
        columnSet.push(key);
        headerTr$.append($('<th/>').html(key));
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
loadJSON('devices.json',function(response) {
    var devices = JSON.parse(response);
    loadJSON('links.json',function(response) {
    var links = JSON.parse(response);
    const urlParams = new URLSearchParams(window.location.search);
    const myParam = urlParams.get('device');
    console.log(myParam);
    buildHtmlTable('#devicesTable',devices);

// append the svg object to the body of the page
var svg = d3.select("#devicesGraph")
.append("svg")
  .attr("width", screen.width - 100)
  .attr("height", 200);

          // Initialize the links
          var link = svg
            .selectAll("line")
            .data(links)
            .enter()
            .append("line")
              .style("stroke", "#000000")
              .style("stroke-width", "1.5")
          var div = d3.select("#devicesGraph").append("div")
            .attr("class", "device-tooltip")
            .style("opacity", 0);
          // Initialize the nodes
          var node = svg
            .selectAll("circle")
            .data(devices)
            .enter()
            .append("circle")
              .attr("r", 5)
              .style("fill", "#000000")
			  .style("cursor","pointer")
              .on("mouseover", function(d) {
                    div.transition()
                        .duration(200)
                        .style("opacity", .9);
                    div	.html(d.ip + '(' + d.mac + ')')
                        .style("left", (d3.event.pageX - 252) + "px")
                        .style("top", (d3.event.pageY - 170) + "px");
						
                    })
                .on("mouseout", function(d) {
                    div.transition()
                        .duration(500)
                        .style("opacity", 0);
                })
                .on("click",function(d) {
                window.location.href = "/devices.html?device=" + d.mac;
                });

          // Let's list the force we wanna apply on the network
          var simulation = d3.forceSimulation(devices)                 // Force algorithm is applied to data.nodes
              .force("link", d3.forceLink()                               // This force provides links between nodes
                    .id(function(d) {return d.id; })                     // This provide  the id of a node
                    .links(links)                                    // and this the list of links
              )
              .force("charge", d3.forceManyBody().strength(-5))         // This adds repulsion between nodes. Play with the -400 for the repulsion strength
              .force("center", d3.forceCenter((screen.width - 300) / 2, 100))     // This force attracts nodes to the center of the svg area
              .force("Collide", d3.forceCollide(10))
              .nodes(devices)
              .on("tick", ticked);


          // This function is run at each iteration of the force algorithm, updating the nodes position.
          function ticked() {
            link
                .attr("x1", function(d) { return d.source.x + 5; })
                .attr("y1", function(d) { return d.source.y - 5; })
                .attr("x2", function(d) { return d.target.x + 5 ; })
                .attr("y2", function(d) { return d.target.y - 5; });

            node
                 .attr("cx", function (d) { return d.x+5; })
                 .attr("cy", function(d) { return d.y-5; });
          }
          });

});