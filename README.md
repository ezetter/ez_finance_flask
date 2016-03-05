#EZ Portfolio

This is a web app to track personal investment portfolios. It allows the user to maintain accounts and individual investments within those accounts. It has features to track the value over time, to compare the values by investment type, owner, etc., and to estimate future values using monte carlo simulations. It includes both numerical and charting capabilities in order to visualize characteristics of portfolios.

##Installation and Setup

### Environment Setup

Clone this repo. I used conda for dependency management. As such dependencies are listed en environment.yml. If you use conda you can create an environment with these dependencies by executing:

```
    conda env create -f environment.yml
```

Then you can run the app from within that environment. If you use another environment manager (e.g. virtualenv), or none at all, you're on your own. environment.yml should be help.

### Database Setup

Currently the database is configured for SQLLite (edit webapp/config.py if you want something else.) Create the database by executing:
 
```
    python manage.py db upgrade
```

### Running

Once the above procedures are completed you can run the server be executing:

```
    python manage.py server
```
The webapp will by default be at http://127.0.0.1:5000/.

You can also operate from the Flask shell by executing:

```
    python manage.py shell
```

Have fun managing your investments!