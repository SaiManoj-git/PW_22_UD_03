from datetime import datetime
from airflow.decorators import dag, task
import json

from airflow import DAG
default_args = {
    'owner': 'airflow',
    'retries': 3
}

@dag(
    schedule_interval='@daily',
    start_date=datetime(2022, 1, 1),
    catchup=False,
    default_args=default_args
)

def capstone_pipeline_api():
    
    @task()
    def imageFetch():
        return {'im':1}
    

    @task()
    def imagePreprocessing(im : dict):
        im.values += 1
        return im

    @task()
    def supervisedStuff(im : dict):
        im.values += 1
        return im

    if(1):
        @task()
        def unsupervisedStuff(im : dict):
            im.values += 1
            return im
    '''
    @task()
    def colorization(im : dict):
        im.values += 1
        return im
    
    @task()
    def denoising(im:dict):
        im.values += 1
        return im
    
    @task()
    def deblurring(im:dict):
        im.values += 1
        return im
    
    @task()
    def inPainitng(im:dict):
        im.values += 1
        return im
    '''

    @task()
    def finalImage(im:dict):
        im.values += 1
        return im
    
    crude_image = imageFetch()
    preprocessed_image = imagePreprocessing(crude_image)
    s_image = supervisedStuff(preprocessed_image)
    us_image = unsupervisedStuff(s_image)
    '''colorized_image = colorization(preprocessed_image)
    denoised_image = denoising(colorized_image)
    deblurred_image = deblurring(denoised_image)
    inpainted_image = inPainitng(deblurred_image)'''
    finalImage(s_image)
    finalImage(us_image)
capstone_dag = capstone_pipeline_api()
    