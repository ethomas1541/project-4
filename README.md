Elijah Thomas ethomas7@uoregon.edu

CS 322 Project 4

Calculator for ACP Brevet open and close times based on:

	https://rusa.org/pages/acp-brevet-control-times-calculator

Provides quick, refresh-less updates for each row in a table based on user input. The last 3 columns of the chart
are extrapolated from user input. Requests are handled with AJAX and sent to a rudimentary Flask-based server.

Frontend: 					brevets/templates/calc.html
Web server: 				brevets/flask_brevets.py
Backend:					brevets/acp_times.py
Unit Tests for Backend:		brevets/tests/test_acp_times.py

Comments in each of these files provide much further detail.