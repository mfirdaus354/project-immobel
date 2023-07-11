
# **A Sneak Peek into Belgium's Real Estate Market**

### An Exploratory Data Analysis with Immoweb.be

By: Muhammad Anhar Firdausyi - BeCode - Junior


## OBJECTIVE

The aim of this analysis to be able to provide insight into these following inquiries

 1. What are the variables found in the observation?
 2. How are the variables correlated to each other, particularly toward the price variable?
 3. What are the most essential variable and why?
 4. Price comparison of properties located in municipalities in Belgium, Wallonia, and Flanders
    - The most expensive municipalities
    - The cheapest municipalities

## DATA COLLECTION STRATEGY

The raw data used in this analysis is obtained from [immoweb.be](http://www.immoweb.be) by scraping the webpages of each classified listings on [immoweb.be](http://www.immoweb.be) and gather the data into 'dataset.json'. The scraping is done by executing a pre-programmed web-scraping program that the author has created for the purpose of this project. The source code of the web-scraper can be found in this repository.

## FINDINGS
 1. There is a Strong Correlation between the plot size and the prices of the property
 2. The distribution of the price of the properties are skewed to the right with high kurtosis, meaning that the prices of properties are hugely varies between each other and there is no other common denominator that can explain such variability.
 
## INSTALLATION

It is advisable to execute this following command using the command prompt before opening the "immoweb_insight"

'pip install -r requirements.txt'

## PERSONAL SITUATION
This project is done in order to fulfill Exploratory Data Analysis assignment for BeCode

## PROJECT LIMITATIONS
1. Data collection strategy can be improved
2. The planning of actions required in fulfilling this project can be improved

## LIBRARIES USED IN THIS PROJECT
1. Scrapy
2. Re
3. bs4
4. Pandas
5. Matplotlib.pyplot
6. Seaborn
7. json