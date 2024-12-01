import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

def preprocess_crime_data(crime_df):
    # Step 1: Drop redundant columns
    crime_df.drop(columns=crime_df.columns[22:], axis=1, inplace=True)
    print("Dataset Shape:",crime_df.shape)
    
    # Step 2: Detect and drop duplicates
    print(f"Duplicated rows detected: {sum(crime_df.duplicated())}")
    crime_df.drop_duplicates(inplace=True)
    
    # Step 3: Check and handle missing values
    print(f"Missing Values: {sum(crime_df.isna().sum())}")
    crime_df.dropna(inplace=True)
    
    # Step 4: Compute arrest rate and create encoding_dict
    encoding_dict = {
        primary_type: idx
        for idx, (primary_type, _) in enumerate(
            crime_df.groupby('primary_type')
            .apply(lambda g: ((g['arrest'].sum() / len(g)) * 100).round(2))
            .sort_values()
            .items()
        )
    }
    
    # Step 5: Encode 'primary_type' and update 'arrest' column
    crime_df['primary_type_encoded'] = crime_df['primary_type'].map(encoding_dict).fillna(-1).astype(int)
    crime_df['arrest'] = crime_df['arrest'].astype(int)
    
    # Step 6: Feature selection
    features = ['domestic', 'district', 'beat', 'community_number', 'ward',
                'x_coordinate', 'y_coordinate', 'latitude', 'longitude',
                'year', 'primary_type_encoded']
    target = 'arrest'
    
    X = crime_df[features]
    Y = crime_df[target]
    
    # Step 7: Scale features
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    return X, Y


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