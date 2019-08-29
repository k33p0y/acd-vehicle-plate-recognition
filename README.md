# Plate Number Recognition

Used in ACD School For recognizing vehicles' plate number that in and out from the campus.

## Installation

1. Download and install Python3 from this url https://www.python.org/downloads/
2. Verify the version:

```()
python3 -V
```

3. Install pip by following this url: https://www.liquidweb.com/kb/install-pip-windows/

4. Install virtualenv

```()
pip install virtualenv

in Windows:
source localenv/Scripts/activate
in Linux and OSX:
source localenv/bin/activate
```

5. Intall Django
6. Check Django version

```()
python -m django --version
```

## Running

1. Migrate

```()
cd pnr_sys
python manage.py migrate
python manage.py runserver
```

## Create SuperUser

```()
python manage.py createsuperuser
```

## Install Required Packages

```()
pip install wheel
pip install django-crispy-forms
pip install pytesseract
pip install Pillow
pip install opencv-python or pip install opencv-contrib-python-headless
pip install django-mathfilters
pip install django-keyboard-shortcuts
pip install schedule
```
