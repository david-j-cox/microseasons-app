# microseasons-app

Inspired by Japan's 72 microseasons, this app allows the user to enter their address and get a poetic description of the microseason for that day and artwork that captures that local fauna and flora from the zip code. 

Here is the generalized flow:
1. The user enters their zip code.  
2. The last three years of weather data are collected from Open Weather map (openweathermap.org) for the five days surrounding today's date (i.e., two days before, today, and two days after).  
3. The data are turned into a .json dataframe passed to GPT-4o.  
4. The returned poetic description is sent to GPT-4o to generate an image in the Nihonga art style and using local fauna and flora.  
5. The image, poem, and descriptive weather statistics are shown in the browser to the user.

<img width="723" alt="Screenshot 2025-01-12 at 4 09 27 PM" src="https://github.com/user-attachments/assets/52b2083a-215d-4bf7-b3ba-9f3304c13190" />

Feel free to test out the app here: [microseasons app link](https://microseasons-app-d4bnb5ezdggzescr.eastus2-01.azurewebsites.net/)
