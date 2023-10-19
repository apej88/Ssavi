document.addEventListener("DOMContentLoaded", function() {
    // JSON 데이터를 가져오는 AJAX 요청을 수행
    $.ajax({
        url: "/analysis/", // JSON 데이터가 있는 URL로 변경해야 합니다.
        method: "GET",
        success: function(data) {
            console.log("데이터 전송 확인")
            // JSON 데이터를 사용하여 그래프를 그리는 함수 호출
            drawGraph(data);
        },
        error: function() {
            alert("데이터를 가져오는 중 오류가 발생했습니다.");
        }
    });

    // 그래프를 그리는 함수
    function drawGraph(data) {
        var canvas = document.getElementById("audio_feature_graph");
        var ctx = canvas.getContext("2d");
        var radarData = {
            labels: ["Acousticness", "Danceability", "Energy", "Loudness", "Speechiness", "Tempo", "Valence"],
            datasets: [{
                label: 'Audio Features',
                data: [
                    data.data.acousticness,
                    data.data.danceability,
                    data.data.energy,
                    data.data.loudness,
                    data.data.speechiness,
                    data.data.tempo,
                    data.data.valence
                ],
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        };
        var radarChart = new Chart(ctx, {
            type: 'radar',
            data: radarData,
            options: {
                scale: {
                    ticks: {
                        beginAtZero: true,
                        max: 1
                    }
                }
            }
        });
    }
});