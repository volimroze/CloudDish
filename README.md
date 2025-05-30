# CloudDish
A lightweight, cloud-native application for restaurant order tracking and automated daily reporting using AWS services.

## 📌 Project Description
CloudDish is a serverless application designed to help restaurants monitor daily orders and automatically generate and email report summaries. It leverages AWS Lambda, DynamoDB, EventBridge, S3, SNS, and CloudWatch, with an optional EC2-hosted or static HTML frontend.

## ⚙️ Architecture Overview
- **Frontend**:
  - Option 1: EC2 instance with Apache (traditional hosting)
  - Option 2: Static HTML/JS interface (serverless)

- **Backend** (fully serverless):
  - AWS Lambda
  - Amazon API Gateway
  - Amazon DynamoDB
  - Amazon S3
  - Amazon EventBridge
  - Amazon SNS
  - Amazon CloudWatch

## 🚀 Features
- Submit orders via web interface
- Store order data in DynamoDB
- Daily automated report generation at 23:59 CET
- Report storage in S3
- Email delivery of reports via SNS
- Monitoring and logs via CloudWatch

## 🧪 How to Run the Project

### ✅ 1. Clone the frontend code (or copy HTML files)
```bash
git clone https://github.com/volimroze/CloudDish.git
```
Upload to EC2 or host locally.

### ✅ 2. Deploy Lambda functions
```bash
zip submitOrderHandler.zip submitOrderHandler.py
aws lambda update-function-code --function-name submitOrderHandler --zip-file fileb://submitOrderHandler.zip
```
Repeat for `generateDailyStatsHandler` and `getMostOrderedDishesHandler`.

### ✅ 3. Trigger Lambda manually (optional)
```bash
aws lambda invoke --function-name generateDailyStatsHandler output.json
```

### ✅ 4. Open frontend
If hosted on EC2:
```
http://<your-ec2-ip>
```

### ✅ 5. View reports in S3
```bash
aws s3 ls s3://clouddish-daily-reports/
```

## 🖥️ Example Output
- ✅ Email with daily summary
- ✅ `.txt` or `.csv` file in S3
- ✅ CloudWatch logs confirming Lambda steps

## 📷 Screenshots
See `Appendix A` and `Appendix B` in the project report.

## 📦 Technologies Used
| Service       | Purpose                     |
|---------------|-----------------------------|
| AWS Lambda    | Backend logic               |
| API Gateway   | HTTP request handling       |
| DynamoDB      | Data storage                |
| EventBridge   | Daily task scheduling       |
| SNS           | Email notifications         |
| S3            | Report storage              |
| CloudWatch    | Monitoring & logs           |
| EC2 (optional)| Host frontend               |

## 👤 Authors
- **Isidora Erakovic**
- **Mattia Benatti**
