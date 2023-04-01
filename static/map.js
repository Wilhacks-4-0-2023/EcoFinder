function getvars(vars) {
    return vars
}

// modifiable variables
var creatingEvent = false;
var eventPolygon = [];

function update() {
    document.getElementById("sendEvent").disabled = !creatingEvent
    document.getElementById("quitEvent").disabled = !creatingEvent
}

function creatingEventonClick() {
    creatingEvent = !creatingEvent
    // console.log(creatingEvent)
    update()
}

function sendEventonClick() {
    console.log('CONFIRM')
    
    creatingEvent = false
    update()
}

function quitEventonClick() {
    console.log('QUIT')
    
    creatingEvent = false
    eventPolygon = []
    update()
}







function success(pos){
    console.log(pos);
    const lat = pos.coords.latitude;
    const lng = pos.coords.longitude;
    const accuracy = pos.coords.accuracy;

    const map = L.map('map').setView([lat, lng], 13);
    const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
    // var marker = L.marker([lat, lng]).addTo(map);
    // var circle = L.circle([lat, lng], {
    //     color: 'red',
    //     fillColor: '#f03',
    //     fillOpacity: 0.3,
    //     radius: accuracy
    // }).addTo(map);


    // TODO: PLACEHOLDER DATA FOR NOW
    var eventData = [
        {
            polygon : [
                [1, 1]
            ]
        }
    ]





    
    var lastRender = []
    function renderPolygon(polygon) {
        // remove last render
        lastRender.forEach((obj) => {
            map.removeLayer(obj)
        })
        lastRender = []

        // render
        if (polygon.length == 0) {
            // nothing to render
        } else if (polygon.length == 1) {
            var coordinate = polygon[0]
            var marker = L.marker(coordinate, {draggable: true});
            marker.addTo(map)
            lastRender.push(marker)
        } else {
            var polygono = L.polygon(
                polygon
            )
            polygono.addTo(map);
            lastRender.push(polygono)
            
            // draggable markers
            for (i = 1; i < polygon.length; i++) {
                var coordinate = polygon[i]
                var marker = L.marker(coordinate, {draggable: true});
                marker.on('drag', (event) => {
                    var coordinate = event.latlng
                    polygon[i] = coordinate

                    // REMOVE POLYGONO FROM lastRender

                    map.removeLayer(polygono)
                    polygono = L.polygon(
                        polygon
                    )
                    polygono.addTo(map);
                    lastRender.push(polygono)
                })
                marker.addTo(map)
                lastRender.push(marker)
            }
        }
    }




    eventData.forEach((event) => {
        renderPolygon(event.polygon)
    })



    // event creation
    map.on('click', function(e) {
        if (creatingEvent) {
            // var marker = new L.marker(e.latlng).addTo(map);
            eventPolygon.push(e.latlng)
            renderPolygon(eventPolygon)
        }
    });

}
   
function fail(error){
    window.alert('Error: ' + error.code);
}


window.addEventListener('load', function() {
    navigator.geolocation.getCurrentPosition(success, fail);            
});

