# Calorie Burn Prediction using XGBoost and Feature Selection

## 🚀 Overview

<img src="Images/Software.gif" width="280">

This project focuses on predicting the amount of calories burned during a physical exercise session. The primary goal is to demonstrate how to build an accurate and efficient machine learning model by leveraging powerful algorithms like **XGBoost** and employing effective feature selection techniques such as **RandomForestRegressor + Permutation Importance**.

The project includes data cleaning, exploratory data analysis (EDA), feature engineering, and model training, culminating in a predictive model that can be integrated into a user-friendly application.

---

## Dataset

The dataset used for this project is from the [Playground Series - S5E5 Kaggle competition](https://www.kaggle.com/competitions/playground-series-s5e5/overview). It contains the following features:

* `Sex`
* `Age`
* `Height`
* `Weight`
* `Duration`
* `Heart_Rate`
* `Body_Temp`
* `Calories` (Target Variable)

---

## Methodology

### 1. Data Cleaning and Preprocessing
* The initial dataset was converted from CSV to Parquet format for faster data loading and processing.
* Data types for `Height` and `Heart_Rate` were converted from float to integer to maintain consistency.
* The dataset was checked for missing values, and none were found.

### 2. Exploratory Data Analysis (EDA)
* Scatter and distribution plots were generated for all features to visualize their relationships and distributions.
* Skewness of the numerical features was analyzed.

### 3. Feature Engineering and Selection
* New features were created to improve model performance, including:
    * **BMI (Body Mass Index)**
    * **Heart\_Rate\_x\_Duration**
    * **Body\_Temp\_x\_Duration**
    * **Age\_x\_Weight**
* The categorical `Sex` feature was converted into a numerical format using one-hot encoding.
* All features were scaled using `StandardScaler`.
* **Permutation Importance** with a `RandomForestRegressor` was used to identify and select the most influential features for predicting calorie burn.

### 4. Modeling
* An **XGBoost Regressor** was trained using the selected features.
* The model was evaluated based on its predictive accuracy.

---

## Results

The final model, built with carefully selected features, demonstrated a high level of accuracy in predicting the number of calories burned. The most significant predictors were found to be **Duration**, **Heart\_Rate**, **Body\_Temp**, and the engineered interaction features.

---

## How to Use

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ameri-mojtaba/Calorie_Burn_Prediction
    ```
2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Jupyter Notebook:**
    Open and run the `Predict_Calorie.ipynb` notebook to see the full analysis and model training process.

---

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* XGBoost
* Matplotlib
* Seaborn

## 🤝 Connect with me 🤝
📎 LinkedIn 

https://www.linkedin.com/in/mojtaba-ameri/
