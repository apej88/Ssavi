// const csrf_token = "{{ csrf_token|escapejs }}";
// document.addEventListener("DOMContentLoaded", function () {
//     const likeButton = document.getElementById('likeButton');
//     const likeImage = document.getElementById('likeImage');
//     let isLiked = false; // 초기 상태는 "좋아요"하지 않은 상태

//     likeButton.addEventListener('click', function() {
//         // 이미지를 변경하고 클릭 상태를 변경
//         if (!isLiked) {
//             likeImage.src = "{% static 'image/like_fill.png' %}";
//             isLiked = true;
//         } else {
//             likeImage.src = "{% static 'image/like.png' %}";
//             isLiked = false;
//         }

//         // 앨범 ID와 유저 ID 가져오기
//         const albumId = this.getAttribute('data-album-id');
//         const userId = this.getAttribute('data-user-id');

//         // 서버로 데이터 전송
//         fetch('/toggle-like-album/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': csrf_token, // CSRF 토큰을 전송해야 함
//             },
//             body: JSON.stringify({albumId, userId, isLiked}),
//         })
//         .then(response => response.json())
//         .then(data => {
//             // 서버로부터 응답을 처리 (예: 성공 메시지)
//             console.log(data);
//         })
//         .catch(error => {
//             console.error('Error:', error);
//         });
//     });
// });

