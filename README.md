# Project Overview 🌟

This repository presents a **Proof of Concept (POC)** utilizing the **face_recognition** library in Python, a state-of-the-art tool designed for facial recognition applications. This project aims to demonstrate the capabilities of the library by integrating it with simulated data, allowing users to explore the functionalities of facial recognition technology. 🤖📸

## Library and Environment 🛠️

The **face_recognition** library was implemented using **Python version 3.8**. This version is chosen for its stability and compatibility with the library, ensuring optimal performance during development and execution.

## Data Generation 📊

To create a diverse dataset for testing, the project leverages the online platform **[This Person Does Not Exist](https://thispersondoesnotexist.com)**, which generates realistic images of fictitious individuals. The dataset comprises images of both male and female subjects, along with a designated blacklist to mimic data associated with fraudulent actors. 👤❌

Additionally, fictitious demographic data for these individuals was generated using the **FAKER** library in Laravel. For further insights and to access this library, please refer to the project repository [here](https://github.com/jvittortrikx1997/fr_migrations). To populate the database tables with this data, run the migration and seeder commands after configuring your **.env** file to connect to your preferred database. 🗃️🔧

## Installation Instructions 🚀

After setting up the database and populating the tables, install the necessary libraries to run the project. You can achieve this by executing the following commands in your terminal:

```bash
pip install dlib-19.22.99-cp38-cp38-win_amd64.whl
pip install face_recognition
pip install mysql-connector
pip install matplotlib
pip install scipy
