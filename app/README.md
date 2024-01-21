# Healthcare FastAPI App

## Overview

This FastAPI application seamlessly manages patient data through a CRUD system powered by MongoDB. In addition to patient information handling, the app incorporates a state-of-the-art machine learning model for cancer prediction and an open-source API for BMI calculation.

## Features

### Patient Data Management

- **CRUD Operations:** Utilize a MongoDB-backed CRUD system for efficient management of patient data.
- **Secure Access:** Implement OAuth 2 authorization to ensure secure access control and protect sensitive patient information.

### Cancer Prediction Model

- **TensorFlow-Keras Model:** Employ a TensorFlow-Keras model to predict cancer types based on X-ray images.
- **Accuracy and Loss Metrics:** Achieve an impressive accuracy of 0.95 on validation data, with a minimal loss of 0.05.
- **Multiple Model Structures:** Experiment with different model structures, selecting the one that yields superior metrics.

### BMI Calculation API

- **Open-Source BMI API:** Contribute to the open-source community by implementing an API for Body Mass Index (BMI) calculations.
- **Integration:** Seamlessly integrate the BMI calculation API, promoting holistic health approaches within applications.

## Cancer Types Predicted

The cancer prediction model identifies four labels:

1. 'Glioma'
2. 'Meningioma'
3. 'No tumor'
4. 'Pituitary'

## Usage

1. **Patient Data Management:**
   - Create, read, update, and delete patient records effortlessly.

2. **Cancer Prediction:**
   - Upload an X-ray image to predict the type of cancer with high accuracy.

3. **BMI Calculation:**
   - Access the open-source BMI API to calculate Body Mass Index.

## Model Selection

Explore two distinct model structures, with the final implementation based on the model delivering superior metrics.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ilyes-bk/web_services_project.git
