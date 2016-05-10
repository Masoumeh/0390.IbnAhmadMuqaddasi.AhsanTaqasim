/**
 * Created by masoumeh on 10.02.16.
 */
var map,arcLayer,routeLayer, arcVisibility;
function makeSomeMaps() {
    pathSource = 0;
    var graph;
    var svg = d3.select("body").append("svg")
        .attr("width", 1000)
        .attr("height", 600);

    var g = svg.append("g");
    var arcGroup = g.append('g');
    //var dijSource, dijTarget;
    map = d3.carto.map();
    d3.select("#geoMap").call(map);
    map.centerOn([44.361488, 33.312806], "latlong");
    map.setScale(4);
    map.refresh();

    var routeData;
    wcLayer = d3.carto.layer.tile();
    wcLayer
        .tileType("stamen")
        .path("watercolor")
        .label("Watercolor")
        .visibility(true);
    routeLayer = d3.carto.layer.topojson();
    routeLayer
        .path("../Data/all_routes_new.topojson")
        .label("Postal Routes")
        .cssClass("roads")
        .renderMode("svg")
        .on("load", function () {
            routeData = routeLayer.features();
            graph = createMatrix(routeData);
            cityLayer = d3.carto.layer.csv();
            cityLayer.path("../Data/cornu_filtered.csv")
                .label("Cities")
                .cssClass("metro")
                .renderMode("svg")
                .x("lon")
                .y("lat")
                .clickableFeatures(true)
                .on("load", function () {
                    var uniqueTopType = {};
                    cityLayer.features().forEach(function (f) {
                        uniqueTopType[f['topType']] = 0;
                    });
                    var disOpts = d3.select("#displayOptionsContainer");
                    Object.keys(uniqueTopType).forEach(function (type) {
                        topTypeDiv(disOpts, type);
                    });
                    //the initial of circles
                    d3.selectAll("circle").transition().duration(1000)
                        .style("fill", "seagreen")
                        .attr("r", 1);
                    var poly = {'data': []};
                    var voronoiLayer=map.createVoronoiLayer(cityLayer, 0.5,poly);
                    voronoiLayer
                        .label("Voronoi")
                        .cssClass("voronoi")
                    .on("load", function() {
                            var data={};
                            d3.json("../Python/commonWithCornu.json", function(error, json) {
                                data = json;//console.log(JSON.stringify(Object.keys(json)));

                                var c20 = d3.scale.category20();
                                var ind = 1;
                                var region_color = {};
                            voronoiLayer.g().selectAll("path")
                                .style("fill",function(p){
                                    //var areaLim = 5;
                                    var pol = d3.geom.polygon(p["geometry"]["coordinates"][0]);
                                    var poly = p["geometry"]["coordinates"][0];
                                    var center = pol.centroid();
                                    var region = p['properties']['node']['region'];
                                    if(region=="noData") return "rgba(0,0,0,0)";
                                    if(region_color[region]==undefined) {
                                        region_color[region] = c20(ind);
                                        ind++;
                                        if(ind == 20) ind =1;
                                    }
                                    //console.log(JSON.stringify(data[Object.keys(data)[0]]));
                                    //console.log(JSON.stringify(p['properties']['node']));

                                    //data[Object.keys(data)[7]].forEach(function(d){
                                    //    //console.log(d.arTitle + " " +  p['properties']['node']['arTitle']);
                                    //    if(d.arTitle == p['properties']['node']['arTitle']) {
                                    //        console.log(d.arTitle);
                                    //        return "rgba(255,0,0,2)";
                                    //    }
                                    //});
                                    //if(Math.abs(pol.area()) < 1) return "red";
                                    var max_area = 100;
                                    var sub=8;

                                    if(region=="Sind") max_area=50;
                                    if(region=="Barqa") max_area=10;
                                    if(region=="Sicile") {
                                        max_area = 1;
                                        sub=10;
                                    }
                                    if(region=="Khazar") max_area = 0;
                                    if(region=="Rihab") max_area = 10;
                                    if(region=="Daylam") max_area = 15;
                                    if(region=="Jazirat al-Arab") max_area = 40;
                                    if(region=="Yemen") max_area=40;
                                    if(region=="Transoxiana") max_area = 2;
                                    if(Math.abs(pol.area()) < max_area) {
                                        for(var i=0;i<poly.length;i++) {
                                            var dist =
                                                Math.sqrt(Math.pow(Math.abs(center[0] - poly[i][0]), 2) +
                                                    Math.pow(Math.abs(center[1] - poly[i][1]), 2));
                                            if(dist > max_area/4) {
                                                console.log(dist + " " + max_area);
                                                var v1 = poly[i][0] - center[0];
                                                v1/=dist;
                                                var v2 = poly[i][1] - center[1];
                                                v2/=dist;
                                                p["geometry"]["coordinates"][0][i]=
                                                    [center[0] + (dist/sub) *v1,
                                                    center[1] + (dist/sub) *v2];
                                            }
                                        }
                                        return region_color[region];
                                    }
                                    else return "rgba(0,0,0,0)";
                                }).style("stroke-width","0.0");

                            voronoiLayer.g().selectAll("g.marker")
                                .filter(function(p) {
                                    var pol = d3.geom.polygon(p["geometry"]["coordinates"][0]);
                                    //if(Math.abs(pol.area()) < 1) return "red";
                                    if(p['properties']['node']['region']=="Sham") {
                                        if(Math.abs(pol.area()) < 1)
                                            return p;
                                    }
                                })
                                .style("pointer-events", "all")
                                .style()
                                .on("click", function() {
                                    //alert(d3.mouse(this));
                                });
                            });
                            //.on("click",function() {
                            //    alert(d3.mouse(this));
                            //});style("fill", "red")
                                //.style("pointer-events", "all")
                                //.on("mouseover", function() {
                                //    //console.log(d3.mouse(this));
                                //})
                                //.on("click",function() {
                                //    alert(d3.mouse(this));
                                //});
                                //.style("cursor","pointer");

                                //.on("click", alert("sdfs"));
                            //d3.selectAll(".voronoi")
                            //    .forEach(function(p){
                            //       console.log("test " + JSON.stringify(p));
                            //    });
                            //
                            //var path = voronoiLayer.g().selectAll("path");
                            //path.data(path[0])
                            //console.log(
                            //    JSON.stringify(path[0][0]['__data__']['geometry']['coordinates']));
                            //path
                            //    .data(path[0])
                            //    .enter().append("polygon")
                            //    .attr("points", function(p){
                            //        var q = [];
                            //        var tmp =p['__data__']['geometry']['coordinates'][0];
                            //        tmp.forEach(function(m) {
                            //            q.push(map.projection()([m]));
                            //        });
                            //        //console.log(q);
                            //        return tmp;
                            //    })
                            //    .attr("stroke","black")
                            //    .attr("stroke-width",2)
                            //    .attr("fill","red");
                            //path[0].forEach(function(p) {
                            //    voronoiLayer.g().selectAll("polygon")
                            //        .data(path[0])
                            //        .enter().append("polygon")
                            //        .attr("points",p['__data__']['geometry']['coordinates'])
                            //        .attr("fill","red");
                            //});
                           //        //var area = polygonArea(p);
                            //         console.log("area: "
                            //             + JSON.stringify(p[0]['__data__']['geometry']));
                            //        //style("fill", "red");
                            //    });

                            //svg.selectAll("polygon")
                            //    .data(poly.data)
                            //    .enter().append("polygon")
                                //.attr("points",function(p) {
                                //    if(p == undefined) return;
                                //    var q = [];
                                //    //p.forEach(function(pp) {
                                //    //    q.push(pp[0],
                                //    //        pp[1]);
                                //    //    console.log("q: "+ JSON.stringify(q))
                                //    //});
                                //    var area = polygonArea(p);
                                //    //console.log("area: " + area);
                                //    if(Math.abs(area) < 100)
                                //    {
                                //        console.log("p:" +JSON.stringify(p));
                                //        return p;
                                //    }
                                //
                                //})
                                //.attr("stroke","black")
                                //.attr("stroke-width",2)
                                //.attr("fill", "red  ");
                    });


                    map.addCartoLayer(voronoiLayer);
                });
            map.addCartoLayer(cityLayer);


            //compute_voronoi(filteredData);
        });
    map.addCartoLayer(wcLayer).addCartoLayer(routeLayer);
    return;

    d3.csv("../Data/cornu.csv", function (csv) {
        var prev = '';
        // To filter the duplicate names and those containing "RoutPoint"
        var filteredData = csv.filter(function (d) {
            if (d.arTitle.indexOf('RoutPoint') === -1) {
                var test;
                if (prev !== d.arTitle) test = true;
                prev = d.arTitle;
                if (test) return d;
            }
        });

        // drop down list for starting point of network flow,
        // containing arTitles from cornu.csv file
        d3.select("#networkStart").on("change", function (d) {
            var id = this.options[this.selectedIndex].value;
            //        updateRoutes(id);
        })
            .selectAll("option").data(filteredData).enter()
            .append("option")
            .attr("value", function (d) {
                return d.arTitle;
            })
            .text(function (d) {
                return d.arTitle;
            });


        d3.csv("../Data/peopleRegion.csv", function (error, data) {
            if (error) throw error;
            // Creating the required data structures
            var output = dataStructsBetweenPeopleYears(data);
            // Min year
            var min_year = output['min_year'];
            // Max year
            var max_year = output['max_year'];
            // A map from people to places they have been related to
            var peopleMap = output['peopleMap'];
            // A map from years to people they have been related to
            var yearPeople = output['yearPeople'];

            var slider = d3.slider().value([0, 100])
                .on("slide", function (evt, value) {
                    d3.select('#minYear').text(''
                        + parseInt(value[0] + min_year) * parseInt((max_year - min_year) / 100));
                    d3.select('#maxYear').text('' +
                        +parseInt(value[1] + min_year) * parseInt((max_year - min_year) / 100));
                });
            //function update(value) {
            d3.select("#calcConnections")
                .on("click", function () {
                    var minyear = parseInt(d3.select('#minYear').html());
                    var maxyear = parseInt(d3.select('#maxYear').html());
                    var uniqueCountires =
                        unify_year_people(minyear, maxyear, yearPeople, peopleMap);
                    updateRoutesCountries(uniqueCountires, graph, arcGroup);
                });
            d3.select("#yearSlider").call(slider);
            d3.select("#minYear").text(min_year + '');
            d3.select("#maxYear").text(max_year + '');

            arcLayer = d3.carto.layer.geojson();
            arcLayer.path("../Data/arcs.json")
                .label("Arcs")
                .visibility(false)
                .renderMode("svg")
                .cssClass("roads")
                .clickableFeatures(true);
            arcVisibility = false;
            map.addCartoLayer(arcLayer);
            //arcLayer.visibility('false');

            //findCountries(csv, data, routeData);
            //var select = d3.select("#personSlider")
            //    .append('div')
            //    .append("select")
            //    .on("change", function (d) {
            //        var id = this.options[this.selectedIndex].value;
            //        updateRoutes(id);
            //    });

            //var options = select.selectAll("option").data(Object.keys(peopleMap));
            //options.enter()
            //    .append("option")
            //    .text(function (d) {
            //        return d;
            //    });
        });
    });
}

