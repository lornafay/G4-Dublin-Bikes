$.getJSON("https://api.openweathermap.org/data/2.5/onecall?lat=53.350140&lon=-6.266155&units=metric&exclude=daily&appid=C5826d96448b6ef028c87b0cf5da80b7", function(data){
    
    console.log(data);

    var iconURLPrefix = "http://openweathermap.org/img/wn/";
    var iconURLSuffix = ".png";

    // display current weather

    var current_time = data.current.dt;
    // convert to miliseconds
    var time = new Date(current_time * 1000);
    console.log(time);
    var hours = time.getHours();
    console.log(hours);
    var minutes = time.getMinutes();
    console.log(minutes);

    

    $('#current_description').html("<p> <span id='current_time'>" + hours + ":" + minutes + "</span><br><br>"+ data.current.temp + "°C<br><br><span class='description'>" 
                                        + data.current.weather[0].description + "</span><br><br>rain: " + data.minutely[0].precipitation + "mm</p>");

    $('#current_icon').html("<img src='" + iconURLPrefix + data.current.weather[0].icon + iconURLSuffix + "' alt='weather icon'>");

    // display forecast weather
    // 2h forecast
    $("#2hr").html("<img src='" + iconURLPrefix + data.hourly[2].weather[0].icon + iconURLSuffix
                                              + "' alt='weather icon'><p><span class='description'>" + data.hourly[2].weather[0].description
                                              + "</span><br><br>chance of rain: " + Math.round(data.hourly[2].pop * 100) + "%</p>");

    // 4h forecast
    $("#4hr").html("<img src='" + iconURLPrefix + data.hourly[4].weather[0].icon + iconURLSuffix
                                              + "' alt='weather icon'><p><span class='description'>" + data.hourly[4].weather[0].description
                                              + "</span><br><br>chance of rain: " + Math.round(data.hourly[4].pop * 100) + "%</p>");

    // 6h forecast
    $("#6hr").html("<img src='" + iconURLPrefix + data.hourly[6].weather[0].icon + iconURLSuffix
                                              + "' alt='weather icon'><p><span class='description'>" + data.hourly[6].weather[0].description
                                              + "</span><br><br>chance of rain: " + Math.round(data.hourly[6].pop * 100) + "%</p>");

    // 8h forecast
    $("#8hr").html("<img src='" + iconURLPrefix + data.hourly[8].weather[0].icon + iconURLSuffix
                                              + "' alt='weather icon'><p><span class='description'>" + data.hourly[8].weather[0].description
                                              + "</span><br><br>chance of rain: " + Math.round(data.hourly[8].pop * 100) + "%</p>");
})