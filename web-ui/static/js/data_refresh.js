



setInterval(function() {

    var ImageElementCam1 = document.getElementById('image_cam1');
    var ImageElementCam2 = document.getElementById('image_cam2');
    var ImageElementCam3 = document.getElementById('image_cam3');
    var ImageElementCam4 = document.getElementById('image_cam4');

    if(typeof(ImageElementCam1) != 'undefined' && ImageElementCam1 != null){
        ImageElementCam1.src = 'image/CAM1?rand=' + Math.random();
    }
    if(typeof(ImageElementCam2) != 'undefined' && ImageElementCam2 != null){
        ImageElementCam2.src = 'image/CAM2?rand=' + Math.random();
    }
    if(typeof(ImageElementCam3) != 'undefined' && ImageElementCam3 != null){
        ImageElementCam3.src = 'image/CAM3?rand=' + Math.random();
    }
    if(typeof(ImageElementCam4) != 'undefined' && ImageElementCam4 != null){
        ImageElementCam4.src = 'image/CAM4?rand=' + Math.random();
    }
}, refreshInterval);


setInterval( function() {
    var request = new XMLHttpRequest()
    request.open('GET', location.href + 'api', true)
    var maskCountCam1 = document.getElementById('mask_count_cam1')
    var nomaskCountCam1 = document.getElementById('nomask_count_cam1')
    var maskCountCam2 = document.getElementById('mask_count_cam2')
    var nomaskCountCam2 = document.getElementById('nomask_count_cam2')
    var maskCountCam3 = document.getElementById('mask_count_cam3')
    var nomaskCountCam3 = document.getElementById('nomask_count_cam3')
    var maskCountCam4 = document.getElementById('mask_count_cam4')
    var nomaskCountCam4 = document.getElementById('nomask_count_cam4')

    request.onload = function() {
        var data = JSON.parse(this.response)
        if (request.status >= 200 && request.status < 400) {
            maskCountCam1.innerHTML = data.mask_count_cam1;
            nomaskCountCam1.innerHTML = data.nomask_count_cam1;
            maskCountCam2.innerHTML = data.mask_count_cam2;
            nomaskCountCam2.innerHTML = data.nomask_count_cam2;
            maskCountCam3.innerHTML = data.mask_count_cam3;
            nomaskCountCam3.innerHTML = data.nomask_count_cam3;
            maskCountCam4.innerHTML = data.mask_count_cam4;
            nomaskCountCam4.innerHTML = data.nomask_count_cam4;
        }


    }

    // Send request
    request.send()

}, refreshInterval);
