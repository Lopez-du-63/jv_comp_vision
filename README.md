# Object detection in an Urban Environment
All instructions provided to carry the project are at the bottom to ease reading from mentor.

## Submission

### Project overview
The target of this project is to get practical knowledge on neural network training. For this purpose a few records will be downloaded from the waymo repository. Its data will be converted to tensorflow compatible format.
Afterwards manual analysis of the data will be carried. Finally different deep learning architecture and data augmentation strategy will be tried to improve target recognition and classification in pictures/video feeds.

As side learning: Containers and virtual machines were a new thing to me. I knew it existed but never configured one myself. I invested nearly more time in getting a working setup and understanding the concepts behind.

### Set up

For the setup, docker file has been modified to install tensorflow 2.5.0.
Waymo dataset wheel must be installed manually with pip command. The wheel is in the root folder.
If working on Windows, Developers build must be installed. Otherwise nvidia-docker will not be compatible with docker. On top of that drivers won't be recognized.
Data is not stored in "/workspace" but in "/data/processed/" folder.

### Dataset
#### Dataset analysis
At the following link can be found some images extract from the [Exploratory Notebook](https://github.com/Lopez-du-63/jv_comp_vision/blob/main/Exploratory%20Data%20Analysis.ipynb).
In order to be able to run the notebook, the utils.py from this project must be used. I implemented my own function to create a dataset and parse it; as I couldn't get to work the one which was provided.

##### Image content
Images contain for the most part vehicles. We also have certain cross-roads with many pedestrian for training, but not as much. Finally the database does not contain many cyclists.

##### Image quality

Brightness and weather are generally good. This a kind of "perfect situation" learning, where hard situations are barely considered.
Some of the records still are filmed during night or rainy days, which is a good thing.
This downside will surely need to be compensated through augmentation.

##### Color spread in the dataset
![Histogram/ Mean and Std](/images/histogram.JPG)

As we can see, colors are mostly centered between 30 and 150; with a blue pick at 255 which comes from the blue sky.

##### Cross validation
For the cross validation strategy, a split between training/validation and test dataset will be carried.
As we have more than 10k images (about the double), and we start training from pre-trained model it is possible to perform this three splits.
A standard split will be used: 75% for training, 15% for validation and 10% for testing.
The testing set is used to ensure there is no leakage of information from the training steps into the test dataset (as model is optimized according to results on the validation set).


### Training 
#### Issues met
Training the neural network was really resource greedy. I faces all common issues one can face in the field I guess:
  * Long waiting times: This one can be fixed by only checking what happens in the first thousant step and get a feeling of what is coming
  * Lack of options from the proto for image transformations: I think Albumentation is a much more powerful tool. But I sticked with the intented project framework. Plus I wouldn't have been able to use the [Explore augmentation notebook](https://github.com/Lopez-du-63/jv_comp_vision/blob/main/Explore%20augmentations.ipynb).
  * Memory consumption: I usually had to manually free GPU memory after each training; which prevented me from running the algorithms overnight.. There must be a way to have tensorflow free the memory, but I didn't take the time to check. My computer was also not able to work with 4 batchs. I reduced it to 2 (even 1 when I played with the architecture of the network).



#### Reference experiment
This section should detail the results of the reference experiment. It should includes training metrics and a detailed explanation of the algorithm's performances.
The metrics provided show the loss computed in the different stages of the neural network:
  * Loss during the classification: is there an object or not, and which type ? Usually values should be between 0 and 1; but I happened to have over 1k for one of my experiments with highly noised pictures
  * Loss during the localization: where is the object detected ?
  * Loss during the regularization (L2 norm)
  * And the total loss, which provides information on the end result

##### Coco metrics for the model
![Coco Metrics for reference model](/images/metrics_reference.JPG)

As can be seen, the learning seems to stabilize close to the end of the learning.
On one hand the regularization loss decreases a lot over the learning in a smooth manner, it seems to reach a stable point also. On the other hand, the classification and localization loss go on average down over the learning, but in a chaotic way.

If we try the model on a few test record, we can notice that:
  * Other vehicles are perceived only when close to them
  * There are difficulties in detecting vehicles at night
  * Pedestrians are barely recognized

#### Improve on the reference
The different configuration files can be found in the following [folder](/config)
I did not succeed improving the pre-trained model. Detections were worse on average. Training time is so long (several hours per experiment) that I only tried a sample of changes:
  * I changed the architecture:
    * Increased depth of the feature extractor
    * Tried L1 norm instead of L2
    * Increased number of layer for the box predictor
    * Modified learning step variance
    * Increased number of steps for the learning
  * I modified the images:
    * the croping
    * the brightness
    * the contrast
    * the hue
    * normalized the image

I wil take the time later on to simply use another pre-trained model. I would like to use the Efficientdet D2 for instance, which provides a greatly improvem mAP for a slighlty worse computation time.
Below the results of my different experiments.

##### Experiment0
In this experiment, I added a lot of color distortion, brightness, saturation etc..
Here the [configuration file](/config/pipeline_exp0.config)


After running the experiment, results were catastrophic. Nothing was detected.
After looking at the metrics, it seems the learning was going smoothly and then suddenly everything went really bad. There must have been some huge outliers which completely disoriented the learning at 12k steps(regularization is computed using L2 norm, which is bad against outliers).
This gave me the hint to try with a L1 regularizer if I ever distord too much images.
Here are the metrics from the experiment:
![Coco Metrics for experiment0 model](/images/metrics_experiment0.JPG)
 
##### Experiment0_bis
In this case I tried to distord a lot less the image and increased the number of learning steps.
Here the [configuration file](pipeline_exp0_bis.config)

The results were not really conclusive. Detection range of the vehicle was worse, and there was an increase of False Positive in the animations I generated.
![Coco Metrics for experiment0 model](/images/metrics_experiment0_bis.JPG)


##### Experiment1
In this case I:
  * took off the hue modification
  * decreased the number of learning steps
  * decreases weight of regularizer in the box predictor
  * increase number of layers before prediction
  * increased depth of the feature extractor


Here the [configuration file](pipeline_exp1.config)
The results were not really conclusive. The regularization loss is hudge.
Nothing was detected when running animation.
![Coco Metrics for experiment model](/images/metrics_experiment1.JPG)


##### Experiment2
In this case I:
  * used L1 normalizer


Here the [configuration file](pipeline_exp2.config)
The results were not really conclusive. Vehicles were not detected and many pedestrians were detected with bounding boxes forming nearly the whole picture.
![Coco Metrics for experiment model](/images/metrics_experiment2.JPG)


##### Experiment3
In this case I:
  * increased the depth of the box predictor
  * switched back to L2 normalizer

Here the [configuration file](pipeline_exp3.config)
The results were better than in previous experiment, as vehicles were detected. But there still was this false pedestrian detection.

![Coco Metrics for experiment](/images/metrics_experiment3.JPG)


##### Experiment4
In this case I:
  * keep a deeper feature extractor but normal bounding box detector


Here the [configuration file](pipeline_exp4.config)
The results were as bas as in experiment2
![Coco Metrics for experiment model](/images/metrics_experiment4.JPG)


#### Conclusion
I did not really improve performance of the reference model. If I keep trying I would use Albumentations to modify images instead. And I would try a different architecture.
Learning are really quite intensive. In order to optimize models the best is to rent a gpu on the cloud. My computer which has a powerful GPU could barely keep going. More than 2 batches was already too much.


## Data

For this project, we will be using data from the [Waymo Open dataset](https://waymo.com/open/). The files can be downloaded directly from the website as tar files or from the [Google Cloud Bucket](https://console.cloud.google.com/storage/browser/waymo_open_dataset_v_1_2_0_individual_files/) as individual tf records. 

## Structure

The data in the classroom workspace will be organized as follows:
```
/home/backups/
    - raw: contained the tf records in the Waymo Open format. (NOTE: this folder only contains temporary files and should be empty after running the download and process script)

/home/workspace/data/
    - processed: contained the tf records in the Tf Object detection api format. (NOTE: this folder should be empty after creating the splits)
    - test: contain the test data
    - train: contain the train data
    - val: contain the val data
```

The experiments folder will be organized as follow:
```
experiments/
    - exporter_main_v2.py: to create an inference model
    - model_main_tf2.py: to launch training
    - experiment0/....
    - experiment1/....
    - experiment2/...
    - pretrained-models/: contains the checkpoints of the pretrained models.
```

## Prerequisites

### Local Setup

For local setup if you have your own Nvidia GPU, you can use the provided Dockerfile and requirements in the [build directory](./build).

Follow [the README therein](./build/README.md) to create a docker container and install all prerequisites.

### Classroom Workspace

In the classroom workspace, every library and package should already be installed in your environment. However, you will need to login to Google Cloud using the following command:
```
gcloud auth login
```
This command will display a link that you need to copy and paste to your web browser. Follow the instructions. You can check if you are logged correctly by running :
```
gsutil ls gs://waymo_open_dataset_v_1_2_0_individual_files/
```
It should display the content of the bucket.

## Instructions

### Download and process the data

The first goal of this project is to download the data from the Waymo's Google Cloud bucket to your local machine. For this project, we only need a subset of the data provided (for example, we do not need to use the Lidar data). Therefore, we are going to download and trim immediately each file. In `download_process.py`, you will need to implement the `create_tf_example` function. This function takes the components of a Waymo Tf record and save them in the Tf Object Detection api format. An example of such function is described [here](https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/training.html#create-tensorflow-records). We are already providing the `label_map.pbtxt` file. 

Once you have coded the function, you can run the script at using
```
python download_process.py --data_dir /home/workspace/data/ --temp_dir /home/backups/
```

You are downloading XX files so be patient! Once the script is done, you can look inside the `/home/workspace/data/processed` folder to see if the files have been downloaded and processed correctly.


### Exploratory Data Analysis

Now that you have downloaded and processed the data, you should explore the dataset! This is the most important task of any machine learning project. To do so, open the `Exploratory Data Analysis` notebook. In this notebook, your first task will be to implement a `display_instances` function to display images and annotations using `matplotlib`. This should be very similar to the function you created during the course. Once you are done, feel free to spend more time exploring the data and report your findings. Report anything relevant about the dataset in the writeup.

Keep in mind that you should refer to this analysis to create the different spits (training, testing and validation). 


### Create the splits

Now you have become one with the data! Congratulations! How will you use this knowledge to create the different splits: training, validation and testing. There are no single answer to this question but you will need to justify your choice in your submission. You will need to implement the `split_data` function in the `create_splits.py` file. Once you have implemented this function, run it using:
```
python create_splits.py --data_dir /home/workspace/data/
```

NOTE: Keep in mind that your storage is limited. The files should be <ins>moved</ins> and not copied. 

### Edit the config file

Now you are ready for training. As we explain during the course, the Tf Object Detection API relies on **config files**. The config that we will use for this project is `pipeline.config`, which is the config for a SSD Resnet 50 640x640 model. You can learn more about the Single Shot Detector [here](https://arxiv.org/pdf/1512.02325.pdf). 

First, let's download the [pretrained model](http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_resnet50_v1_fpn_640x640_coco17_tpu-8.tar.gz) and move it to `training/pretrained-models/`. 

Now we need to edit the config files to change the location of the training and validation files, as well as the location of the label_map file, pretrained weights. We also need to adjust the batch size. To do so, run the following:
```
python edit_config.py --train_dir /home/workspace/data/train/ --eval_dir /home/workspace/data/val/ --batch_size 4 --checkpoint ./training/pretrained-models/ssd_resnet50_v1_fpn_640x640_coco17_tpu-8/checkpoint/ckpt-0 --label_map label_map.pbtxt
```
A new config file has been created, `pipeline_new.config`.

### Training

You will now launch your very first experiment with the Tensorflow object detection API. Create a folder `training/reference`. Move the `pipeline_new.config` to this folder. You will now have to launch two processes: 
* a training process:
```
python model_main_tf2.py --model_dir=training/reference/ --pipeline_config_path=training/reference/pipeline_new.config
```
* an evaluation process:
```
python model_main_tf2.py --model_dir=training/reference/ --pipeline_config_path=training/reference/pipeline_new.config --checkpoint_dir=training/reference/
```

NOTE: both processes will display some Tensorflow warnings.

To monitor the training, you can launch a tensorboard instance by running `tensorboard --logdir=training`. You will report your findings in the writeup. 

### Improve the performances

Most likely, this initial experiment did not yield optimal results. However, you can make multiple changes to the config file to improve this model. One obvious change consists in improving the data augmentation strategy. The [`preprocessor.proto`](https://github.com/tensorflow/models/blob/master/research/object_detection/protos/preprocessor.proto) file contains the different data augmentation method available in the Tf Object Detection API. To help you visualize these augmentations, we are providing a notebook: `Explore augmentations.ipynb`. Using this notebook, try different data augmentation combinations and select the one you think is optimal for our dataset. Justify your choices in the writeup. 

Keep in mind that the following are also available:
* experiment with the optimizer: type of optimizer, learning rate, scheduler etc
* experiment with the architecture. The Tf Object Detection API [model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md) offers many architectures. Keep in mind that the `pipeline.config` file is unique for each architecture and you will have to edit it. 


### Creating an animation
#### Export the trained model
Modify the arguments of the following function to adjust it to your models:
```
python .\exporter_main_v2.py --input_type image_tensor --pipeline_config_path training/experiment0/pipeline.config --trained_checkpoint_dir training/experiment0/ckpt-50 --output_directory training/experiment0/exported_model/
```

Finally, you can create a video of your model's inferences for any tf record file. To do so, run the following command (modify it to your files):
```
python inference_video.py -labelmap_path label_map.pbtxt --model_path training/experiment0/exported_model/saved_model --tf_record_path /home/workspace/data/test/tf.record --config_path training/experiment0/pipeline_new.config --output_path animation.mp4
```

