/**
 * Created by masoumeh on 10.02.16.
 */

function makeSomeMaps() {
    pathSource = 0;
    var graph;
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
    routeLayer = d3.carto.layer.topojson();
    routeLayer
        .path("../Data/all_routes_new.topojson")
        .label("Postal Routes")
        .cssClass("roads")
        .renderMode("svg")
        .on("load", function() {
            postdata = routeLayer.features();
            graph = createMatrix(postdata);
            cityLayer = d3.carto.layer.csv();
            cityLayer.path("../Data/cornu.csv")
                .label("Cities")
                .cssClass("metro")
                .renderMode("svg")
                .x("lon")
                .y("lat")
                .clickableFeatures(true)
                .on("load", function () {
                    //the initial of circles
                    d3.selectAll("circle").transition().duration(1000)
                        .style("fill", "green")
                        .attr("r",5);
                });
            map.addCartoLayer(cityLayer);
        });
    map.addCartoLayer(wcLayer).addCartoLayer(routeLayer);

    d3.csv("../Data/peopleRegion.csv", function (error, data) {
        if (error) throw error;
        var output = dataStructsBetweenPeopleYears(data);
        var min_year = output['min_year'];
        var max_year = output['max_year'];
        var peopleMap = output['peopleMap'];
        var yearPeople = output['yearPeople'];
        d3.select("#yearSlider")
            .call(d3.slider().value([0, 100])
                .on("slide", function (evt, value) {
                    d3.select('#minYear').text(''
                        + parseInt(value[0] + min_year) * parseInt((max_year - min_year) / 100));
                    d3.select('#maxYear').text(''+
                        + parseInt(value[1] + min_year) * parseInt((max_year - min_year) / 100));
                })
                .on("slideend", function (evt, value) {
                    var minyear = parseInt(value[0] + min_year)
                        * parseInt((max_year - min_year) / 100);
                    var maxyear = parseInt(value[1] + min_year)
                        * parseInt((max_year - min_year) / 100);
                    var uniqueCountires =
                        unify_year_people(minyear,maxyear,yearPeople,peopleMap);
                    updateRoutesCountries(uniqueCountires,graph);
                })
        );

        d3.select("#minYear").text(min_year+'');
        d3.select("#maxYear").text(max_year+'');

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
    });
}



