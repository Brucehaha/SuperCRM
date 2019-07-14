var photos = document.getElementById('photo-list-tab');
// ajax
 if(photos) {
     photos.addEventListener('click',
     function GetImages() {
         let photos = document.getElementById('photo-list-tab');
         let imagList =document.getElementById('show-images');
         while(imagList.firstChild) {
             imagList.removeChild(imagList.firstChild)
         }
         var model = photos.getAttribute('model');
         var app = photos.getAttribute('app');
         var field = photos.getAttribute('field');
         var params = 'model_name='+model+'&app_name='+app+'&field_name='+field;
         var xhr = new XMLHttpRequest();
         xhr.onreadystatechange = function () {
              if(xhr.readyState == 4) {
                  var images = JSON.parse(xhr.responseText);
                  for(var i=0;i<images.length; i++) {
                      var image = document.createElement('img');
                      image.setAttribute('src', images[i][0]);
                      image.setAttribute('alt', images[i][1]);
                      image.setAttribute('height', '200');
                      image.setAttribute('width', '200');
                      image.setAttribute('class', 'image-item');

                      imagList.appendChild(image);
                  }

             }
         }
        xhr.open('GET', '/superadmin/media-gallery.html'+'?'+params);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        xhr.send(null)
 }
     , false)
 }


// Get the backupmodal
var backupmodal = document.getElementById("modal");

// Get the button that opens the backupmodal
var btn = document.getElementById("upload-file");

// Get the <span> element that closes the backupmodal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the backupmodal
btn.onclick = function() {
  backupmodal.style.display = "block";
  // boostrap model-open set the body overflow:hidden
  document.getElementsByTagName('body')[0].setAttribute('class', 'backupmodal-open');

}

// When the user clicks on <span> (x), close the backupmodal
span.onclick = function() {
  backupmodal.style.display = "none";
  document.getElementsByTagName('body')[0].removeAttribute('class', 'backupmodal-open');
}

// When the user clicks anywhere outside of the backupmodal, close it
window.onclick = function(event) {
  if (event.target == backupmodal) {
    backupmodal.style.display = "none";
    document.getElementsByTagName('body')[0].removeAttribute('class', 'backupmodal-open');

  }
}