"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)

    # Brevet distance and start date
    brev_dist = request.args.get('brev_dist', 200, type=int)
    start_date = request.args.get('start_date', type = str)
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))

    # Arrow object from start_date string
    start_arrow = arrow.get(start_date)

    # Ideal case, for when all data is valid
    # ecode 0 signifies no error at all
    try:
        open_time = acp_times.open_time(km, brev_dist, start_arrow).format('YYYY-MM-DDTHH:mm')
        close_time = acp_times.close_time(km, brev_dist, start_arrow).format('YYYY-MM-DDTHH:mm')
        result = {"open": open_time, "close": close_time, "ecode": 0}
        return flask.jsonify(result=result)
    
    # Send back an unchanged version of the open and close fields' initial data.
    # Send back an error code the frontend can translate to a human-readable error message
    except OverflowError:
        result = {"open": "mm/dd/yyyy --:-- --", "close": "mm/dd/yyyy --:-- --", "ecode": 1}
        return flask.jsonify(result=result)
    except ArithmeticError:
        result = {"open": "mm/dd/yyyy --:-- --", "close": "mm/dd/yyyy --:-- --", "ecode": 2}
        return flask.jsonify(result=result)

#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
