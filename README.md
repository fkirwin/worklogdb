To run unittest try:
python -m unittest discover -s C:/TreehouseProjects/worklogdb -t C:\TreehouseProjects\worklogdb
coverage run test_suite.py
coverage report --omit test_suite.py
**Note - you may have to change your directories to reflect what your environment looks like.  They may fail otherwise.

Application entry point is in the worklogdb.py file.

Search results are paged for better readability.
