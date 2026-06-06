pipeline {

    agent any

    stages {

        stage('Test Flask') {
            steps {
                script {
                    docker.image('python:3.11').inside('-u root') {
                        sh 'pip install -r requirements.txt'
                        sh 'python test.py'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t flask_hello:latest .'
            }
        }
    }
}