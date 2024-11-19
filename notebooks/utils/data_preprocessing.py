{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "bdd73478-37bd-4838-a530-dee146d2ddb7",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "from sklearn.compose import ColumnTransformer\n",
    "from sklearn.pipeline import Pipeline\n",
    "from sklearn.impute import SimpleImputer\n",
    "from sklearn.preprocessing import OneHotEncoder, StandardScaler\n",
    "\n",
    "def preprocess_data(data):\n",
    "    \"\"\"\n",
    "    Preprocesses a Pandas DataFrame by applying separate pipelines for\n",
    "    categorical and numerical data. The function handles missing values,\n",
    "    scales numerical data, and one-hot encodes categorical data.\n",
    "\n",
    "    Parameters:\n",
    "        data (pd.DataFrame): Input DataFrame to process.\n",
    "\n",
    "    Returns:\n",
    "        pd.DataFrame: Transformed DataFrame with processed features.\n",
    "    \"\"\"\n",
    "    # Identify categorical and numerical columns\n",
    "    categorical_cols = data.select_dtypes(include=['object', 'category']).columns\n",
    "    numerical_cols = data.select_dtypes(include=['number']).columns\n",
    "\n",
    "    # Define pipelines for categorical and numerical data\n",
    "    categorical_pipeline = Pipeline(steps=[\n",
    "        ('imputer', SimpleImputer(strategy='most_frequent')),\n",
    "        ('onehot', OneHotEncoder(handle_unknown='ignore'))\n",
    "    ])\n",
    "    \n",
    "    numerical_pipeline = Pipeline(steps=[\n",
    "        ('imputer', SimpleImputer(strategy='mean')),\n",
    "        ('scaler', StandardScaler())\n",
    "    ])\n",
    "\n",
    "    # Combine pipelines into a single ColumnTransformer\n",
    "    preprocessor = ColumnTransformer(transformers=[\n",
    "        ('cat', categorical_pipeline, categorical_cols),\n",
    "        ('num', numerical_pipeline, numerical_cols)\n",
    "    ], remainder='drop')  # Ensure only transformed columns are retained\n",
    "    \n",
    "    # Fit and transform the data\n",
    "    processed_data = preprocessor.fit_transform(data)\n",
    "    \n",
    "    # Extract feature names\n",
    "    categorical_feature_names = (\n",
    "        preprocessor.named_transformers_['cat']['onehot']\n",
    "        .get_feature_names_out(categorical_cols)\n",
    "    )\n",
    "    numerical_feature_names = numerical_cols\n",
    "    all_feature_names = list(categorical_feature_names) + list(numerical_feature_names)\n",
    "    \n",
    "    # Convert the result to a DataFrame\n",
    "    processed_df = pd.DataFrame(processed_data.toarray() if hasattr(processed_data, 'toarray') else processed_data,\n",
    "                                columns=all_feature_names, index=data.index)\n",
    "    \n",
    "    return processed_df"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
