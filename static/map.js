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
    //var marker = L.marker([lat, lng]).addTo(map);
    var circle = L.circle([lat, lng], {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.3,
        radius: accuracy
    }).addTo(map);

}
   
function fail(error){
    window.alert('Error: ' + error.code);
}
window.addEventListener('load', function() {
    navigator.geolocation.getCurrentPosition(success, fail);            
});