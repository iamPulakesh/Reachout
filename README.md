## Overview

ReachOut is a Flask-based web application deployed on AWS that allows people to submit real-time reports of incidents such as accidents, disasters or safety concerns. The application supports image uploads, geolocation via Google Maps API and structured data storage.

The goal is to help people and authorities — stay informed and connected through transparent public reporting.

---

## Features

- Submit reports with location, description, incident type and image
- Google Maps API integration for accurate location tagging
- Public view to access all submitted reports
- Uploaded images stored in Amazon S3
- Data stored securely in Amazon RDS
- Deployed in a secure AWS VPC using EC2

---

## AWS Services Used

| Service        | Purpose                                                 |
|----------------|---------------------------------------------------------|
| **EC2**         | Hosts the Flask application                             |
| **S3**          | Stores uploaded images securely                         |
| **RDS / MySQL** | Stores incident report data in structured format        |
| **VPC**         | Isolated networking environment for the application     |
| **IAM**         | Manages secure access between EC2 and other services    |
| **CloudFormation** | Automates infrastructure deployment as code          |

---

## How It Works

1. **User submits a report** with location, incident type, details and image(optional).
2. **Google Maps API** fetches coordinates from the address.
3. Image is uploaded to **S3** and metadata is stored in **RDS**.
4. Public can view the reports which are submitted and share it with the respective authority.

---

## Deployment Instructions

1. Launch your stack using the `cloudformation-template.yaml`.
2. SSH into the EC2 instance and deploy the Flask app.
3. Configure environment variables for DB and S3.
4. Ensure the EC2 instance has proper IAM role and VPC settings.

---
## Setup

1. Deploy Infra
aws cloudformation create-stack \
  - stack-name incident-reporter-stack \
  - template-body file://cloudformation-template.json \

2. SSH into EC2
`ssh -i your_accesskey.pem ec2-user@ ec2-public-ip`

3. App Setup
`sudo yum install python3 git -y`

4. Run the Flask app
`python3 app.py`





