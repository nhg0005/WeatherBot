console.log("WeatherBot ready.");
console.log();

// Packages to be used
const fetch = require("node-fetch");
const Twit = require("twit");
const config = require("./config");

console.log(config);
console.log();

// Python style string formatting
String.prototype.format = function () {
    var i = 0, args = arguments;
    return this.replace(/{}/g, function () {
      return typeof args[i] != 'undefined' ? args[i++] : '';
    });
};

// Create a Twit instance
var T = new Twit(config);

// Set up event handler
var stream = T.stream('statuses/filter', { track: ['@WeatherBotTwit'] });

// Triggers an event on a tweet that mentions WeatherBot and passes the tweetWeather function to send the weather
stream.on('tweet', tweetWeather);

// Function that takes in the tweet that triggered the event and responds to that user
// The tweet should only contain a zip code
async function tweetWeather(tweet) {
    try {
        // Get who sent the tweet
        var name = tweet.user.screen_name;

        // Get the id of the user. Used to reply to them
        var nameID = tweet.id_str;

        // Text contents of the input tweet
        var text = tweet.text;
        var zip = text.replace('@WeatherBotTwit ','');

        // For debug purposes
        console.log(name)
        console.log(text)
        console.log(zip)

        // Fetch the weather from OpenWeather based on a zip code
        const weather = await fetch('http://api.openweathermap.org/data/2.5/weather?zip={},us&appid={}&units=imperial'.format(zip, config.weather_api_key));
        let response = await weather.json();
        const temperature = response.main.temp;
        const location = response.name;
        const description = response.weather[0].description;

        // Print the weather in json format to the console
        console.log(response)

        // Form the reply
        var message = "@" + name + " It is currently {}° F in {} with {}.".format(temperature, location, description)

        // Create the tweet
        var tweet = {
            status: message,
            in_reply_to_status_id: nameID
        };

        // Send the tweet
        T.post('statuses/update', tweet, function(err, data, response) {
            if (err) {
                console.log("Something went wrong.");
                console.log(err);
                console.log();
            } else {
                console.log("Success. The reply was tweeted.")
            }
        })
    } catch (error) {
        console.error(error);
    }
}