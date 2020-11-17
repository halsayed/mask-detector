



setInterval(function() {

    var myImageElement = document.getElementById('image_still');
    if(typeof(myImageElement) != 'undefined' && myImageElement != null){
        myImageElement.src = 'image_still?rand=' + Math.random();
    }
}, refreshInterval);


setInterval( function() {
    var request = new XMLHttpRequest()
    request.open('GET', location.href + 'api', true)
    var maskCount = document.getElementById('mask_count')
    var nomaskCount = document.getElementById('nomask_count')
    var timestamp = document.getElementById('image_timestamp')
    var barcodes_html = ''

    request.onload = function() {
        var data = JSON.parse(this.response)
        if (request.status >= 200 && request.status < 400) {
            maskCount.innerHTML = data.mask_count;
            nomaskCount.innerHTML = data.nomask_count;
            timestamp.innerHTML= data.image_timestamp;
        }


    }

    // Send request
    request.send()

}, refreshInterval);
