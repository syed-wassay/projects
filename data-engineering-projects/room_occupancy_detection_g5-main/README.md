
# DEG Group 5 Capstone Project

## Team members

| Full Name | Roll Number | Email Address |
| :-------- | :------- | :------------------------- |
| Muhammad Daniyal  | 2211-017-KHI-DEG | mohammad.daniyal@xloopdigital.com |
| Fayez Baig  |2211-007-KHI-DEG  | fayaz.baig@xloopdigital.com  |
| Ovais Saleem  | 2211-023-KHI-DEG | ovais.saleem@xloopdigital.com |
| Muhammad Moiz Khan| 2211-020-KHI-DEG | moiz.khan@xloopdigital.com |
| Hammad Siddiqi| 2211-009-KHI-DEG | hammad.siddiqi@xloopdigital.com |
| Syed Wasay Waseem | 2211-030-KHI-DEG | syed.wasay@xloopdigital.com |


## Installation / Deployment

### Requirements
You will need docker to run this project. The development was done using docker version `23.0.1, build a5ee5b1`

### Initial steps
Before you run this project, you will need to set the following `ENV VARIABLES` present in the `.env` file

`MINIO_ROOT_USER` (username for minio)

`MINIO_ROOT_PASSWORD` (password for minio)

`MONGODB_CONNECTION_URL` (mongodb connection url)

You may change the values of remaining `ENV VARIABLES` as per your liking

### Execution
You will find a `start.sh` script inside the project directory, this script executes the whole project as per the requirement, you can read the `start.sh` file for more information

```bash
sudo sh start.sh
```

You will be able to access the frontend of the project at `http://127.0.0.1:5000`

### Model Training
At the time of writing, the project already has a model trained and saved in the directory of `prediction_service` as `model.pkl`

But if you want to re-train the model or you do not find a `model.pkl` inside `prediction_service` you can run the `train_model.sh` script which will train the model on your provided dataset and save the model inside `prediction_service` directory

```bash
sudo sh train_model.sh
```
