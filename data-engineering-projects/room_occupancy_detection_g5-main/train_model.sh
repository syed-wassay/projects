# Build docker image present inside model directory
docker build -t train_model ./model

# Run the container using keyword args
# mounting volume to access exported model
# adding --rm to remove container after exiting
docker run \
    -v ./model:/app --rm -it train_model \
    --data_path Occupancy.csv \
    --save_model True \
    --model_dir ./

# create directory for prediction service
mkdir -p prediction_service

# move exported model.pkl file into prediction_service
mv ./model/model.pkl ./prediction_service/model.pkl
