# Overview

Core Exiles Tools is a collection of tools that automate certain parts of the browser game Core Exiles. The tool injects DOM elements into the game page so features can be easily accessed.

## Automatic Travel

After specifying the player's current location and target destination, the automatic travel tool will calculate the path with the lowest fuel cost between the two and automatically simulate user input to navigate the game world.

![Travel Demo](https://github.com/jasonw930/CoreExilesTools/blob/main/travel_demo.gif)

## Automatic Login

This tool will read user credentials from an environment file and use them to login to the game.

![Login Demo](https://github.com/jasonw930/CoreExilesTools/blob/main/login_demo.gif)

# Technical Details

- The client for this program was developed using Javascript, which is responsible for injecting DOM elements that the user interacts with to send requests to the backend.

- The backend for this program was developed using Python and Flask, which is used to host a local server. The program can be controlled using various endpoints exposed by the server.

- Web automation is achieved using Selenium WebDriver, which allows the program to simulate user input.

- The current version of this program is a rewrite of my original prototype which can be found in the version1 directory. The prototype was merely a proof of concept and has completely unmaintainable spaghetti code. The purpose of this rewrite was to implement the same features using a robust layered architecture that is easily maintainable and expandable. When the layout of the game inevitably changes, the data layer can be swapped out to easily accommodate that change. If I ever decide to interact with the backend using a different interface, then the controller layer can be swapped out.
