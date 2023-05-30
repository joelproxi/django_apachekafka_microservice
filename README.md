 




<div align="center">
   
<h1>Build Blog App with Django Framework and Apache-Kafka using Microservices architecture .</h1>
<h3 align="center"> In this project, we are going to transfrom a blog app in monolihtic architecture on micriservice architechture using django and apache kafka <a href="https://github.com/joelproxi/myblog">
</h3>
</div>

<br>

<p><em><u>NB:</u> This tutoriel it's not for beginers</em></p>


<!-- INSTALLATION -->
## Installation
1. <a href="#python-installation">Install Python</a> ;
2. Clone the project in desired directory ;
   ```sh
   git clone https://github.com/joelproxi/django_rabbitMQ_blog_miscroservice.git
   ```
3. Move to directory  folder ;
   ```sh
   cd path/to/django_rabbitMQ_blog_miscroservice
   ```
4. Create a virtual environnement *(More detail to [Creating a virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment))* ;
    * For Windows :
      ```sh
      python -m venv env
      ```
    * For Linux :
      ```sh
      python3 -m venv env
      ```
5. Activate the virtual environment ;
    * For Windows :
        * For cmd shell :
            ```sh
            .\env\Scripts\activate.bat
            ```
        * For powershell shell : 
            ```sh
            .\env\Scripts\activate.ps1
            ```
    * For Linux and MacOS :
      ```sh
      source env/bin/activate or . env/bin/activate
      ```
6. Install package of requirements.txt ;
   ```sh
   pip install -r requirements.txt
   ```

7. How to run the application
    * Using Docker: docker-compose up

    * Using shell commands
        * Move to posts project folder and run these following command :
            * In the first shell
                ```sh
                python comsumer.py
                ```
            * In the second shell
                ```sh
                python manage.py runserver localhost:8000
                ```
        * And the end, move to comments project folder and run these following command :
            * In the first shell
                ```sh
                python comsumer.py
                ```
            * In the second shell
                ```sh
                python manage.py runserver localhost:8001
                ```

8. Open a browseable api like Postman, start the test and enjoy!!






