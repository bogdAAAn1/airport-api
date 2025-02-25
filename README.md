# ✈️ Airport-API

The Airport API service is designed to efficiently manage and monitor flight data, including airport details, 
flight schedules, routes, and aircraft information. Built with DRF, it offers a RESTful interface for retrieving 
and managing aviation-related data.


## 🛠 Installing using GitHub

Before you begin, ensure you have met the following requirements:
 - ✅ Install PostgresSQL and create db
 - ✅ Python3.13 must be already installed. 

## 🚀 Run the project locally without Docker

## Installed

1. Clone the repository:
```
git clone https://github.com/bogdAAAn1/airport-api/tree/develop
```
2. Go to the project directory:
```
cd airport_api
```
3. Create a virtual Python engine and activate it:
```
python -m venv venv 
source venv/bin/activate(on macOS)
venv\Scripts\activate(on Windows)
```
4. Set the project assignments:
```
pip install -r requirements.txt
```
#### If you want to make your own changes, you can additionally install the requirements-dev.txt
```
pip install -r requirements-dev.txt
```
## ⚙️ Configuration Environment Variables:
  - Create a file named .env, using .env.sample as an example.
  - Make sure you have replaced all the dummy keys with your actual data.

##### django settings
```
set SECRET_KEY=<secret_key>
set DEBUG=<debug>
```
##### database
```
set POSTGRES_DB=<db_name>
set POSTGRES_DB_PORT=<db_port>
set POSTGRES_USER=<db_user>
set POSTGRES_PASSWORD=<db_password>
set POSTGRES_HOST=<db_host>
```

## 🚦 Starting the server
1. Create database migrations:
```
python maange.py makemigrations
python manage.py migrate
```

2. Start the development server:
```
python manage.py runserver
```

The API should now be accessible at http://127.0.0.1:8000/api/airport-api/

## 🐳 RUN with Docker


Add this fields to .env file
```
set PGADMIN_DEFAULT_EMAIL=<email>
set PGADMIN_DEFAULT_PASSWORD=<password>
```

Docker should bу installed

```
docker-compose build
```
```
docker-compose up
```

# 🔑 Getting access
 - create user api/user/register/
 - get access token api/user/token/

 - To authenticate, include the obtained token in your request headers with the format:
```
 - Authorization: Bearer <your-token>
```

## 📜 API Documentation

- The API is documented using the OpenAPI standard.
- Access the API documentation by running the server and navigating to http://127.0.0.1:8000/api/doc/swagger/
  or http://127.0.0.1:8000/api/doc/redoc/.

## ✨ Features:

## 🔑 Authentication & Security  
- Supports **JWT authentication** to ensure data security.  
- Allows users to **create profiles** using email and password.  

## 🎫 Ticket & Order Management  
- **Add flight tickets**, specifying row and seat numbers.  
- **View order status** for authenticated users.  

## 📆 Flight Information  
- **Detailed flight data**, including routes, departure and arrival times, aircraft details, and seat availability.  
- **Filter and search flights** by various parameters.  

## 🌍 Airport Details  
- **Comprehensive airport database**, including names, codes, and locations relative to major cities and countries.  

## 🛤 Route Insights  
- **Access route details**, including departure and destination airports.  
- **Calculate distances** between airports.  
