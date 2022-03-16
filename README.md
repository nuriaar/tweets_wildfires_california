# Larry on Fire

### Installing the Application

1. Run `bash install.sh` in the top-level directory, this will install all required libraries in a virtual environment
2. Enter the virtual environment with `source virtual_larry/bin/activate`
3. Launch the dash server with `ipython3 larry_on_fire.py` and click on the link displayed in the output

*Note*: Please run this application locally for optimal performance.

### Interacting with the Application

Once the three steps above are executed, one can interact with the application on the web browser by toggling three things:

* Year (dropdown menu)
* Season (button)
* Geography (button)

The prior two apply to all 4 visualizations, while the last filter only applies to the wordcloud and LDA. This allows the user to (1) locate the fires, (2) look at the tweet intensity compared to the wildfire intensity, and (3) get an overview of the discussed topics.

*Note:* please keep in mind the applications takes a few seconds to load, especially when loading tweets from all over the USA. 

### Interacting with the API

1. Run `ipython3 api_interaction.py` in the top-level directory
2. Enter a start and an end date in the command line (format: YYY-MM-DD)
3. View the output of the API in `data/twitter_data/simulation.csv`
