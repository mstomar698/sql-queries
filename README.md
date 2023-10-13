### DEMO

> The demo has 3 levels:

- Level 1 - There is many to many relationships between students and teachers. Store their data in the tables. if a teacher is selected the corresponding students will be displayed and if the students are selected then the corresponding teachers should be displayed
- Level 2- Choosing the teacher and a student pair. Generate the certificate
- Level 3- Verify the certificate using the JWT token Deadline is Tue 17th October


### Installation
```bash
git clone https://github.com/mstomar698/sql-queries . 
# Use conda for better performance
conda create -n sql-queries python=3.9
conda activate sql-queries
pip install -r requirements.txt

# Create migrations
python manage.py makemigrations
python manage.py migrate
# create super or register once server starts
python manage.py createsuperuser
# insert demo data
python manage.py insert_json_data
# run server
python manage.py runserver
```