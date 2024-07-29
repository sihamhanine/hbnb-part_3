# HBNB Project

## Description

The HBNB project is part of the Holberton School curriculum. It aims to create a basic replica of an Airbnb-like application, allowing CRUD operations (Create, Read, Update, Delete) on a JSON file-based database via HTTP requests.

## Features

- Create, update, and delete users.
- Add, modify, or delete rental places.
- Create, modify, or delete amenities for a place.
- Post, update, or delete reviews for places.

## Technologies Used

- **Python 3.10.12**: Main programming language.
- **Flask**: Framework to handle the RESTful API.
- **Gunicorn**: WSGI server to deploy the application.
- **Unittest**: Unit testing module.
- **SwaggerUI**: API documentation.
- **Docker**: Containerization of the application.
- **GitHub Actions**: Continuous integration and deployment.

### Future Implementations

- **CI/CD**: improve our GitHUB Actions workflow to achieve Continuous Implementation and Continuous Development.
- **SQLAlchemy**: or another database toolkit, to migrate our JSON base system.
- **Security**: will be enforced and based on authentification tokens amongst other systems.
- **Front end**: a proper website, with neat HTML, CSS and JavaScript.

## Installation

### Prerequisites

- Docker installed on your machine.

### Installation Steps

1. **Clone the repository**

    ```sh
    git clone https://github.com/niranois13/holbertonschool-hbnb.git
    cd holbertonschool-hbnb
    ```

2. **Build the Docker image**

    ```sh
    docker image build . -t "hbnb"
    ```

3. **Run the Docker container**

    By default, the application runs on port 5000.

    ```sh
    docker run -t -p 5000:5000 -v hbnb_data:/home/hbnb/hbnb_data hbnb
    ```

    To run the application directly with GitHub:

    ```sh
    docker run -t -p 5000:5000 -v hbnb_data:/hbnb_data --pull=always ghcr.io/niranois13/holbertonschool-hbnb:latest
    ```

## Usage

Once the container is running, you can access the API at `http://localhost:5000`.

API documentation is available here:

`http://localhost:5000/api/docs`

If needed, replace `http://localhost:5000` with the machine's IP address `http://ip`

## Contributors

### For the Part 2:
MEYNETGAUTHIER Emmanuel (https://github.com/8690holbertonstudents)  
DOYEN Nicolas (https://github.com/niranois13)

#### For the Part 1:
ROMAND Jérôme (https://github.com/jeje-digifab)  
MARTIN Maxime (https://github.com/cosmos510)  
DOYEN Nicolas (https://github.com/niranois13)  
