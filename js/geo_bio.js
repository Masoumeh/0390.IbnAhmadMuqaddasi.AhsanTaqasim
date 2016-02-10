/**
 * Created by masoumeh on 10.02.16.
 */

function createMatrix() {
    postdata = postLayer.features();
    edgeList = [];
    edgeMap = {};

    nodeHash = {};
    for (x in postdata) {
        var line = postdata[x].geometry.coordinates;
        var sName = postdata[x].properties.sToponym;
        var eName = postdata[x].properties.eToponym;
        var lS = line[0];
        var lE = line[line.length - 1];
        var nA = [lS, lE];
        var cost = d3.geo.length(postdata[x]) * 6371;
        if (edgeMap[sName]) {
            edgeMap[sName][eName] = cost;
        }
        else {
            edgeMap[sName] = {};
            edgeMap[sName][eName] = cost;
        }
        if (edgeMap[eName]) {
            edgeMap[eName][sName] = cost;
        }
        else {
            edgeMap[eName] = {};
            edgeMap[eName][sName] = cost;
        }
    }

    graph = new Graph(edgeMap);
    cityLayer = d3.carto.layer.csv();
    cityLayer.path("../Data/cornu.csv")
        .label("Cities")
        .cssClass("metro")
        .renderMode("svg")
        .x("lon")
        .y("lat")
        //.clickableFeatures(true)
        .on("load", function () {

        });
    map.addCartoLayer(cityLayer);
}

function displayPath(pathData,countries) {
    d3.selectAll("circle").transition().duration(1000)
        .style("fill", "green")
        .attr("r",5);

    if (pathData) {
        d3.selectAll("path").filter(function (d) {
            return pathData.indexOf(d.properties.sToponym) > -1 && pathData.indexOf(d.properties.eToponym) > -1;
        }).transition().duration(2000).style("stroke", "red").style("stroke-width", 3);
        d3.selectAll("circle").filter(function (d) {
            return pathData.indexOf(d.topURI) > -1
        }).transition().duration(2000)
            .style("fill", "red")
            .attr("r", function(d) {
                var size = (parseInt(countries[d['topURI']]));
                if(isNaN(size)) return 5;
                if(size > 1000) {size = size / 50}
                else {size = size/2;}
                return size+''});

        var pDataArray = d3.selectAll("path").filter(function (d) {
            return pathData.indexOf(d.properties.sToponym) > -1 && pathData.indexOf(d.properties.eToponym) > -1
        }).data();
        // var totalLength = d3.sum(pDataArray, function(d) {return d.properties.cost});
        // d3.select("#pathdata").html("<span style='font-weight: 900'>Total Distance:</span> " + formatter(totalLength) + "km");
    }
    else {
        d3.select("#personSlider").html("NO ROUTE");
    }
}

function makeSomeMaps() {
    pathSource = 0;
    //var dijSource, dijTarget;
    map = d3.carto.map();
    d3.select("#geoMap").call(map);
    map.centerOn([44.361488, 33.312806], "latlong");
    map.setScale(4);
    map.refresh();
    wcLayer = d3.carto.layer.tile();
    wcLayer
        .tileType("stamen")
        .path("watercolor")
        .label("Watercolor")
        .visibility(true);
    postLayer = d3.carto.layer.topojson();
    postLayer
        .path("../Data/all_routes_new.topojson")
        .label("Postal Routes")
        .cssClass("roads")
        .renderMode("svg")
        .on("load", createMatrix);
    map.addCartoLayer(wcLayer).addCartoLayer(postLayer);
    nodes = [];

    d3.csv("../Data/peopleRegion.csv", function (error, data) {
        if (error) throw error;
        var people = [];
        var cnt = 0;
        var min_year = 2000, max_year = 0;
        var peopleMap = {};
        var yearPeople = {};
        data.forEach(function (d) {
            if (peopleMap[d.id] != undefined) {
                peopleMap[d.id] = {'diedAt': d.diedAt,
                    'city': peopleMap[d.id]['city'] + ',' + d.city};
            } else {
                peopleMap[d.id] = {'diedAt': d.diedAt, 'city': d.city};
            }

            if (yearPeople[d.diedAt] != undefined) {
                yearPeople[d.diedAt] = {'id': yearPeople[d.diedAt]['id'] + ',' + d.id};
            } else {
                yearPeople[d.diedAt] = {'id': d.id};
            }

            var year = parseInt(d.diedAt);
            if (year < min_year) min_year = year;
            if (year > max_year) max_year = year;
        });

        d3.select("#personSlider")
            .append('div')
            .call(d3.slider().value([0, 100])
                .on("slide", function (evt, value) {
                    d3.select('#yearValue').text("from "
                        + parseInt(value[0] + min_year) * parseInt((max_year - min_year) / 100) + " to "
                        + parseInt(value[1] + min_year) * parseInt((max_year - min_year) / 100));
                })
                .on("slideend", function (evt, value) {
                    var uniqueCountires = {};
                    var minyear = parseInt(value[0] + min_year) * parseInt((max_year - min_year) / 100);
                    var maxyear = parseInt(value[1] + min_year) * parseInt((max_year - min_year) / 100);
                    for (var i = minyear; i <= maxyear; i++) {
                        if (yearPeople[i + ''] != undefined) {
                            var arr = yearPeople[i + '']['id'].split(',');
                            arr.forEach(function (d) {
                                console.log("test "+JSON.stringify(peopleMap));
                                var city = peopleMap[d]['city'].split(',');
                                city.forEach(function (d) {
                                    if (uniqueCountires[d] == undefined)
                                        uniqueCountires[d] = 0;
                                    else uniqueCountires[d]++;
                                });
                            });
                        }
                    }
                    updateRoutesCountries(uniqueCountires);
                })
        );

        d3.select('#sourceSelectParent')
            .append('div')
            .attr('id', 'yearValue')
            .text('from ' + min_year + ' to ' + max_year);

        var select = d3.select("#personSlider")
            .append('div')
            .append("select")
            .on("change", function (d) {
                var id = this.options[this.selectedIndex].value;
                updateRoutes(id);
            });

        var options = select.selectAll("option").data(Object.keys(peopleMap));
        options.enter()
            .append("option")
            .text(function (d) {
                return d;
            });

        function updateRoutesCountries(countries) {
            d3.selectAll("path").transition().duration(1000).style("stroke", function (d, i) {
                return "black"
            }).style("stroke-width", "2px");
            var country = Object.keys(countries);
            for (var x = 0; x < country.length; x++) {
                for (var y = x + 1; y < country.length; y++) {
                    var pData = graph.findShortestPath(country[x], country[y]);
                    if(pData) {
                        displayPath(pData, countries);
                    }
                }
            }
        }

        function updateRoutes(id) {
            var trav = 0;
            d3.selectAll("path").transition().duration(1000).style("stroke", function (d, i) {
                return "black"
            }).style("stroke-width", "2px");

            var country = peopleMap[id]['country'].split(',');
            for (var x = 0; x < country.length; x++) {
                for (var y = x + 1; y < country.length; y++) {
                    var pData = graph.findShortestPath(country[x], country[y]);
                    trav++;
                    if(pData) {
                        displayPath(pData);
                    }
                }
            }
        }
    });
}



