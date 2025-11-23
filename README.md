### Initialise the project
Clone the project:
```
git clone https://github.com/uv547756/web-app-fossee.git
```
Install all the dependencies:

```
cd web-app-fossee
pip install -r requirements.txt
```

### Initalise the backend
```
# Change to backend directory
cd backend

# Apply migrations
python manage.py migrate

# Create a superuser (used in auth)
python manage.py createsuperuser

# start the server
python manage.py runserver
```
 Create a `.env` file under `/backend/backend/`
 and Enter your django secret key, sample `.env`:
```
SECRET_KEY_DJANGO=<YOUR_SECRET_KEY>
```
 

### Initalise the frontend (React)
1. Navigate to frontend `cd main-frontend` 
2. Install dependencies (if not already done) `npm  install`
3. Run development server `npm run dev`
4. Access frontend at `http://localhost:4173` or `http://127.0.0.1:4173`

### Initalise the frontend (PyQt)
1. Navigate to frontend `cd desktop-frontend`
2. Run frontend app `python main.py`
