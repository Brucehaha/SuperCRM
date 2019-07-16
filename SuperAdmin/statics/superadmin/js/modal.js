/* toggle modal open and close */
let body = document.getElementsByTagName('body')[0];
let uploader = document.getElementById('uploader');
let uploadClick = document.getElementById('upload-file');

if(uploadClick) {
    uploadClick.addEventListener('click', function(){
        // set body to overflow hidden
        body.setAttribute('class', 'modal-open');
        // show uploader modal
        uploader.style.display = 'block';
    }, false)
}

let backdrop = document.getElementsByClassName('media-modal-backdrop')[0];
let x = document.getElementsByClassName('media-modal-close')[0];

function closeModal() {
        // remove overflow hidden
        body.removeAttribute('class', 'modal-open');
        uploader.style.display = 'none';
    }

/* close modal when click  backdrop or close symbol */
if(backdrop) {
    backdrop.addEventListener('click',closeModal , false)
}

if(x) {
    x.addEventListener('click',closeModal , false)
}


/* menu button click */

let menus = document.getElementsByClassName('media-menu-item');
Array.from(menus).forEach(function (el) {

    el.addEventListener('click', function (event) {
        var isActive = el.classList.contains('active')
        if(!isActive) {
            el.classList.add('active');
            removeActive(menus, el)
        }
    }, false);
});

function removeActive(menus, el) {
    Array.from(menus).filter(element => element != el).forEach(function (element) {
        var isActive = el.classList.contains('active');
        if(isActive) {
            element.classList.remove('active');
        }

    });

}


var photos = document.getElementById('medial_library');
// ajax
 if(photos) {
     console.log('hello');
     photos.addEventListener('click',
     function GetImages() {
         let attachments =document.getElementsByClassName('attachments')[0];
         while(attachments.firstChild) {
             attachments.removeChild(attachments.firstChild)
         }
         var model = photos.getAttribute('model');
         var app = photos.getAttribute('app');
         var field = photos.getAttribute('field');
         var params = 'model_name='+model+'&app_name='+app+'&field_name='+field;
         var xhr = new XMLHttpRequest();
         xhr.onreadystatechange = function () {
              if(xhr.readyState == 4) {
                  console.log(xhr.responseText);
                  var images = JSON.parse(xhr.responseText);
                  for(var i=0;i<images.length; i++) {
                      let list = document.createElement('li');
                      list.setAttribute('class', 'attachment');
                      let image = document.createElement('img');
                      image.setAttribute('src', images[i][0]);
                      image.setAttribute('alt', images[i][1]);
                      image.setAttribute('height', '200');
                      image.setAttribute('width', '200');
                      image.setAttribute('class', 'image-item');
                      list.appendChild(image)
                      attachments.appendChild(list);
                  }

             }
         }
        xhr.open('GET', '/superadmin/media-gallery.html'+'?'+params);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        xhr.send(null)
 }
     , false)
 }
