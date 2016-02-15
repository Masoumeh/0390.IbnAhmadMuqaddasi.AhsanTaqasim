/**
 * Created by masum on 11.02.16.
 */
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

function displayPath(pathData,countries) {
    var rscale = d3.scale.linear()
        .domain([1,1000])
        .range([3,40]);
    d3.selectAll("circle").transition().duration(1000)
        .style("fill", "green")
        .attr("r",5);

    if (pathData) {
        d3.selectAll("path").filter(function (d) {
            return pathData.indexOf(d.properties.sToponym) > -1
                && pathData.indexOf(d.properties.eToponym) > -1;
        }).transition().duration(2000).style("stroke", "red").style("stroke-width", 3);
        d3.selectAll("circle").filter(function (d) {
            return pathData.indexOf(d.topURI) > -1
        }).transition().duration(2000)
            .style("fill", "red")
            .attr("r", function(d) {
                var size = (parseInt(countries[d['topURI']]));
                if(isNaN(size)) return 5;
                //if(size > 1000) {size = size / 50}
                //else {size = size/10;}
                return rscale(size);});

        d3.selectAll("circle").filter(function (d) {
            return pathData.indexOf(d.topURI) <= -1
        }).transition().duration(2000)
            .attr("r", "0");

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

function updateRoutesCountries(countries,graph) {
    d3.selectAll("path").transition().duration(1000).style("stroke", function (d, i) {
        return "black"
    }).style("stroke-width", "2px");
    var country = Object.keys(countries);
    var pathData = [];
    for (var x = 0; x < country.length; x++) {
        for (var y = x + 1; y < country.length; y++) {
            var pData = graph.findShortestPath(country[x], country[y]);
            if (pData) {
                pathData = pathData.concat(pData);
            }
        }
    }
    displayPath(pathData, countries);
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
                displayPath(pData);
            }
        }
    }
}

function dataStructsBetweenPeopleYears(data) {
    var min_year = 2000, max_year = 0;
    var peopleMap = {};
    var yearPeople = {};
    data.forEach(function (d) {
        if (peopleMap[d.id] != undefined) {
            peopleMap[d.id] = {
                'diedAt': d.diedAt,
                'city': peopleMap[d.id]['city'] + ',' + d.city
            };
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
    var output = {};
    output['min_year']=min_year;
    output['max_year']=max_year;
    output['peopleMap']=peopleMap;
    output['yearPeople']=yearPeople;
    return output;
}