function closeOpen(container) {
    switch (container) {
        case "leftPanel":
            d3.select("#controlbar").style("left") == "15px" ? d3.select("#controlbar").transition().duration(500).style("left", "-350px") : d3.select("#controlbar").transition().duration(500).style("left", "15px");
            d3.select("#closeLeft").classed("rightarrow") ? d3.select("#closeLeft").classed("rightarrow", false).classed("leftarrow", true) : d3.select("#closeLeft").classed("rightarrow", true).classed("leftarrow", false);
            break;
        case "rightPanel":
            if (d3.select("#rightControls").style("right") == "15px") {
                d3.select("#rightControls").transition().duration(500).style("right", "-300px")
                d3.select("#mapControls").transition().duration(500).style("right", "60px")
            }
            else {
                d3.select("#rightControls").transition().duration(500).style("right", "15px")
                d3.select("#mapControls").transition().duration(500).style("right", "200px")
            }
            d3.select("#closeRight").classed("rightarrow") ? d3.select("#closeRight").classed("rightarrow", false).classed("leftarrow", true) : d3.select("#closeRight").classed("rightarrow", true).classed("leftarrow", false);
            break;
    }
}

function topTypeDiv(disOpts, type) {
    var div = disOpts.append("div")
        .style("width", "100%")
        .append("div")
        .attr("id", function () {
            return type;
        })
        .attr("class", "eyeButton");
    var input = div.append("input")
        .attr("id", type + "Button")
        .attr("class", "mode-checkbox")
        .attr("name", "display")
        .attr("checked", "checked")
        .attr("type", "checkbox")
        .attr("value", function () {
            return type;
        })
        .on("change", function () {
            if (!this.checked) {
                d3.selectAll("circle")
                    .filter(function (d) {
                        return d.topType == type;
                    }).attr("r", 0);
            } else {
                d3.selectAll("circle")
                    .filter(function (d) {
                        return d.topType == type;
                    }).attr("r", 5);
            }
        });

    div.append("label")
        .attr("for", function () {
            return type + "button";
        })
        .attr("class", "mode-picker-label")
        .attr("name", "display")
        .html(function () {
            return type;
        });
}

function hideAllTab() {
    d3.select('#persontab').style('display', 'none');
    d3.select('#person').style('background', '#B1CA8D');
    d3.select('#networktab').style('display', 'none');
    d3.select('#network').style('background', '#B1CA8D');
    d3.select('#routetab').style('display', 'none');
    d3.select('#route').style('background', '#B1CA8D');
}

function showTab(tabname) {
    hideAllTab();
    d3.select('#' + tabname).style('display', 'block');
    d3.select('#' + tabname.substring(0, tabname.length - 3)).style('background', 'white');
}

function polygon(d) {
    return "M" + d.join("L") + "Z";
}