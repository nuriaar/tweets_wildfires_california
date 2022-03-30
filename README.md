# Larry on Fire

Authors: Núria Adell Raventós, Jonas Heim, Pavan Prathuru, Sergio Olalla Ubierna

The goal of this project is to give the user the ability to visualize when people tweet about the California wildfires (when they care about them) and what they tweet about (what their concerns are). Our application does this by allowing users to analyze the evolution over time (2015-2020) while offering several filters to interact with the data.

More precisely, it allows a user to analyze the social conversations taking place on 
Twitter around the California wildfires with several components that:
1. Map the location of the most significant wildfires
2. Compare the Twitter conversation volume with the wildfire intensity
3. Showcase the main topics of the conversations

### Installing the Application

1. Run `bash install.sh` in the top-level directory, this will install all required libraries in a virtual environment
2. Enter the virtual environment with `source virtual_larry/bin/activate`
3. Launch the dash server with `ipython3 larry_on_fire.py` and click on the link displayed in the output

*Notes:*
* Please run this application locally for optimal performance.
* When initially loading the application, it can take about a minute.
* When using the filters in the browser, the application takes a few seconds to reload, especially when loading tweets from the entire country.

### Interacting with the Application

Once the three steps above are executed, one can interact with the application on the web browser by toggling three things:

* Year (dropdown menu)
* Season (button)
* Geography (button)

The prior two apply to all 4 visualizations, while the last filter only applies to the wordcloud and LDA. This allows the user to (1) locate the fires, (2) look at the tweet intensity compared to the wildfire intensity, and (3) get an overview of the discussed topics.

### Interacting with the API

1. Run `ipython3 api_interaction.py` in the top-level directory
2. Enter a start and an end date in the command line (format: YYY-MM-DD)
3. View the output of the API in `data/twitter_data/simulation.csv`
