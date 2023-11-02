# The Game of Kings: How game conditions affect the best chess players

Chess, often regarded as the "Game of Kings," is a centuries-old strategy board game that has captivated minds with its complexity and elegance. Throughout history, chess has seen countless battles waged over the 64 squares of its board. These battles are not only contests of intelligence and strategy but also a reflection of human ingenuity.

In the world of chess, understanding the patterns and characteristics of game outcomes is of paramount importance. This analysis explores how game parameters affected players with FIDE Titles, asking how ELO rating, accuracy score, time controls and more impact game outcomes.

This analysis began by using webscraping tools to gather data for over 20,000 games and over 1000 individual players from chess.com, the world most popular chess website.

After cleaning the data, Exploratory Data Analysis began. Exploration of variables generated intruiging insights into factors that affect game outcomes in addition to relationship between variables. The questioned answered in EDA phase were:

**1. Which side tends to win more frequently: white or black?** 

**2. How does player skill level affect game outcomes?** 

**3. How does player accuracy affect game outcomes?** 

**4. What can we learn from the time format of the games?**

 
![Excerpt from Exploratory Data Analysis of Moves Counts](https://github.com/clerycolm/Chess-Games-Analysis/blob/main/Moves%20Count%20plots.png?raw=true)

This analysis concludes with Multiclass Classification Model Building. Findings from exploratory data analysis are applied in an attempt to predict game outcomes. 

Our objectives in Model Building are twofold. Firstly, we aim to construct interpretable models that effectively capture and quantify the relationship between the dataset features and game outcomes. It is of importance that we build upon the insights made in the EDA phase to further our understanding of the game of chess.

The second is to use these models to predict game outcomes. By leveraging the insights gained during the EDA phase, we aim to develop models capable of categorizing game results, potentially foreseeing victory, defeat, or draw based on the historical game data.

These goals are achieved through the development of Multinomial Logistic Regression models, Random Forest Classifiers, K Nearest Neighbour Classifiers and Support Vector Machines. The primary measure used in judging models was accuracy, with a score of $91\%$ being achieved in testing of Support Vector Machine model.

**Key Skills and Tools:** Python (scikit-learn, statsmodels , numpy, pandas, matplotlib, seaborn), Web Scraping ( Beautiful Soup, selenium ), Multiclass Classification, Resampling Methods, Hypothesis Testing, Exploratory Data Analysis
