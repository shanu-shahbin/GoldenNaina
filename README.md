
# GoldenNaina E-commerce Platform

GoldenNaina is an e-commerce platform built using Django and PostgreSQL, featuring wishlist management, coupon functionality, secure payment options, and a customized admin panel. The platform is deployed using AWS services for scalability and performance.

Live at: [www.goldennaina.com](http://www.goldennaina.com)

![GoldenNaina - Google Chrome 9_14_2024 7_56_17 PM](https://github.com/user-attachments/assets/9c310749-a6d8-445c-8a0e-499652455ff5)

---

## Table of Contents

1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Deployment Architecture](#deployment-architecture)
4. [Installation and Setup](#installation-and-setup)
5. [Docker Setup](#docker-setup)
6. [Configuration](#configuration)
7. [Usage](#usage)
8. [Screenshots](#screenshots)
9. [Testing](#testing)
10. [Contributing](#contributing)
11. [License](#license)

---

## Features

- **User Authentication**: Secure signup and login using email and password, with password reset functionality.
- **Wishlist Management**: Users can add and manage their favorite products for future purchases using AJAX for smooth interactions.
- **Product Search**: Full-text search and category-based filtering for easy product discovery.
- **Order Tracking**: Users can track their orders in real time, with detailed status updates.
- **Coupon System**: Apply promotional codes at checkout for discounts.
- **Payment Options**: Integrated **PayPal** and **Cash on Delivery** for flexible payment solutions.
- **Profile Management**: Manage addresses, view wishlist items, and order details from a dedicated profile section.
- **Related Products & Reviews**: Display related products and allow users to add and view reviews on product pages.
- **Size Guide**: A dedicated page to assist users in selecting the correct sizes.
- **Admin Panel**: Custom-built admin panel using **Jazmin** for managing products, orders, and users.

---

## Tech Stack

### Frontend
- **HTML5**: For page structure and layout.
- **CSS3**: For responsive design and styling.
- **JavaScript**: For adding interactive elements and enhancing user experience.
- **AJAX**: Used for dynamic wishlist management without reloading pages.

### Backend
- **Django**: A robust Python framework for handling the server-side logic and database management.
- **PostgreSQL**: A relational database for storing product, user, and order data.
- **Psycopg2**: PostgreSQL adapter to enable efficient database queries.

### Payment Integration
- **PayPal SDK**: Integrated to process online payments.
- **Cash on Delivery**: Available as an offline payment option for customers.

### Admin Panel
- **Jazmin**: Custom admin interface to manage backend data efficiently.

### Deployment
- **AWS EC2**: For hosting the application server.
- **Amazon S3**: For storing static files such as images, CSS, and JavaScript.
- **RDS PostgreSQL**: Managed database service with automatic backups.
- **Nginx**: Used as a reverse proxy for managing incoming web traffic.
- **Gunicorn**: Application server used to handle requests.
- **Cloudflare**: DNS management, CDN, and protection against DDoS attacks.
- **Docker**: Containerized the application for easier deployment.
- **Amazon ECR**: Docker images are uploaded to Amazon Elastic Container Registry (ECR) for secure and scalable storage.

---

## Deployment Architecture
*Diagram showing the deployment architecture with AWS services*
<br>
![DALL·E 2024-09-15 19 12 44 - A detailed cloud architecture diagram for the GoldenNaina e-commerce platform using AWS services  The diagram should include_ 1) Users accessing the p](https://github.com/user-attachments/assets/1abebc9b-c208-4146-9b17-32625e899269)


---

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/shanu-shahbin/GoldenNaina.git
   cd GoldenNaina
Create a virtual environment and activate it:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up environment variables for database, AWS services, and PayPal integration in a .env file:

bash
Copy code
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_SECRET_KEY=your_paypal_secret_key
Apply migrations and run the server:

bash
Copy code
python manage.py migrate
python manage.py runserver
Docker Setup
To containerize and deploy the application using Docker and Amazon ECR:

Create a Dockerfile in the root directory of your project:

dockerfile
Copy code
# Dockerfile
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . /app/

# Expose the port
EXPOSE 8000

# Run the Django application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
Build the Docker image:
bash
Copy code
docker build -t goldennaina:latest .
Login to ECR:

bash
Copy code
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com
Tag and Push the Docker image to ECR:

![Elastic Container Registry - Private repositories - Google Chrome 9_13_2024 9_11_08 PM](https://github.com/user-attachments/assets/60f7d96c-32d0-4cd5-888d-7cd35b3c3278)
<br>
bash
Copy code
docker tag goldennaina:latest <aws_account_id>.dkr.ecr.<region>.amazonaws.com/goldennaina:latest
docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/goldennaina:latest

![Elastic Container Registry - Private repositories - Google Chrome 9_13_2024 9_11_44 PM](https://github.com/user-attachments/assets/9636ff0d-74e6-4ca9-9561-4392bac6944f)
<br>
Configuration
Before running the project, configure the following environment variables:

SECRET_KEY: Your Django secret key.
DATABASE_URL: PostgreSQL connection URL.
PAYPAL_CLIENT_ID: PayPal SDK client ID.
PAYPAL_SECRET_KEY: PayPal SDK secret key.
AWS_ACCESS_KEY_ID: AWS access key for managing S3.
AWS_SECRET_ACCESS_KEY: AWS secret key for managing S3.
S3_BUCKET_NAME: S3 bucket name for static files.
Place these in a .env file at the root of the project.

Usage
Once the setup is complete, the application can be accessed via http://localhost:8000 in a local environment.

Key functionalities:

Browse products, add to wishlist, and checkout with payment.
Access user profile to manage orders and addresses.
Admins can log in to the custom admin panel to manage users, products, and orders.
Screenshots
1. User Dashboard

![GoldenNaina - Google Chrome 9_15_2024 7_33_57 PM](https://github.com/user-attachments/assets/5254490f-2c8c-432d-96da-0040a95d4cac)

![GoldenNaina - Google Chrome 9_15_2024 7_34_18 PM](https://github.com/user-attachments/assets/310cdc4d-5f3e-476f-ae78-e1ffea3d8e2d)

2. Admin Panel

![GoldenNaina - Google Chrome 9_15_2024 7_35_41 PM](https://github.com/user-attachments/assets/09f5f1fa-0b79-4eff-8d6d-0eac874652d5)

![GoldenNaina - Google Chrome 9_15_2024 7_35_57 PM](https://github.com/user-attachments/assets/2b1333f1-e3a1-4c63-91a3-509b6dad43d6)

3. Product Page

![GoldenNaina - Google Chrome 9_15_2024 7_37_30 PM](https://github.com/user-attachments/assets/10451d8c-c0af-47fc-b23c-1b68c4cdd9aa)

![GoldenNaina - Google Chrome 9_15_2024 7_37_59 PM](https://github.com/user-attachments/assets/a2bf4350-89f4-4069-88a0-061a69042411)

4. Payment Options
   
5. Deployement
![Launch an instance _ EC2 _ us-west-2 - Google Chrome 9_7_2024 6_22_13 PM](https://github.com/user-attachments/assets/00b58004-1296-440b-8567-219f68d063e0)

![CreateSecurityGroup _ EC2 _ us-west-2 - Google Chrome 9_7_2024 6_33_13 PM](https://github.com/user-attachments/assets/c6da987c-e400-4c2e-b32e-11cbf0465247)

![Database Details - RDS Management Console - Google Chrome 9_10_2024 1_30_54 PM](https://github.com/user-attachments/assets/a8d35b01-5457-4f3d-b310-3d28d6d52fd1)

![Database Details - RDS Management Console - Google Chrome 9_10_2024 1_32_25 PM](https://github.com/user-attachments/assets/eba2088d-86f4-4bf1-a9ba-d5360ebd49bf)

![ModifyInboundSecurityGroupRules _ EC2 _ us-west-2 - Google Chrome 9_12_2024 1_04_01 PM](https://github.com/user-attachments/assets/591f9eaa-d4cd-4563-a5a6-3bb74daf9838)

![Elastic Container Registry - Private repositories - Google Chrome 9_13_2024 9_14_18 PM](https://github.com/user-attachments/assets/a2594e33-fecd-4a89-9f1c-0f23452d5cc3)

![Elastic Container Registry - Private repositories - Google Chrome 9_13_2024 9_14_33 PM](https://github.com/user-attachments/assets/5266e6be-1e93-4b50-ac1f-c1bad81edca3)

![Elastic Container Registry - Private repositories - Google Chrome 9_13_2024 9_14_53 PM](https://github.com/user-attachments/assets/2ffea86d-db11-41a2-864a-c911cac22427)


Contributing
Contributions are welcome! If you find any issues or have feature requests, please open an issue or submit a pull request. Before contributing, please ensure you:

Fork the repository.
Create a new branch for your feature/fix.
Commit your changes with descriptive commit messages.
Open a pull request to the main branch.

License
This project is licensed under the MIT License. See the LICENSE file for details.


