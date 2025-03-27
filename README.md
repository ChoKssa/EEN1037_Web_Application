# Factory Machinery Tracking System

This project is a web application built with Django to track the status and repairs of factory machinery. It runs inside a Docker container and is easily configurable using environment variables.

---

## 🔧 Requirements

- [Docker](https://www.docker.com/)
- (Optional) [Docker Compose](https://docs.docker.com/compose/) for easier multi-container orchestration

---

## 🚀 Quick Start with Docker Compose

This is the easiest way to run the application with a PostgreSQL database and default settings.

### 1. Clone the repository

```bash
git clone https://github.com/ChoKssa/EEN1037_Web_Application.git factory-tracking
cd factory-tracking
```

### 2. Launch the app

```bash
docker compose up --build
```

This command will:

- Build the Django app image
- Start the Django app and PostgreSQL database in containers
- Automatically run database migrations and create an admin user

You can access the app at [http://localhost:8000](http://localhost:8000)

---

## ⚙️ Using Custom Environment Variables

You can override the default admin account and database settings by passing your own variables.

### Option 1: Edit the `.env` file (automatically loaded)

Create a file named `.env` in the project root (see [.env.example](./.env.example)):

```shell
DJANGO_SUPERUSER_USERNAME=myadmin
DJANGO_SUPERUSER_PASSWORD=secretpass
DJANGO_SUPERUSER_EMAIL=myadmin@example.com
DATABASE_URL=postgres://customuser:custompass@db:5432/customdb

POSTGRES_DB=customdb
POSTGRES_USER=customuser
POSTGRES_PASSWORD=custompass

```

Then run:

```bash
docker compose up --build
```

### Option 2: Pass variables inline

```bash
DJANGO_SUPERUSER_USERNAME=myadmin \
DJANGO_SUPERUSER_PASSWORD=secretpass \
DATABASE_URL=postgres://customuser:custompass@db:5432/customdb \
docker compose up --build
```

---

## 🧪 Running the App WITHOUT the PostgreSQL Service

If you want to connect the Django app to an external or already running database, you can start only the app:

```bash
docker compose up --build factory
```

Make sure the `DATABASE_URL` environment variable points to a valid database (PostgreSQL or SQLite).

---

## 🏗️ Build the Image Manually (Without Compose)

You can build the app using only the `Dockerfile`:

```bash
docker build -t factory_app ./factory_tracking
```

---

## ▶️ Run the App from the Image

After building the image, run the app manually:

```bash
docker run -p 8000:8000 \
  -e DJANGO_SUPERUSER_USERNAME=admin \
  -e DJANGO_SUPERUSER_PASSWORD=admin \
  -e DJANGO_SUPERUSER_EMAIL=admin@example.com \
  -e DATABASE_URL=postgres://factoryuser:factorypass@your-db-host:5432/factorydb \
  factory_app
```

Make sure to:

- Replace `your-db-host` with the address of your PostgreSQL server or define the exact url of your database
- Mount a volume if you want to persist files or use SQLite using `-v` flag

Example with volume (for SQLite):

```bash
docker run -p 8000:8000 \
  -v $(pwd)/app/storage:/app/storage \
  -e DATABASE_URL=sqlite:////app/storage/db.sqlite3 \
  factory_app
```

---

## 💠 Useful Tips

- The Django app automatically creates a superuser if it doesn’t exist
- You can change default credentials using environment variables
- Database migrations run automatically on startup
- You can use PostgreSQL (recommended) or SQLite for testing

---

## 🪩 Clean Up

To stop and remove containers and volumes:

```bash
docker compose down -v
```

---

## 📁 Project Structure

```shell
project/
│
├── factory_tracking/           # Contains app source code
    ├── Dockerfile              # Build script for the app image
    ├── docker_entrypoint.sh    # Custom entrypoint for startup logic
    └── requirements.txt        # Python dependencies
└── docker-compose.yml          # Main Docker Compose file
```

---

## 👨‍💻 Contact

If you encounter issues, please contact the team or refer to the project documentation.
