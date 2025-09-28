# Real-Estate-Price-Prediction-and-Recommendation-System

# 🏠 AI-Driven Property Valuation and Recommendation System

This repository hosts the complete codebase and documentation for the capstone project focused on predicting real estate property prices using advanced data science techniques. It integrates price prediction, visual analytics, and personalized recommendations into an intuitive web application, deployed using Streamlit and AWS.

---

## 📌 Project Overview

This end-to-end project covers:
- Real estate **price prediction**
- **Feature engineering** and cleaning
- **Model selection and tuning**
- Interactive **analytics dashboard**
- Custom **recommender system**
- **Web app deployment** on AWS

---

## 📁 Project Structure

```
real-estate-price-prediction/
├── Data_Gathering/        # Raw and cleaned datasets
├── Data_Preprocessing/    # Data preprocessing,EDA
├── Model_Selection/       # Model selection
└──  README.md              # Documentation
```

---

## 🧾 Data Collection

Data was self-scraped from the [99acres](https://www.99acres.com) real estate website and complemented with listings from other property platforms to ensure variety and reliability.

---

## 🧹 Data Cleaning & Merging

- Merged flat and house listings
- Handled missing values and inconsistencies
- Standardized area units and location data

---

## 🛠️ Feature Engineering

New features were created to improve model quality:
- Property age and furnishing type
- Area-type combinations
- Amenities count and **luxury score**
- Room indicators and property type

---

## 📊 Exploratory Data Analysis (EDA)

Using Pandas Profiling and visualizations:
- Price trends by location and property type
- Room-wise pricing boxplots
- Correlation analysis and distributions

---

## 🚫 Outlier Detection & Missing Value Handling

- Removed outliers using IQR/Z-score
- Applied median/mode imputation for missing critical fields

---

## 🧠 Feature Selection

Selected features using:
- Correlation Matrix
- Random Forest, Gradient Boosting
- LASSO, Recursive Feature Elimination
- SHAP (Explainable AI) and permutation importance

---

## 🤖 Model Comparison and Selection

Compared multiple models using a unified pipeline and evaluation metrics:

| Model                         | Description                         |
|------------------------------|-------------------------------------|
| Linear Regression            | Baseline linear model               |
| Support Vector Regression    | Non-linear regression               |
| Random Forest Regressor      | Ensemble tree-based model           |
| MLP Regressor (Neural Net)   | Deep learning-based regressor       |
| LASSO & Ridge Regression     | Regularized linear models           |
| Gradient Boosting Regressor  | Sequential tree boosting            |
| Decision Tree Regressor      | Rule-based model                    |
| KNN Regressor                | Distance-based regression           |
| ElasticNet                   | Combined L1 and L2 regularization   |

**Evaluation Metrics**:
- R² Score
- RMSE
- MAE

✅ The top-performing model was integrated into a full preprocessing + prediction pipeline and deployed using Streamlit.

---

## 📈 Analytics Dashboard

An interactive dashboard includes:
- Price heatmaps by city zones
- Word clouds of amenities
- Room-wise pricing boxplots
- Scatterplots and histograms for user insights

---

## 💡 Recommender System

Three recommendation models implemented:
1. **Facilities-Based Recommender**
2. **Price-Based Recommender**
3. **Location Advantage Recommender**

Recommendations are shown interactively via Streamlit based on user preferences.

---

## ☁️ Deployment

The full application was deployed on **AWS**, integrating:
- Property price prediction
- Interactive insights
- Real estate recommendations

Deployed via Streamlit for a smooth user experience and cloud accessibility.

---

## 🛠️ Tech Stack

- **Python**, **Pandas**, **NumPy**, **Scikit-learn**
- **XGBoost**, **LightGBM**
- **Matplotlib**, **Seaborn**, **Plotly**


---

## 📚 Key Takeaways

This project demonstrates:
- End-to-end real estate pipeline design
- Custom feature engineering and model tuning
- Real-world application deployment
- AI-driven decision support for end-users

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
