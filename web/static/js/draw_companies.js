    var margin = {top: 5, right: 40, bottom: 20, left: 120},
        width = 960 - margin.left - margin.right,
        height = 50 - margin.top - margin.bottom;

    var chart = d3.bullet()
        .width(width)
        .height(height);

    var callback = function(data) {
      console.log(data)
      var svg = d3.select("#plot").selectAll("svg")
          .data(data)
        .enter().append("svg")
          .attr("class", "bullet")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
        .append("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
          .call(chart);

      var title = svg.append("g")
          .style("text-anchor", "end")
          .attr("transform", "translate(-6," + height / 2 + ")");

      title.append("text")
          .attr("class", "title")
          .text(function(d) { return d.title; });

      title.append("text")
          .attr("class", "subtitle")
          .attr("dy", "1em")
          .text(function(d) { return d.subtitle; });

    }

    d3.json("/get_companies", callback);