pipeline {
    agent any

    // Skip the automatic checkout to avoid empty repository URL errors
    options {
        skipDefaultCheckout()
    }

    // Optional: AWS environment variables for future Docker deployment
    // environment {
    //     AWS_REGION = 'us-east-1'
    //     ECR_REPO = 'my-repo'
    //     IMAGE_TAG = 'latest'
    //     SERVICE_NAME = 'llmops-medical-service'
    // }

    stages {

        stage('Clone GitHub Repo') {
            steps {
                echo 'Cloning GitHub repo to Jenkins...'
                git branch: 'main', 
                    url: 'https://github.com/Keshav-chand/Medical-RAG-Chatbot.git', 
                    credentialsId: 'github-token'
            }
        }

        stage('Build') {
            steps {
                echo 'Building the project...'
                // Example: install dependencies
                // sh 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                // Example: run tests
                // sh 'pytest tests/'
            }
        }

        stage('Deploy (Optional)') {
            steps {
                echo 'Deploying Docker image to AWS ECR...'
                // Example Docker/AWS commands:
                // sh "aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
                // sh "docker build -t $ECR_REPO:$IMAGE_TAG ."
                // sh "docker tag $ECR_REPO:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:$IMAGE_TAG"
                // sh "docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:$IMAGE_TAG"
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}
