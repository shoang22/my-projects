# Data Science Portfolio
I am a student at George Mason University with a passion for all things data science. Currently pursuing a bachelor's degree in Computational and Data Science with a minor in Biology, my domain interests extend outside the classroom to projects with applications in machine learning, natural language processing, computer vision, and agent-based modeling.

## Contents

### Cancer Classification Model
Data analysis and feature engineering are performed on a cancer classification dataset for use with sequential neural network to classify observations as benign or malignant.

*Libraries: pandas, matplotlib, scikit-learn, tensorflow.keras, seaborn, numpy*

### Chicago Crime Prediction by Venue Clusters
Chicago crimes and census data retrieved from Db2 instance are joined with venue information obtained with Foursquare Places API. The resulting dataset is used to train a K-Means Clustering algorithm to create clusters based on the frequency of venue types in a certain location. The clusters are evaluated to determine which combinations of venues have the highest probability of criminal incidents occuring.

[View with interactive maps](https://nbviewer.jupyter.org/github/shoang22/my-projects/blob/master/chicago-crime-clusters/chicago-crime-clusters.ipynb) 

*Libraries: SQLAlchemy, numpy, pandas, matplotlib, scikit-learn, folium*

### Dating App Simulation
Two agent based models are created to simulate agent interactions in dating applications. Each application was created with its own level of multiplicity. The goal of this experiment was to observe agent interactions under differing rulesets. This project was submitted to the SpringSim 2020 Conference and is currently under review for publication in a scientific journal.

*Libraries: networkx, numpy, time, random, scipy*

### Digit Recognizer
Image data provided by Kaggle is used to train a ResNet50 convolutional neural network to predict whether images contained integers 0 through 9. The original dataset was provided in .csv format with coded pixels as columns. I had to covert the instances to images for the CNN to process.

*Libraries: fastai, matplotlib, numpy, pandas, python imaging library, os, random*

### Real or Not
A dataset from Kaggle.com contains twitter posts referring to natural disasters. Also included in the dataset are instances with keywords often associated with natural disasters, but not referring to incidents involving natural disasters. A long short term memory (LSTM) neural network was trained on the dataset to classify instances as actual referrals to natural disasters or posts not referring to natural disasters.

*Libraries: tensorflow.keras, numpy, pandas, matplotlib*
