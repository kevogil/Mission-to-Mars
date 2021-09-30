## Mission to Mars

### Objective
Build a web application to scrape various websites for data related to Mars and display the information in a single HTML page.

### Step 1 : Web scraping
Utilizing Jupyter Notebook, we will scrape the following websites:

<b>NASA Mars News</b>
Collect the latest news title and paragraph text.

<B>JPL Mars Space Images - Featured Image</b>
Use splinter to navigate the site and find the image URL to the current featured Mars image.

<b>Mars Facts</b>
Visit the Mars Facts webpage and scrape the table containing facts about the planet.

<b>Mars Hemisphere</b>
Visit the Astrogeology site to obtain high res images for each of Mar's hemispheres.

### Step 2 : MongoDB and Flask application
Store all scraped information into a Mongo database and create a new HTML page with Flask that will contain all of the information.

1. Convert the Jupyter Notebook to a Python script that will execute all of the scraping code and return one Python dictionary with all of the scraped information.

2. Create a Flask app that imports the scrape function from the Python script.

3. Create a root route that will query the MongoDB and pass the scraped infromation into a HTML template.

4. Design a HTML template file that will display all of the data from the Python dictionary.