from flask import Flask,request, jsonify, render_template
import pickle
import numpy as np
from watchdog.events import EVENT_TYPE_OPENED
import cv2 as cv
import joblib
import json
import torch
from PIL import Image, ImageChops, ImageOps
from torchvision import transforms
from model import Model
from train import SAVE_MODEL_PATH
import io

app = Flask(__name__, static_url_path='/static', static_folder='static')


### IRIS Classification Models ### Model based on Text classification
model_filename = 'C:/Users/chris/Desktop/Dimitris/Tutorials/AI/Computational-Intelligence-and-Statistical-Learning/WebApp/Models/svm_model_iris.pkl'
# model_filename = 'D:/Programming/AI_Detector_WebApp/Computational-Intelligence-and-Statistical-Learning/WebApp/Models/svm_model_iris.pkl'
SVM_Iris_model = joblib.load(model_filename)

model_filename = 'C:/Users/chris/Desktop/Dimitris/Tutorials/AI/Computational-Intelligence-and-Statistical-Learning/WebApp/Models/KNN_model_iris.pkl'
# model_filename = 'D:/Programming/AI_Detector_WebApp/Computational-Intelligence-and-Statistical-Learning/WebApp/Models/KNN_model_iris.pkl'
KNN_Iris_model = joblib.load(model_filename)

model_filename = 'C:/Users/chris/Desktop/Dimitris/Tutorials/AI/Computational-Intelligence-and-Statistical-Learning/WebApp/Models/Nearest_model_iris.pkl'
# model_filename = 'D:/Programming/AI_Detector_WebApp/Computational-Intelligence-and-Statistical-Learning/WebApp/Models/Nearest_model_iris.pkl'
KNearestCentroid_Iris_model = joblib.load(model_filename)

### IRIS Clustering Model ### 
model_filename = 'C:/Users/chris/Desktop/Dimitris/Tutorials/AI/Computational-Intelligence-and-Statistical-Learning/WebApp/Models/kmeans_iris.pkl'
# model_filename = 'D:/Programming/AI_Detector_WebApp/Computational-Intelligence-and-Statistical-Learning/WebApp/Models/kmeans_iris.pkl'
KMeans_Iris_model = joblib.load(model_filename)


### BreastCancer Clustering Model ### 
model_filename = 'C:/Users/chris/Desktop/Dimitris/Tutorials/AI/Computational-Intelligence-and-Statistical-Learning/WebApp/Models/kmeans_breast_cancer_model.pkl'
# model_filename = 'D:/Programming/AI_Detector_WebApp/Computational-Intelligence-and-Statistical-Learning/WebApp/Models/kmeans_breast_cancer_model.pkl'
KMeans_breast_cancer_model = joblib.load(model_filename)


# Load the saved KMeans model and StandardScaler
model_filename = 'C:/Users/chris/Desktop/Dimitris/Tutorials/AI/Computational-Intelligence-and-Statistical-Learning/WebApp/Models/scaler_breast_cancer.pkl'
# model_filename = 'D:/Programming/AI_Detector_WebApp/Computational-Intelligence-and-Statistical-Learning/WebApp/Models/scaler_breast_cancer.pkl'
scaler = joblib.load(model_filename)


model_filename = 'C:/Users/chris/Desktop/Dimitris/Tutorials/AI/Computational-Intelligence-and-Statistical-Learning/WebApp/Models/iris_regression_model.pkl'
# model_filename = 'D:/Programming/AI_Detector_WebApp/Computational-Intelligence-and-Statistical-Learning/WebApp/Models/iris_regression_model.pkl'
Regression_Iris_model = joblib.load(model_filename)


model_filename = 'C:/Users/chris/Desktop/Dimitris/Tutorials/AI/Computational-Intelligence-and-Statistical-Learning/WebApp/Models/Regression_CaliforniaHouses.pkl'
# model_filename = 'D:/Programming/AI_Detector_WebApp/Computational-Intelligence-and-Statistical-Learning/WebApp/Models/iris_regression_model.pkl'
Regression_House_model = joblib.load(model_filename)


