# Income Mapping application

The idea of this project is to test the capabilities of Dash by creating an application with a real-word data set of our choosing.

# Dependencies

The app make use of the packages specified in requirements.txt

# Introduction

The chosen data can be found [here](https://www.kaggle.com/goldenoakresearch/us-household-income-stats-geo-locations) and its retrieval was possible thanks to the Kaggle python API. After data is retrieved it is removed from your computer automatically.

Data is composed by numerous attributes related to the income of U.S cities. Theres stpatial information such as latitude and longuitude; mean income, standard deviations, water and land proportions, etc. Every time the app is executed the data is directly loaded from Kaggle leaving no trace in the computer. As a result of this, if the data in its original Kaggle repository is updated, so will the application.

The application is meant to be a tool for exploring the different incomes throughout the United States and in no way the attempt is to perform a thorough statistical analysis of the different possible locations.

# Functionalities

The layour of the app is simple, with a navigation bar with only two options: visualizations and data table.

Map is the principal page, where a map of the US is displayed along with bubbles indicating the areas with data and a color based on an income gradient. It is possible to filter by state. In addition to that, below the map different visualizations grouped by ZIP code and city can be seen based on different metrics such as mean income, meadian and standard deviation of the income.

On the other hand, Data shows a data table with the used information. This data can be downloaded in this very same section of the page.

