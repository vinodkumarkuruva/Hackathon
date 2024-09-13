Project Name : Hackathon Management System API

Introduction : The Hackathon Submissions App is designed for hosting hackathons and managing submissions. Authorized users can create hackathons, and participants can submit code, files, or links as their hackathon entries. The platform provides APIs for listing, registering, and making submissions to hackathons, as well as viewing submitted projects.

Technologies : Backend      :  Flask, Flask-SQLAlchemy, Flask-Migrate , Flask- Login
               Database     :  Sqlite
               Other Tools  :  Git and Postman
               
Features     :  Create Hackathons       :   Authorized users can create hackathons with details like title, description, images, type of submission, start and end times, and prize information.
                Hackathon Listing       :   List all active hackathons.
                Hackathon Registration  :   Users can register for hackathons.
                Submissions             :   Users can submit files, images, or links based on the hackathon type.
                View Registrations      :   Users can list hackathons they are registered for.
                View Submissions        :   Users can view their submissions for any hackathon they've registered for.


-->Installation and Setup

1. Clone the Repositry : https://github.com/vinodkumarkuruva/Hackathon.git
                         cd Hackathon

2 . Prerequisites -   Python 3.7+: Ensure that Python is installed on your system
                      Flask - As a Framework
                      Docker: For containerizing the application
                      

3 . Steps to Set Up -     Create a virtual environment          :    python3 -m venv < name of virtual Environment > 
 	
                          To activate the virtual Environment   :    < name of virtual Environment >/Scripts/activate 
 
                           Install dependencies                  :    pip install -r requirements.txt
                         
                           Set up the database                   :    flask db init
                         	                                            flask db migrate -m "Initial migration"
                                                                      flask db upgrade
                         
                           Run the server                        :    Python run.py (or) flask run
                         
                           * The application will start and be accessible at http://127.0.0.1:5000
                           
                           
4 . Running the Application with Docker -   	 Build the Docker image              :     docker build -t < name of image > .
 
                                             	 Run the Docker container            :     docker run -p 5000:5000 < name of Image >
    
                                              * The application will be available at http://localhost:5000

5 . Structure of the application - 


 /Hackathon
 ├── app/
 │   ├── models.py        		    # Contains the database models (Books, Students, Inventory, Issue)
 │   ├── routes.py         		    # Defines the API endpoints
 │   ├── views.py          		    # Contains business logic
 ├── __init__.py        				  # Initializes the Flask app and SQLAlchemy
 ├── requirements.txt   				  # Python dependencies         
 ├── Dockerfile         				  # Docker configuration for containerizing the app
 ├── migrations/        				  # Directory for database migrations
 ├── app.py             				  # Script for running the application            
 └── README.md              		   # Project documentation


 6 . Other Info - 

  --> Error Handling: The application returns appropriate HTTP 400 status codes for bad requests.

 --> Modularity: The application is designed to be modular, with separate services handling business logic, making the codebase easy to maintain and extend.

 --> Docker Support: A Dockerfile is included for containerization, making it easy to deploy the application in different environments.

                                              
