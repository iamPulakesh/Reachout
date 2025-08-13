## Overview

ReachOut is a Flask-based web application deployed on AWS that allows people to submit real-time reports of incidents such as accidents, disasters or safety concerns. The application supports image uploads, geolocation via Google Maps API and structured data storage.

The goal is to help people and authorities — stay informed and connected through transparent public reporting

---

## Features
- Submit incident reports with up to 3 images/videos
- View all reported incidents in a searchable table
- Attachments stored securely in AWS S3
- Modular Flask app using Blueprints
- MySQL database integration
- Secure AWS credentials via GitHub Actions secrets
- CI pipeline with linting and import checks

---

## Requirements
- Python 3.11+
- MySQL database
- AWS account (S3, SSM Parameter Store)
- AWS credentials (set as environment variables or GitHub secrets)

---

## Setup
1. **Clone the repository:**
   ```sh
   git clone https://github.com/iamPulakesh/Reachout.git
   cd Reachout
   ```
2. **Install dependencies:**
   ```sh
   pip install -r Requirements.txt
   ```
3. **Configure AWS and DB:**
   - Store DB and S3 credentials in AWS SSM Parameter Store
   - Set AWS credentials as environment variables or GitHub secrets
4. **Run the app:**
   ```sh
   python3 app.py
   ```
5. **Access the app:**
   - http://localhost:5000/

---

## Project Structure
```
Reachout/
├── app.py
├── Requirements.txt
├── db/
│   └── connection.py
├── routes/
│   ├── main_routes.py
│   ├── admin_routes.py
│   └── image_routes.py
├── templates/
│   ├── index.html
│   ├── admin.html
│   └── view_reports.html
└── .github/
    └── workflows/
        └── reachout-ci.yml
```






