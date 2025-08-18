import sys
import os
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.impute import SimpleImputer
from dataclasses import dataclass

from source.exception import CustomException
from source.logger import logging
from source.utilities import save_object

@dataclass
class DataTransformationConfig:
    preprocessor = os.path.join('artifacts',"processor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer(self):
        '''
        This funciton is responsible for data transformation
        '''

        try:
            numerical_columns = ['reading score', 'writing score']
            categorical_columns = ['gender', 'race/ethnicity', 'parental level of education', 'lunch', 'test preparation course']

            num_pipeline = Pipeline(
                steps=[
                    ("impute",SimpleImputer(strategy='median')), #handles missing values
                    ('scaler',StandardScaler())
                ]
            )

            logging.info('Categorical features scaling completed')

            categorical_pipleine = Pipeline(
                steps = [
                    ('impute',SimpleImputer(strategy='most_frequent')),#handles  categorical missing values by replacing them with most frequently occured categorical values
                    ('oneHotEncoding',OneHotEncoder(handle_unknown='ignore')),
                    ('scaler',StandardScaler(with_mean=False))
                ]
            )
            
            logging.info('Categorical features encoding completed')

            preprocesor = ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_columns),
                    ("cat_pipelines",categorical_pipleine,categorical_columns)
                ]
            )

            return preprocesor
        
        except Exception as e:
            raise CustomException(e,sys)


    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df = pd.read_csv('artifacts/train.csv')
            test_df = pd.read_csv('artifacts/test.csv')

            logging.info('REad train nd test data completed!')

            logging.info('Pbtaiing preprocessing object')

            preprocessing_obj = self.get_data_transformer()

            target_column = 'math score'
            numerical_columns = ['reading score', 'writing score']

            input_feature_train_df = train_df.drop(columns = [target_column],axis = 1)
            target_feature_train = train_df[target_column]

            input_feature_test_df = test_df.drop(columns = [target_column],axis = 1)
            target_feature_test = test_df[target_column]

            logging.info(
                f'Applying preprocessor object on training data frame and test dataframe'
            )

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr,np.array(target_feature_train)
            ]
            test_arr = np.c_[input_feature_test_arr,np.array(target_feature_test)]

            logging.info(f'Saved preprocessig object.')

            save_object(
                file_path  =self.data_transformation_config.preprocessor,
                obj = preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor
            )
        except Exception as e:
            raise CustomException(e,sys)