# web-scraping-challenge

This repo includes four primary files (three to operate the webpage and one notebook to show exploratory scrape process)

- Mission_to_Mars/scrape_mars.py
  - Utilizes/organizes the work of the notebook to scrape appropriate data when called by the /scrape route of our flask app
  
- Mission_to_Mars/app.py
  - The flask application that controls the back-end of our webpage. Connects to a mongodb database, initiates our scrape appication, stores results in the database, and uses stored results to populate our templated index.html
  
- Mission_to_Mars/templates/index.html
  - Our home route directs flask to load this template file, which uses a combination of Bootstrap and Jinja to display our scraped data.
  
- Mission_to_Mars/mission_to_mars.ipynb
  - Our jupyter notebook that was initially used to find the correct syntax for the various scrape asks.
  
  
 ![Webpage Example](https://github.com/jpicca/web-scraping-challenge/blob/master/screenshots/screenshot1.png)