model_filename = 'C:/Users/chris/Desktop/Dimitris/Tutorials/AI/Computational-Intelligence-and-Statistical-Learning/WebApp/Models/Regression_CaliforniaHouses.pkl'
# model_filename = 'D:/Programming/AI_Detector_WebApp/Computational-Intelligence-and-Statistical-Learning/WebApp/Models/iris_regression_model.pkl'
Regression_House_model = joblib.load(model_filename)

model_filename = 'C:/Users/chris/Desktop/Dimitris/Tutorials/AI/Computational-Intelligence-and-Statistical-Learning/WebApp/Models/cifar10_pytorch_model.pkl'
# model_filename = 'D:/Programming/AI_Detector_WebApp/Computational-Intelligence-and-Statistical-Learning/WebApp/Models/iris_regression_model.pkl'
cifar10_model = joblib.load(model_filename)


@app.route('/')
def home():
    return render_template('Home.html')


### Classification
@app.route('/Classification')
def Classification():
    return render_template('Classification.html')

@app.route('/Classification_Iris', methods=['GET'])
def Classification_Iris():
    return render_template('Classification_Iris.html')

@app.route('/ClassificationIris', methods=['POST'])
def ClassificationIris():
    try:
        # Extract the input data from the HTML form
        SepalLength = request.form.get('SepalLength')
        SepalWidth = request.form.get('SepalWidth')
        PetalLength = request.form.get('PetalLength')
        PetalWidth = request.form.get('PetalWidth')

        # Check if any of the features are null or empty strings
        if not all([SepalLength, SepalWidth, PetalLength, PetalWidth]):
            message = "Please set all the features"
            return render_template('Classification_Iris.html', message=message)
        
        # Convert features to floats if they are not null or empty strings
        SepalLength = float(SepalLength)
        SepalWidth = float(SepalWidth)
        PetalLength = float(PetalLength)
        PetalWidth = float(PetalWidth)
        
        input_data = np.array([SepalLength, SepalWidth, PetalLength, PetalWidth]).reshape(1, -1)

        if 'SVM' in request.form:
            prediction = SVM_Iris_model.predict(input_data)
        elif 'KNN' in request.form:
            prediction = KNN_Iris_model.predict(input_data)
        elif 'KNearestCentroid' in request.form:
            prediction = KNearestCentroid_Iris_model.predict(input_data)

        if(prediction is None):
            return render_template('Classification_Iris.html')
        else:
            result = int(prediction[0])
            if(result == 0):
                result = "Setosa"
            elif result == 1:
                result = "Versicolor"
            else:
                result = "Virginica"
            return render_template('Classification_Iris.html', result=result)
        
        
    except (ValueError, TypeError) as e:
        message = "Invalid input format. Please provide valid numeric values for all features."
        return render_template('Classification_Iris.html', message=message)


# @app.route('/Classification_BreastCancer', methods=['GET'])
# def Classification_BreastCancer():
#     return render_template('Classification_BreastCancer.html')


# @app.route('/ClassificationBreastCancer', methods=['POST'])
# def ClassificationBreastCancer():
    try:

        # # Example input array with 6 features (replace with your own input data)
        # input_data = np.array([[17.99, 10.38, 122.8, 1001, 0.1184, 0.2776]])
        
        # Extract the input data from the HTML form
        Radius_Mean = request.form.get('Radius_Mean')
        Texture_Mean = request.form.get('Texture_Mean')
        Perimeter_Mean = request.form.get('Perimeter_Mean')
        Area_Mean = request.form.get('Area_Mean')
        Smoothness_Mean = request.form.get('Smoothness_Mean')
        Compactness_Mean = request.form.get('Compactness_Mean')

        # Check if any of the features are null or empty strings
        if not all([Radius_Mean, Texture_Mean, Perimeter_Mean, Area_Mean, Smoothness_Mean, Compactness_Mean]):
            message = "Please set all the features"
            return render_template('Classification_BreastCancer.html', message=message)
        
        # Convert features to floats if they are not null or empty strings
        Radius_Mean = float(Radius_Mean)
        Texture_Mean = float(Texture_Mean)
        Perimeter_Mean = float(Perimeter_Mean)
        Area_Mean = float(Area_Mean)
        Smoothness_Mean = float(Smoothness_Mean)
        Compactness_Mean = float(Compactness_Mean)

        input_data = np.array([Radius_Mean, Texture_Mean, Perimeter_Mean, Area_Mean, Smoothness_Mean, Compactness_Mean]).reshape(1, -1)

        if 'SVM' in request.form:
            prediction = SVM_BreastCancer_model.predict(input_data)
        elif 'KNearestCentroid' in request.form:
            prediction = NearestCentroid_BreastCancer_model.predict(input_data)
        

        if(prediction is None):
            return render_template('Classification_BreastCancer.html')
        else:
            result = int(prediction[0])
            print(result)
            if(result == 0):
                result = "Benign"
            else:
                result = "Malignant"
            return render_template('Classification_BreastCancer.html', result=result)
        
        
    except (ValueError, TypeError) as e:
        message = "Invalid input format. Please provide valid numeric values for all features."
        return render_template('Classification_BreastCancer.html', message=message)





