# GoldenNaina

An e-commerce platform built using Django and PostgreSQL, with a range of user-friendly features like wishlist management, coupon functionality, secure payment options, and a customized admin panel. The platform is deployed using AWS services, ensuring scalability and performance.

![Project Logo](path_to_your_logo_image)

## Features

- **User Authentication**: Sign up and log in using email and password, with secure password reset via email.
- **Wishlist Management**: Users can add products to a wishlist for future reference.
- **Product Search**: Full-text search functionality with category-based filtering.
- **Order Tracking**: Users can track the status of their orders in real-time.
- **Coupon System**: Custom coupon feature to apply discounts during checkout.
- **Payment Options**: Integrated with **PayPal** and **Cash on Delivery** for flexible payment options.
- **Profile Section**: Users can manage their addresses, view wishlist items, and order history.
- **Reviews and Related Products**: Users can view and add reviews, and explore related products.
- **Size Guide Page**: Added for assisting users in selecting the right product sizes.
- **Contact & Support**: Users can easily get in touch for support through a dedicated page.
- **Admin Panel**: Customized admin panel using **Jazmin** for managing products, users, and orders.

![Feature Screenshot 1](path_to_screenshot_1)  
*Image: Product page with related products and reviews*

---

## Tech Stack

### Frontend:
- **HTML5**: For structuring the web pages.
- **CSS3**: Styling with responsive design.
- **JavaScript**: Adding interactive elements and animations.

### Backend:
- **Django**: Python web framework used for building the application.
- **PostgreSQL**: Database management for handling product, user, and order data.
- **Psycopg2**: PostgreSQL adapter for database queries.

### Payment:
- **PayPal SDK**: Integrated for handling secure payments.
- **Cash on Delivery**: Option available for UAE-based customers.

### Admin Panel:
- **Jazmin**: Customized admin interface for better management of the platform.

### Deployment:
- **AWS EC2**: Used for server hosting.
- **Amazon S3**: For managing static files (CSS, JS, and media).
- **RDS PostgreSQL**: Database service for handling product and user data.
- **Nginx**: Used as a reverse proxy to manage web traffic.
- **Gunicorn**: Application server for handling requests.
- **Cloudflare**: Used for DNS management, security, and content delivery.

---

## Deployment Architecture

![Architecture Diagram](path_to_architecture_image)  
*Image: Diagram showing the deployment architecture with AWS services*

---

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
