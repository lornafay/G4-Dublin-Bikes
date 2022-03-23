$.getJSON("https://api.openweathermap.org/data/2.5/onecall?lat=53.350140&lon=-6.266155&units=metric&exclude=daily&appid=C5826d96448b6ef028c87b0cf5da80b7", function(data){
    
    console.log(data);

    var iconURLPrefix = "http://openweathermap.org/img/wn/";
    var iconURLSuffix = ".png";

    // display current weather
    $('#current_description').html("<p>" + data.current.weather[0].description + "<br><br> " + data.current.temp + "°C</p>");
    $('#current_icon').html("<img src='" + iconURLPrefix + data.current.weather[0].icon + iconURLSuffix + "' alt='weather icon'>");

    // display forecast weather
    $("#2hr").html("<p>2hr</p><br><img src='" + iconURLPrefix + data.hourly[2].weather[0].icon + iconURLSuffix + "' alt='weather icon'>" + data.hourly[2].weather[0].description);
    $("#4hr").html("<p>4hr</p><br><img src='" + iconURLPrefix + data.hourly[4].weather[0].icon + iconURLSuffix + "' alt='weather icon'>" + data.hourly[4].weather[0].description);
    $("#6hr").html("<p>6hr</p><br><img src='" + iconURLPrefix + data.hourly[6].weather[0].icon + iconURLSuffix + "' alt='weather icon'>" + data.hourly[6].weather[0].description);
    $("#8hr").html("<p>8hr</p><br><img src='" + iconURLPrefix + data.hourly[8].weather[0].icon + iconURLSuffix + "' alt='weather icon'>" + data.hourly[8].weather[0].description);

})