#ComputerVision
@app.route('/ComputerVision', methods=['GET'])
def ComputerVision():
    return render_template('ComputerVision.html')

@app.route('/ComputerVision_MNIST', methods=['GET'])
def ComputerVision_MNIST():
    return render_template('ComputerVision_MNIST.html')

@app.route('/ComputerVision_MNIST_Up_image', methods=['GET'])
def ComputerVision_MNIST_Up_image():
    return render_template('ComputerVision_MNIST_Up_image.html')


@app.route('/ComputerVision_MNIST_RealTime', methods=['GET'])
def ComputerVision_MNIST_RealTime():
    return render_template('ComputerVision_MNIST_RealTime.html')

 
@app.route("/predict_uploaded_image", methods=["POST"])
def predict_uploaded_image():
    img = Image.open(request.files["img"]).convert("L")

    # predict
    res_json = {"pred": "Err", "probs": []}
    if predict is not None:
        res = predict(img)
        res_json["pred"] = str(np.argmax(res))
        res_json["probs"] = [p * 100 for p in res]


    
    return render_template('ComputerVision_MNIST_Up_image.html', predicted_value=res_json["pred"])



@app.route("/DigitRecognition", methods=["POST"])
def predict_digit():
    img = Image.open(request.files["img"]).convert("L")

    # predict
    res_json = {"pred": "Err", "probs": []}
    if predict is not None:
        res = predict(img)
        res_json["pred"] = str(np.argmax(res))
        res_json["probs"] = [p * 100 for p in res]

    return json.dumps(res_json)


