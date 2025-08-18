import sys
import pandas as pd
from source.exception import CustomException
from source.logger import logging
from source.utilities import load_object

class Prediction:
    def __init__(self):
        pass

    def predict(self,features):
        try:
            model_path = 'artifacts\model.pkl'
            preprocessor_path = 'artifacts\processor.pkl'
            model = load_object(file_path = model_path)
            preprocessor = load_object(file_path = preprocessor_path)
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            return preds
        
        except Exception as e:
            raise CustomException(e,sys)

class CustomData:
    #! the function of this class is to map the inputs from frontend to backend by combining them into a dataframe for easy accessibility
    def __init__(
            self,
            gender:str,
            race_ethnicity:str,
            parental_level_of_education,
            lunch:str,
            test_preparation_coure:str,
            reading_score,
            writing_score
    ):
        #* these values are coming from frontend
        self.gender = gender
        self.race = race_ethnicity
        self.parental_education = parental_level_of_education
        self.lunch = lunch
        self.test_course = test_preparation_coure
        self.reading_score = reading_score
        self.writing_score = writing_score

    def get_data_as_df(self):
        try:
            custom_data_input = {
                'gender':[self.gender],
                'race/ethnicity': [self.race],
                'parental level of education':[self.parental_education],
                'lunch':[self.lunch],
                'test preparation course':[self.test_course],
                'reading score':[self.reading_score],
                'writing score':[self.writing_score]
            }
            return pd.DataFrame(custom_data_input)
        except Exception as e:
            raise CustomException(e,sys)