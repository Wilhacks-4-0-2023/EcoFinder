function getvars(vars) {
    return vars
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
    var circle = L.circle([lat, lng], {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.3,
        radius: accuracy
    }).addTo(map);


    var eventData = [
        {
            polygon : [
                [1, 1]
            ]
        }
    ]

    eventData.forEach((event) => {
        if (event.polygon.length == 1) {
            var coordinate = event.polygon[0]
            var marker = L.marker(coordinate).addTo(map);
        } else {
            var polygon = L.polygon(
                event.polygon
            ).addTo(map);
            // event.polygon.forEach((coordinate) => {
            //     coordinate.latitude
            // })
        }
    })

    map.on('click', function(e) {
        var marker = new L.marker(e.latlng).addTo(map);
    });

}
   
function fail(error){
    window.alert('Error: ' + error.code);
}
window.addEventListener('load', function() {
    navigator.geolocation.getCurrentPosition(success, fail);            
});

