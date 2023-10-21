// 페이지가 로드 될 때 밑에 코드들이 동작한다.
// 로드되었을 때 유저정보를 미리 받아와서 그 곡에대해 좋아요를 눌렀으면
// 이미지의 src 값을 바꾸어 주어야 한다.
// 그리고 좋아요를 눌렀을 때 liked_track table에 저장되어야 한다.
// 좋아요를 취소했을 때 liked_track table에 저장된 정보를 삭제해야 한다.
document.addEventListener('DOMContentLoaded', function() {
    var images = document.querySelectorAll('.Thumbs_up_image');
    var changeButtons = document.querySelectorAll('.Thumbs_up_btn');
    var imageSources = [
        "/static/image/Thumbs_up_fill.png",
        "/static/image/Thumbs_up.png"
    ];
    var imageIndices = Array.from({ length: changeButtons.length }, () => 1);

    changeButtons.forEach(function(button, index) {
        button.addEventListener('click', function() {
            imageIndices[index] = (imageIndices[index] + 1) % imageSources.length;
            images[index].src = imageSources[imageIndices[index]];
        });
    });
});