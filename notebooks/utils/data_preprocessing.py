import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

def preprocess_data(data):
    """
    Preprocesses a Pandas DataFrame by applying separate pipelines for
    categorical and numerical data. The function handles missing values,
    scales numerical data, and one-hot encodes categorical data.

    Parameters:
        data (pd.DataFrame): Input DataFrame to process.

    Returns:
        pd.DataFrame: Transformed DataFrame with processed features.
    """
    # Identify categorical and numerical columns
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns
    numerical_cols = data.select_dtypes(include=['number']).columns

    # Define pipelines for categorical and numerical data
    categorical_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    numerical_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])

    # Combine pipelines into a single ColumnTransformer
    preprocessor = ColumnTransformer(transformers=[
        ('cat', categorical_pipeline, categorical_cols),
        ('num', numerical_pipeline, numerical_cols)
    ], remainder='drop')  # Ensure only transformed columns are retained
    
    # Fit and transform the data
    processed_data = preprocessor.fit_transform(data)
    
    # Extract feature names
    categorical_feature_names = (
        preprocessor.named_transformers_['cat']['onehot']
        .get_feature_names_out(categorical_cols)
    )
    numerical_feature_names = numerical_cols
    all_feature_names = list(categorical_feature_names) + list(numerical_feature_names)
    
    # Convert the result to a DataFrame
    processed_df = pd.DataFrame(processed_data.toarray() if hasattr(processed_data, 'toarray') else processed_data,
                                columns=all_feature_names, index=data.index)
    
    return processed_df