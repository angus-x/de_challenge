### Section 1 - Data Pipelines


- Airflow is used to schedule the tasks. [Airflow2](https://airflow.apache.org/docs/apache-airflow/stable/start.html) and python>=3.4 are required.

- to add the taskflow to Airflow, move input and output folder, and etl.py to the "dags" folder under Airflow home.

```    
── dags
    ├── etl.py
    ├── input
    │   ├── applications_dataset_1.csv
    │   └── applications_dataset_2.csv
    │   
    ├── output
    │   ├── successful
    │   │   ├── processed_successful.csv
    │   └── unsuccessful
    │       └── processed_unsuccessful.csv
        
```

- In this solution, pickle files are used to store and pass data between tasks. In production environment, we could consider cloud storage + MySQL/postgreDB for the setup.

- Please refer to etl.py for the details of the etl process