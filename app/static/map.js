function getvars(vars) {
    return vars
}

// modifiable variables
var creatingEvent = false;
var viewingInfo = false;
var eventPolygon = [];

function viewingInfoOff() {
    viewingInfo = false
}

function update() {
    document.getElementById("sendEvent").disabled = !creatingEvent
    document.getElementById("quitEvent").disabled = !creatingEvent
    document.getElementById("eventForm").hidden = !creatingEvent

    document.getElementById("eventView").hidden = !viewingInfo

    var v = '';
    if (eventPolygon.length == 0) {
        v = ''
    } else {
        v = '['
        eventPolygon.forEach((coordinate) => {
            v = v + '[' + coordinate.lat + ', ' + coordinate.lng + '], '
        })
        v = v.substring(0, v.length - 2) + ']'
        console.log(v)
    }

    document.getElementById("location").value = v
    // window.clearPolygon()
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
    var marker = L.marker([lat, lng]).addTo(map);
    // var circle = L.circle([lat, lng], {
    //     color: 'red',
    //     fillColor: '#f03',
    //     fillOpacity: 0.3,
    //     radius: accuracy
    // }).addTo(map);


    // var eventData = []
    // const eventDataRequest = {{ url_for("api/get-event") }}
    // fetch(eventDataRequest)
    // .then(response => response.json())
    // .then(data => {
    //     // data is a parsed JSON object
    //     eventData = data
    //     console.log(data)
    //     console.log(eventData)

    //     // update
    //     eventData.forEach((event) => {
    //         window.renderPolygon(event.polygon)
    //     })
    // })

    // TODO: PLACEHOLDER DATA FOR NOW
    // var eventData = [
    //     {
    //         polygon : [
    //             [1, 1]
    //         ]
    //     }
    // ]





    
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
                if (event.location) {
                    console.log(event.location)
                    var polygono = window.renderPolygon(JSON.parse(event.location))

                    polygono.on("mouseover", (event) => {

                    });
                    polygono.on("mouseout", (event) => {
                        
                    });
                    polygono.on("click", (e) => {
                        console.log(event)
        
                        viewingInfo = true

                        update()

                        document.getElementById("eventViewTitle").textContent = "Title: " + event.title
                        document.getElementById("eventViewContent").textContent = "Content: " + event.content
                        document.getElementById("eventViewDatePosted").textContent = "Date Posted: " + event.date_posted
                        // document.getElementById("eventViewLocation").textContent = event.location

                    });
                }
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

    window.clearPolygon()


    // eventData.forEach((event) => {
    //     window.renderPolygon(event.polygon)
    // })

    ////



    // event creation
    map.on('click', function(e) {
        if (creatingEvent) {
            // var marker = new L.marker(e.latlng).addTo(map);
            eventPolygon.push(e.latlng)
            window.clearPolygon()
            window.renderPolygon(eventPolygon)
            update()
        }
    });

}
   
function fail(error){
    window.alert('Error: ' + error.code);
}


function startup() {
    window.addEventListener('load', function() {
        navigator.geolocation.getCurrentPosition(success, fail);            
    });
}

