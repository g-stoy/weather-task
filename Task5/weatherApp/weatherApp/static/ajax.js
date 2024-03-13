$(document).ready(function() {
    $('#searchButton').click(function(event) {
        event.preventDefault(); 

        city = $('#city').val();

        document.querySelector('.rslt_p').textContent = ''
        
        $.ajax({
            url: '/get_city_weather',
            type: 'GET',
            data: { city: city }, 
            success: function(response) {
                child = document.querySelector('.rslt_p')
                child.textContent = "City " + response['city'] + " Weather: " + response['weather'] + " Temperature: " + response["temp"] + "°C, Humidity: " + response['humidity'] + "%";
                $('.result').append(child);
                document.querySelector('#city').value = ''
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });

    $('#refreshButton').click(function(event){
        event.preventDefault();

        $.ajax({
            url: '/refresh',
            type: 'GET',
            success: function(response) {
                $('ul').empty();
                $('.statistic').empty();
                console.log(response.coldest_city)
                response.cities.forEach(function(cityData) {
                    cityItem = $('<div class="col-md-2">').append(
                        $('<div class="card">').append(
                            $('<div class="card-body text-center">').append(
                                $('<h4 class="card-title">').text(cityData.city),
                                $('<p class="card-text">').text('Weather: ' + cityData.weather),
                                $('<p class="card-text">').text('Temperature: ' + cityData.temp + '°C'),
                                $('<p class="card-text">').text('Humidity: ' + cityData.humidity + '%')
                            )
                        )
                    );
                    $('ul').append(cityItem);
                })
                statistic = $('<div class="col-md-12 text-center">').append(
                    $('<h4 class="text-center" style="margin-top: 2%;">').text('The coldest city is ' + response.coldest_city),
            $('<h4 class="text-center" style="margin-bottom: 5%;">').text('The average temperature is '+ response.average_temp + '°C')
                )
            $('.statistic').append(statistic);
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });
});