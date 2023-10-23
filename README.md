To start the project make sure python 3.11.xx is installed.
Open a terminal and navigate to this project folder.
Run the following command to create a python virtual environment.
                    
                    python3 -m venv .venv

To start the virtual environment run this command.

                    .\\.venv\Scripts\activate

To exit the virtual environment run this command.

                    deactivate

While within the virtual environment, to installed python packages run:

                    pip install -r requirements.txt

To start the flask app use the following command.

                    flask --debug run