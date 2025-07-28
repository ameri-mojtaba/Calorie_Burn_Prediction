from sklearn.base import BaseEstimator, TransformerMixin

# This class contains all the logic for creating new features.
class FeatureEngineer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        # In this particular case, the fit step does nothing
        return self

    def transform(self, X, y=None):
        # We create a copy of the dataframe so that the original is not changed.
        X_transformed = X.copy()

        # Creating new features based on formulas
        # Note: We make sure that the calculations are performed correctly even on the test data
        X_transformed['BMI'] = X_transformed['Weight'] / ((X_transformed['Height'] / 100) ** 2)
        X_transformed['exercise_intensity'] = X_transformed['Duration'] * X_transformed['Heart_Rate']
        X_transformed['WD'] = X_transformed['Weight'] * X_transformed['Duration']
        X_transformed['AD'] = X_transformed['Age'] * X_transformed['Duration']

        return X_transformed
