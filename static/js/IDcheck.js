// 로그인 입력폼 검사

$(document).ready(function() {
    // 장르 2개 이상 선택
    $('#login-form').submit(function(event) {
        let selected_genres = $('input[name="genre_list"]:checked').length;
        if (selected_genres < 2) {
            alert('최소 2개 이상의 장르를 선택해주십시오.');
            event.preventDefault();
        }
    })

    // 아이디 중복 검사 기능
    $('.id_check').click(function() {
        var username = $('#input_id').val();
        if (username) {
            let csrftoken = $('[name=csrfmiddlewaretoken]').val();
            $.ajax({
                type: 'post',
                url: '{% url "id_check" %}',
                data: {'username': username},
                headers: {'X-CSRFToken': csrftoken},
                success: function(data) {
                    console.log(data)
                    if (data.is_taken) {
                        alert('이미 사용 중인 아이디입니다.');
                        $('#input_id').val('');
                    } else {
                        alert('사용 가능한 아이디입니다.');
                    }
                }
            });
        } else {
            alert("아이디를 입력해주십시오");
        };
    });
});