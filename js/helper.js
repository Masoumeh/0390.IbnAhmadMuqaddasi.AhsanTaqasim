/**
 * Created by masum on 11.02.16.
 */
// make a unique list of countries(names) for people in a specific year
// starting from a yearPeople map(year to people ids) to peopleMap (people to year + country (name))
function unify_year_people(minyear,maxyear,yearPeople,peopleMap) {
    var uniqueCountries = {};
    for (var i = minyear; i <= maxyear; i++) {
        if (yearPeople[i + ''] != undefined) {
            var arr = yearPeople[i + '']['id'].split(',');
            arr.forEach(function (d) {
                var city = peopleMap[d]['city'].split(',');
                city.forEach(function (d) {
                    if (uniqueCountries[d] == undefined)
                        uniqueCountries[d] = 0;
                    // counts the number of countries in a map
                    else uniqueCountries[d]++;
                });
            });
        }
    }
    return uniqueCountries;
}

function createMatrix(postdata) {
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

    return new Graph(edgeMap);
}

function calcPathSize(d, uniquePaths ) {
    //var pathscale = d3.scale.linear()
    //    .domain([d3.min(d3.values(uniquePaths)),d3.max(d3.values(uniquePaths))])
    //    .range([1,20]);
    var pathscale = d3.scale.linear().domain([1,15]).range([1,10]);
    // To consider the paths from A to B and B to A as one path
    var tmp1 = uniquePaths[d.properties.sToponym
    +","+ d.properties.eToponym];
    var tmp2 = uniquePaths[d.properties.eToponym
    +","+ d.properties.sToponym];
    var size;
    if(tmp1==undefined && tmp2==undefined) {size = 0}
    else {
        if(tmp1==undefined)
            size = pathscale(tmp2);
        else size = pathscale(tmp1);
    }
    return size;
}

function calcPathSizeForColors(d, uniquePaths ) {
    //var pathscale = d3.scale.linear()
    //    .domain([d3.min(d3.values(uniquePaths)),d3.max(d3.values(uniquePaths))])
    //    .range([1,20]);
    var pathscale = d3.scale.linear().domain([1,15]).range([1,20]);
    // To consider the paths from A to B and B to A as one path
    var tmp1 = uniquePaths[d.properties.sToponym
    +","+ d.properties.eToponym];
    var tmp2 = uniquePaths[d.properties.eToponym
    +","+ d.properties.sToponym];
    var size;
    if(tmp1==undefined && tmp2==undefined) {size = 0}
    else {
        if(tmp1==undefined)
            size = pathscale(tmp2);
        else size = pathscale(tmp1);
    }
    return size;
}

function displayPath(pathData, countries, uniquePaths) {
    //console.log("countries: " + JSON.stringify(d3.values(countries)));
    //console.log("uniqPaths: "+JSON.stringify(uniquePaths));
    var rscale = d3.scale.linear()
        .domain(d3.extent(d3.values(countries)))
        .range([5,30]);

    var colorScale = d3.scale.linear()
        .domain(d3.extent(d3.values(uniquePaths)))
        .range(["darkseagreen", "darkgreen"])
        .interpolate(d3.interpolateHcl);

    //Initial fill of all circles
    d3.selectAll("circle").transition().duration(1000)
        .style("fill", "seagreen")
        .attr("r",5);
    //
    d3.selectAll("path").filter(function (d) {
        return pathData.indexOf(d.properties.sToponym) === -1
            || pathData.indexOf(d.properties.eToponym) === -1;
    }).transition().duration(1000).style("stroke-width", 0); // or display property?

    if (pathData) {
        d3.selectAll("path").filter(function (d) {
            return pathData.indexOf(d.properties.sToponym) > -1
                && pathData.indexOf(d.properties.eToponym) > -1;
        }).transition().duration(2000).style("stroke", function (d) {
            var size = calcPathSizeForColors(d, uniquePaths);
            return colorScale(size);
        }).style("stroke-width", function (d) {
                return calcPathSize(d, uniquePaths);
        });

        d3.selectAll("circle").filter(function (d) {
            return pathData.indexOf(d.topURI) > -1
        }).transition().duration(2000)
            .style("fill", "orange")
            .style("stroke", "orange")
            .attr("r", function (d) {
                var size = (parseInt(countries[d['topURI']]));
                if (isNaN(size)) return 5;
                return rscale(size);
            });

        d3.selectAll("circle").filter(function (d) {
            return (pathData.indexOf(d.topURI) <= -1 // is this line needed to be checked? for 949 to 1300 it seems it's needed!
            || Object.keys(countries).indexOf(d.topURI) <= -1 )
        }).transition().duration(2000)
            .attr("r", "0");

        var pDataArray = d3.selectAll("path").filter(function (d) {
            return pathData.indexOf(d.properties.sToponym) > -1
                && pathData.indexOf(d.properties.eToponym) > -1
        }).data();
        // var totalLength = d3.sum(pDataArray, function(d) {return d.properties.cost});
        // d3.select("#pathdata").html("<span style='font-weight: 900'>Total Distance:</span> " + formatter(totalLength) + "km");
    }
    //else {
    //    d3.select("#personSlider").html("NO ROUTE");
    //}
}

