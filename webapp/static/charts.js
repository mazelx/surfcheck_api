 var api = "https://surfcheck-api.herokuapp.com/surfchecks";
            //var api = "http://localhost:5001/surfchecks";


            d3.json(api, function (json_data) {
                var width=700;
                var height=200;
                var data = json_data;
                var minDate =  new Date(data[0].datetime),
                    maxDate = new Date(data[data.length-1].datetime);
                // Largeur et hauteur

                var chart_margin = {top: 0, right: 0, bottom: 0, left: 0};
                var chart_weight = width - chart_margin.left - chart_margin.right
                var chart_height = height - chart_margin.top - chart_margin.bottom;
                var barPadding = 1;

                // Parse the date / time
                // var parseDate = d3.time.format("%Y-%m-%dT%H:%M:%S.%LZ").parse;

                // scale
                var whScale = d3.scale.linear()
                        .domain([0, 3])
                        .range([chart_height, 0]);
                var wpScale = d3.scale.linear()
                        .domain([0, 18])
                        .range([chart_height, 0]);
                var dtScale = d3.time.scale().domain([minDate, maxDate]).range([0, chart_weight]);

                // axis
                var yAxis = d3.svg.axis()
                  .scale(whScale)
                  .orient("left");
                var xAxis = d3.svg.axis()
                    .scale(dtScale)
                    .orient("bottom")
                    .tickFormat(d3.time.format("%d-%m %H:%M"));

                // chart and axis group
                var charts = d3.selectAll(".chart-container")
                               .append("g")
                               .attr("class", "chart")
                               .attr("transform", "translate(" + chart_margin.left + "," + chart_margin.top + ")");

                // wave height chart
                var whChart = d3.select("#chart-wave-height")
                var whChartData = whChart.append("g")
                    .selectAll("rect")
                    .data(data)
                    .enter()

                // wave height chart max
                whChartData.append("rect")
                    .attr("class", "bar height-max")
                    .attr("data-wave_height-max", function(d) {return d.wave_height_max})
                    // .attr("fill", "teal")
                    // .attr("fill", function(d) {
                    //     return "rgb(" + (255 - Math.round(d.wave_period * 17)) + ", 0, 0)"; //15s = 255
                    // })
                    .attr("x", 0)
                    .attr("y", function(d) {
                        return whScale(d.wave_height_max);
                    })
                    .attr("width", chart_weight / data.length - barPadding)
                    .attr("height", function(d) {
                        return chart_height - whScale(d.wave_height_max);
                    })
                    .attr("x", function(d, i) {
                        return i * (chart_weight / data.length);
                    });

                 // wave height chart
                whChartData.append("rect")
                    .attr("class", function(d, i) {
                        if(i == data.length - 1) {
                            return "bar active";
                        }
                        return "bar";
                    })
                    .attr("data-wave_height", function(d) {return d.wave_height})
                    // .attr("fill", "teal")
                    // .attr("fill", function(d) {
                    //     return "rgb(" + (255 - Math.round(d.wave_period * 17)) + ", 0, 0)"; //15s = 255
                    // })
                    .attr("x", 0)
                    .attr("y", function(d) {
                        return whScale(d.wave_height);
                    })
                    .attr("width", chart_weight / data.length - barPadding)
                    .attr("height", function(d) {
                        return chart_height - whScale(d.wave_height);
                    })
                    .attr("x", function(d, i) {
                        return i * (chart_weight / data.length);
                    })


                // wave period chart
                var wpChart = d3.select("#chart-wave-period")
                wpChart.append("g")
                    .selectAll("rect")
                    .data(data)
                    .enter()
                    .append("rect")
                    .attr("class", function(d, i) {
                        if(i == data.length - 1) {
                            return "bar active";
                        }
                        return "bar";
                    })
                    .attr("data-wave_period", function(d) {return d.wave_period})
                    // .attr("fill", "teal")
                    // .attr("fill", function(d) {
                    //     return "rgb(" + (255 - Math.round(d.wave_period * 17)) + ", 0, 0)"; //15s = 255
                    // })
                    .attr("x", 0)
                    .attr("y", function(d) {
                        return wpScale(d.wave_period);
                    })
                    .attr("width", chart_weight / data.length - barPadding)
                    .attr("height", function(d) {
                        return chart_height - wpScale(d.wave_period);
                    })
                    .attr("x", function(d, i) {
                        return i * (chart_weight / data.length);
                    });


                // // Y axis
                // chart.append("g")
                //     .attr("class", "y axis")
                //     .call(yAxis);
                // // X axis
                // chart.append("g")
                //     .attr("class", "x axis")
                //     .attr("transform", "translate(0," + chart_height + ")")
                //     .call(xAxis)

                // wave height indicator
                d3.select("#ind-wave-height")
                    .selectAll("div")
                    .data(data)
                    .enter()
                    .append("div")
                    .attr("class", function(d, i) {
                        if(i == data.length - 1) {
                            return "indicator-text";
                        }
                        return "indicator-text invisible";
                    })
                    .text(function(d) {
                        return d.wave_height + 'm';
                    });
                    // wave height indicator
                d3.select("#ind-wave-period")
                    .selectAll("div")
                    .data(data)
                    .enter()
                    .append("div")
                    .attr("class", function(d, i) {
                        if(i == data.length - 1) {
                            return "indicator-text";
                        }
                        return "indicator-text invisible";
                    })
                    .text(function(d) {
                        return d.wave_period + 's';
                    });
            })