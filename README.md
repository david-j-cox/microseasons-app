# microseasons-app
Inspired by Japan's 72 microseasons, this app allows the user to enter their address and get a poetic description of the microseason for that day and artwork that captures that local fauna and flora from the zip code. 

Here is the generliazed flow:
     - The user enters their zip code. 
     - The last three years of weather data are collected from Open Weather map (openweathermap.org) for the five days surrounding today's date (i.e., two days before, today, and two days after).
     - The data are turned into a .json dataframe passed to GPT-4o
     - The returned poetic description is sent to GPT-4o to generate an image in the Nihonga art style and using local fauna and flora.
     - The image, poem, and descriptive weather statistics are shown in the browser to the user. 

Feel free to test out the app here: https://microseasons-app-d4bnb5ezdggzescr.eastus2-01.azurewebsites.net/