function displayPathArc(pathData, countries, uniquePaths) {
    displayPath(pathData,countries,uniquePaths);
    ////console.log("countries: " + JSON.stringify(d3.values(countries)));
    ////console.log("uniqPaths: "+JSON.stringify(uniquePaths));
    ////
    ////console.log("test" +
    ////    JSON.stringify(d3.selectAll("path")[0][0]['__data__']['properties']['coordinates']));
    //
    //var rscale = d3.scale.linear()
    //    .domain(d3.extent(d3.values(countries)))
    //    .range([5, 40]);
    //
    //var colorScale = d3.scale.linear()
    //    .domain(d3.extent(d3.values(uniquePaths)))
    //    .range(["darkseagreen", "darkgreen"])
    //    .interpolate(d3.interpolateHcl);
    //
    ////Initial fill of all circles
    //d3.selectAll("circle").transition().duration(1000)
    //    .style("fill", "seagreen")
    //    .attr("r", 5);
    ////
    ////d3.selectAll("path").filter(function (d) {
    ////    return pathData.indexOf(d.properties.sToponym) === -1
    ////        && pathData.indexOf(d.properties.eToponym) === -1;
    ////}).transition().duration(1000).style("stroke", 0); // or display property?
    ////d3.selectAll("path").style("display", "none");
    //
    ////if (pathData) {
    ////d3.selectAll("path").filter(function (d) {
    ////    return pathData.indexOf(d.properties.sToponym) > -1
    ////        && pathData.indexOf(d.properties.eToponym) > -1;
    ////}).transition().duration(2000).style("stroke", function (d) {
    ////    var size = calcPathSize(d, uniquePaths);
    ////    return colorScale(size);
    ////}).style("stroke-width", function (d) {
    ////    return calcPathSize(d, uniquePaths);
    ////});
    //
    //d3.selectAll("circle").filter(function (d) {
    //    return pathData.indexOf(d.topURI) > -1
    //}).transition().duration(2000)
    //    .style("fill", "orange")
    //    .style("stroke", "orange")
    //    .attr("r", function (d) {
    //        var size = (parseInt(countries[d['topURI']]));
    //        if (isNaN(size)) return 5;
    //        return rscale(size);
    //    });
    //
    //links = [];
    //Object.keys(uniquePaths).forEach(function (d) {
    //    var tmp = d.split(",");
    //    var start = tmp[0];
    //    var end = tmp[1];
    //    var test = d3.selectAll("circle").filter(function (d) {
    //        return d.topURI == start;
    //    });
    //    var start_lat = test[0][0]['__data__']['lat'];
    //    var start_lon = test[0][0]['__data__']['lon'];
    //
    //    test = d3.selectAll("circle").filter(function (d) {
    //        return d.topURI == end;
    //    });
    //    var end_lat = test[0][0]['__data__']['lat'];
    //    var end_lon = test[0][0]['__data__']['lon'];
    //
    //    links.push({
    //        type: "LineString",
    //        coordinates: [
    //            [start_lon, start_lat],
    //            [end_lon, end_lat]
    //        ]
    //    });
    //});
    ////mylayer = d3.carto.layer.topojson();
    ////mylayer
    ////    .featureArray(links)
    ////    .cssClass("roads")
    ////    .renderMode("svg")
    ////    .on("load", function() {
    ////            alert("here");
    ////        });
    ////map.addCartoLayer(mylayer);
    //
    //
    //var projection = d3.geo.albersUsa()
    //    .scale(1070);
    //var path = d3.geo.path()
    //    .projection(projection);
    //d3.selectAll("path")
    //    .data(links)
    //    .enter()
    //    .append("path")
    //    .attr("d",path);
    //
    //
    ////d3.selectAll("path").
    ////    enter().append("path")
    ////    .attr("r", 5)
    ////    .style("fill", "red");
    ////  //  data(links);//.style("stroke","10px");
    //
    //d3.selectAll("circle").filter(function (d) {
    //    // is this line needed to be checked? for 949 to 1300 it seems it's needed!
    //    return (pathData.indexOf(d.topURI) <= -1
    //    || Object.keys(countries).indexOf(d.topURI) <= -1 )
    //}).transition().duration(2000)
    //    .attr("r", "0");
    //
    ////var pDataArray = d3.selectAll("path").filter(function (d) {
    ////    return pathData.indexOf(d.properties.sToponym) > -1
    ////        && pathData.indexOf(d.properties.eToponym) > -1
    ////}).data();
    //// var totalLength = d3.sum(pDataArray, function(d) {return d.properties.cost});
    //// d3.select("#pathdata").html("<span style='font-weight: 900'>Total Distance:</span> " + formatter(totalLength) + "km");
    //
    ////else {
    ////    d3.select("#personSlider").html("NO ROUTE");
    ////}
}