class Predict():
    def __init__(self):
        device = torch.device("cpu")
        self.model = Model().to(device)
        self.model.load_state_dict(torch.load(SAVE_MODEL_PATH, map_location=device))
        self.transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])

    def _centering_img(self, img):
        w, h = img.size[:2]
        left, top, right, bottom = w, h, -1, -1
        imgpix = img.getdata()

        for y in range(h):
            offset_y = y * w
            for x in range(w):
                if imgpix[offset_y + x] > 0:
                    left = min(left, x)
                    top = min(top, y)
                    right = max(right, x)
                    bottom = max(bottom, y)

        shift_x = (left + (right - left) // 2) - w // 2
        shift_y = (top + (bottom - top) // 2) - h // 2
        return ImageChops.offset(img, -shift_x, -shift_y)

    def __call__(self, img):
        img = ImageOps.invert(img)  # MNIST image is inverted
        img = self._centering_img(img)
        img = img.resize((28, 28), Image.BICUBIC)  # resize to 28x28
        tensor = self.transform(img)
        tensor = tensor.unsqueeze_(0)  # 1,1,28,28

        self.model.eval()
        with torch.no_grad():
            preds = self.model(tensor)
            preds = preds.detach().numpy()[0]

        return preds
    


### Clustering 
@app.route('/Clustering')
def Clustering():
    return render_template('Clustering.html')


@app.route('/Clustering_Iris')
def Clustering_Iris():
    return render_template('Clustering_Iris.html')


@app.route('/Clustering_Iris', methods=['GET', 'POST'])
def Clustering_Iris_Predict():
    if request.method == 'POST':
        try:
            sepal_length = float(request.form.get('sepal_length'))
            sepal_width = float(request.form.get('sepal_width'))

            # Create a new data point from user input
            new_data_point = np.array([[sepal_length, sepal_width]])

            # Predict the cluster for the user's input
            predicted_cluster = KMeans_Iris_model.predict(new_data_point)

            if(predicted_cluster is None):
                return render_template('Clustering_Iris.html')
            else:
                result = int(predicted_cluster[0])
                if(result == 0):
                    result = "Setosa"
                elif result == 1:
                    result = "Versicolor"
                else:
                    result = "Virginica"
            return render_template('Clustering_Iris.html', result=result)


        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid input. Please enter valid numbers.'})

    return render_template('Clustering_Iris.html')



@app.route('/Clustering_BreastCancer')
def Clustering_BreastCancer():
    return render_template('Clustering_BreastCancer.html')

### TODO: Display plots to the html code
@app.route('/Clustering_BreastCancer', methods=['GET', 'POST'])
def Clustering_BreastCancer_Predict():
    if request.method == 'POST':
        try:
            # Get user input features (mean radius and mean texture)
            mean_radius = float(request.form.get('mean_radius'))
            mean_texture = float(request.form.get('mean_texture'))

            # Standardize the input features (same as during training)
            user_input = np.array([[mean_radius, mean_texture]])
            user_input = scaler.transform(user_input)

            # Predict the cluster for the user's input
            predicted_cluster = KMeans_Iris_model.predict(user_input)
            if(predicted_cluster is None):
                return render_template('Clustering_BreastCancer.html')
            else:
                result = int(predicted_cluster[0])
                if(result == 0):
                    result = "Setosa"
                elif result == 1:
                    result = "Versicolor"
                else:
                    result = "Virginica"
            return render_template('Clustering_BreastCancer.html', result=result)


        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid input. Please enter valid numbers.'})

    return render_template('Clustering_BreastCancer.html')



### Regression 
@app.route('/Regression')
def Regression():
    return render_template('Regression.html')


@app.route('/Regression_iris', methods=['GET', 'POST'])
def Regression_iris():
    if request.method == 'POST':
        try:
            # Get user input features (sepal length, sepal width, petal length, petal width)
            sepal_length = float(request.form.get('sepal_length'))
            sepal_width = float(request.form.get('sepal_width'))
            petal_length = float(request.form.get('petal_length'))
            petal_width = float(request.form.get('petal_width'))

            # Create a new data point from user input
            user_input = np.array([[sepal_length, sepal_width, petal_length, petal_width]])

            # Predict the regression value for the user's input
            predicted_value = Regression_Iris_model.predict(user_input)

            return render_template('Regression_Iris.html', predicted_value=predicted_value[0])

        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid input. Please enter valid numbers.'})

    return render_template('Regression_Iris.html', predicted_value=None)


@app.route('/Regression_house', methods=['GET', 'POST'])
def Regression_house():
    try:
        # Get input data from the form
        inputs = [float(x) for x in request.form.values()]
        
        # Make a prediction using the model
        prediction = Regression_House_model.predict([inputs])[0]
        
        # Format the prediction as a string
        predicted_value = f"${prediction:.4f}"
        
        return render_template('Regression_House.html', prediction=predicted_value)
    
    except Exception as e:
        return render_template('Regression_House.html', error="Error: " + str(e))




@app.route('/RealTimeFaceDetection', methods=['GET'])
def RealTimeFaceDetection():
    return render_template('RealTimeFaceDetection.html')


@app.route('/ComputerVision_CIFAR', methods=['GET'])
def ComputerVision_CIFAR():
    return render_template('ComputerVision_CIFAR10.html')



@app.route('/Activity_Recognition', methods=['GET'])
def Activity_Recognition():
    return render_template('Activity_Recognition.html')

@app.route('/LanguageTechnology', methods=['GET'])
def LanguageTechnology():
    return render_template('LanguageTechnology.html')

@app.route('/ReinforcementLearning', methods=['GET'])
def ReinforcementLearning():
    return render_template('ReinforcementLearning.html')



if __name__ == '__main__':
    import os
    assert os.path.exists(SAVE_MODEL_PATH), "no saved model"
    predict = Predict()
    app.run(debug=True)


