function getvars(vars) {
    return vars
}

// modifiable variables
var creatingEvent = false;
var eventPolygon = [];

function update() {
    document.getElementById("sendEvent").disabled = !creatingEvent
    document.getElementById("quitEvent").disabled = !creatingEvent
    document.getElementById("eventForm").disabled = !creatingEvent

    window.clearPolygon()
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

    // do some polygon processing

    

    eventPolygon = []

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
    window.clearPolygon = function(polygon) {
        if (polygon) {
            var polygonremovei = lastRender.indexOf(polygon)
            map.removeLayer(lastRender[polygonremovei])
            lastRender = lastRender.splice(polygonremovei, 1)
        } else {
            // remove last render
            lastRender.forEach((obj) => {
                map.removeLayer(obj)
            })
            lastRender = []

            eventData.forEach((event) => {
                window.renderPolygon(event.polygon)
            })
        }
    }

    window.renderPolygon = function(polygon) {

        // render
        if (polygon.length == 0) {
            // nothing to render
        } else if (polygon.length == 1) {
            var coordinate = polygon[0]
            var marker = L.marker(coordinate, {draggable: true});
            marker.on('drag', (event) => {
                var position = event.latlng
                console.log(position)
                marker.setLatLng(position, {
                    draggable: true
                })
                polygon[0] = position
            })
            marker.addTo(map)
            lastRender.push(marker)

            return marker
        } else {
            var polygono = L.polygon(
                polygon
            )
            polygono.addTo(map);
            lastRender.push(polygono)
            var polygonremovei = lastRender.length - 1
            
            // draggable markers
            for (i = 0; i < polygon.length; i++) {
                var coordinate = polygon[i]
                var marker = L.marker(coordinate)
                // var marker = L.marker(coordinate, {draggable: true});
                // marker.on('drag', (event) => {
                //     var coordinate = event.latlng
                //     polygon[i] = coordinate

                //     // REMOVE POLYGONO FROM lastRender
                //     lastRender = lastRender.splice(polygonremovei, 1)

                //     map.removeLayer(polygono)
                //     polygono = L.polygon(
                //         polygon
                //     )
                //     polygono.addTo(map);
                //     lastRender.push(polygono)
                //     polygonremovei = lastRender.length - 1
                // })
                marker.addTo(map)
                lastRender.push(marker)
            }

            return polygono
        }
    }




    eventData.forEach((event) => {
        window.renderPolygon(event.polygon)
    })



    // event creation
    map.on('click', function(e) {
        if (creatingEvent) {
            // var marker = new L.marker(e.latlng).addTo(map);
            eventPolygon.push(e.latlng)
            window.clearPolygon()
            window.renderPolygon(eventPolygon)
        }
    });

}
   
function fail(error){
    window.alert('Error: ' + error.code);
}


window.addEventListener('load', function() {
    navigator.geolocation.getCurrentPosition(success, fail);            
});