function updateRoutesCountries(countries,graph) {
    var country = Object.keys(countries);
    var pathData = [];
    var uniquePaths = {};

    if (d3.select('input[name="pathvis"]:checked')[0][0].value == 0) {
        for (var x = 0; x < country.length; x++) {
            for (var y = x + 1; y < country.length; y++) {
                var pData = graph.findShortestPath(country[x], country[y]);
                if (pData) {
                    for (var i = 0; i < pData.length; i++) {
                        for (var j = i + 1; j < pData.length; j++) {
                            // Check both i to j and j to i paths
                            // to prevent counting a path two times
                            if (uniquePaths[pData[i] + "," + pData[j]] == undefined) {
                                if (uniquePaths[pData[j] + "," + pData[i]] != undefined) {
                                    // adds counter to one of the ij/ji paths
                                    uniquePaths[pData[j] + "," + pData[i]]++;
                                } else {
                                    uniquePaths[pData[j] + "," + pData[i]] = 1;
                                }
                            } else {
                                uniquePaths[pData[i] + "," + pData[j]]++;
                            }
                        }
                    }
                    // concats new path to the array of pathData
                    pathData = pathData.concat(pData);
                }
            }
        }
        displayPath(pathData, countries, uniquePaths);
    } else {
        for (var x = 0; x < country.length; x++) {
            pathData = pathData.concat(country[x]);
            for (var y = x + 1; y < country.length; y++) {
                var pData = graph.findShortestPath(country[x], country[y]);
                if (pData) {
                    if (uniquePaths[country[x] + "," + country[y]] == undefined) {
                        if (uniquePaths[country[y] + "," + country[i]] != undefined) {
                            // adds counter to one of the ij/ji paths
                            uniquePaths[country[y] + "," + country[x]]++;
                        } else {
                            uniquePaths[country[x] + "," + country[y]] = 1;
                        }
                    } else {
                        uniquePaths[country[i] + "," + country[j]]++;
                    }
                }
            }
        }

        displayPathArc(pathData, countries, uniquePaths);
    }
}

function updateRoutes(id) {
    var trav = 0;
    d3.selectAll("path").transition().duration(1000).style("stroke", function (d, i) {
        return "black"
    }).style("stroke-width", "2px");

    var country = peopleMap[id]['city'].split(',');
    for (var x = 0; x < country.length; x++) {
        for (var y = x + 1; y < country.length; y++) {
            var pData = graph.findShortestPath(country[x], country[y]);
            trav++;
            if (pData) {
                //console.log("pathdata: ", JSON.stringify(pData));
                displayPath(pData);
            }
        }
    }
}

// Building initial map structures
function dataStructsBetweenPeopleYears(data) {
    var min_year = 2000, max_year = 0;
    // A map from people to assigned year and name (now just toponyms)
    var peopleMap = {};
    // A map from year to people assigned to that year
    var yearPeople = {};
    data.forEach(function (d) {
        // Group the years to decades
        var diedAtDecade = d.diedAt - (d.diedAt % 10);
        if (peopleMap[d.id] != undefined) {
            peopleMap[d.id] = {
                'diedAt': diedAtDecade,
                'city': peopleMap[d.id]['city'] + ',' + d.city
            };
        } else {
            peopleMap[d.id] = {'diedAt': diedAtDecade, 'city': d.city};
        }

        if (yearPeople[diedAtDecade] != undefined) {
            yearPeople[diedAtDecade] = {'id': yearPeople[diedAtDecade]['id'] + ',' + d.id};
        } else {
            yearPeople[diedAtDecade] = {'id': d.id};
        }

        var year = parseInt(diedAtDecade);
        if (year < min_year) min_year = year;
        if (year > max_year) max_year = year;
    });
    var output = {};
    output['min_year']=min_year;
    output['max_year']=max_year;
    output['peopleMap']=peopleMap;
    output['yearPeople']=yearPeople;
    return output;
}
