-----installing dependent packages-----
pip install -r requirements.text

-----for running the project----
python manage.py runserver

-----assumptions-----
1. The card number length should be 16, cvv should be of length 3 and card should not be expired for a a success status.
2. Also, card type must be either "creditcard" or "debitcard"
