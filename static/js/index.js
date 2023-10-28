function displayAlbumInfo(albumElement) {
    var albumInfo = albumElement.querySelector('.album_info');
    if (albumInfo) {
        albumInfo.style.display = 'block';
    }
}

function hideAlbumInfo(albumElement) {
    var albumInfo = albumElement.querySelector('.album_info');
    if (albumInfo) {
        albumInfo.style.display = 'none';
    }
}

var albums = document.querySelectorAll('.album');

    albums.forEach(function(albumElement) {
        albumElement.addEventListener('mouseover', function() {
            displayAlbumInfo(albumElement);
        });

        albumElement.addEventListener('mouseout', function() {
            hideAlbumInfo(albumElement);
        });
      });