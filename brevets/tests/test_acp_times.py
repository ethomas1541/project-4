"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""

from acp_times import *
import nose    # Testing framework
import logging
import arrow

epoch = arrow.get('1970-01-01T00:00:00+00:00')
alitime = arrow.get('2011-10-21T11:00:00+00:00')

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

def get_formatted_date(function, cdist, bdist, stime):
    return function(cdist, bdist, stime).format('YYYY-MM-DD HH:mm:ss')

def test_opens_website_example_1():

    # First test shown on the website linked in acp_times.py's header.

    assert(get_formatted_date(open_time, 60, 200, epoch) == "1970-01-01 01:46:00")      # 1H46
    assert(get_formatted_date(open_time, 120, 200, epoch) == "1970-01-01 03:32:00")     # 3H32
    assert(get_formatted_date(open_time, 175, 200, epoch) == "1970-01-01 05:09:00")     # 5H09
    assert(get_formatted_date(open_time, 200, 200, epoch) == "1970-01-01 05:53:00")     # 5H53

def test_closes_website_example_1():

    # Same thing, with the close times.

    assert(get_formatted_date(close_time, 60, 200, epoch) == "1970-01-01 04:00:00")     # 4H00
    assert(get_formatted_date(close_time, 120, 200, epoch) == "1970-01-01 08:00:00")    # 8H00
    assert(get_formatted_date(close_time, 175, 200, epoch) == "1970-01-01 11:40:00")    # 11H40
    assert(get_formatted_date(close_time, 200, 200, epoch) == "1970-01-01 13:20:00")    # 13H20

def test_opens_website_example_2():

    # Not doing exactly 50km intervals like the website said. Now that <200 controls have been proven to behave right,
    # what about those >200?

    assert(get_formatted_date(open_time, 350, 400, epoch) == "1970-01-01 10:34:00")     # 10H34
    assert(get_formatted_date(open_time, 550, 600, epoch) == "1970-01-01 17:08:00")     # 17H08

def test_closes_website_example_2():

    # Same w/ close times

    assert(get_formatted_date(close_time, 550, 600, epoch) == "1970-01-02 12:40:00")    # 36H40
    assert(get_formatted_date(close_time, 600, 600, epoch) == "1970-01-02 16:00:00")    # 16H00

def test_website_example_3():
    
    # Example 3 only has one open and one close time. I test them both here.

    assert(get_formatted_date(open_time, 890, 1000, epoch) == "1970-01-02 05:09:00")    # 29H09
    assert(get_formatted_date(close_time, 890, 1000, epoch) == "1970-01-03 17:23:00")   # 65H23


def test_ali():
    assert(get_formatted_date(close_time, 1140, 1000, alitime) == "2011-10-25 00:30:00")

# Test numbers that are out of range

def test_bad_numbers():
    with nose.tools.assert_raises(OverflowError):
        open_time(-1, 200, epoch)
    
    with nose.tools.assert_raises(OverflowError):
        close_time(-1, 200, epoch)

    with nose.tools.assert_raises(OverflowError):
        open_time(1201, 200, epoch)
    
    with nose.tools.assert_raises(OverflowError):
        close_time(1201, 200, epoch)

# Test lengths that aren't legal
# 199, 399, 599, 799, 999

def test_bad_brev_lengths():
    for i in range(1, 6):
        with nose.tools.assert_raises(IndexError):
            open_time(250, 200 * i - 1, epoch)

        with nose.tools.assert_raises(IndexError):
            close_time(250, 200 * i - 1, epoch)


# Test control distances that make no sense (are greater than overall brevet distance)

def test_control_len_greater():
    with nose.tools.assert_raises(ArithmeticError):
        open_time(400, 200, epoch)

    with nose.tools.assert_raises(ArithmeticError):
        close_time(400, 200, epoch)

# Test bad object types

def test_bad_instances():
    with nose.tools.assert_raises(TypeError):
        open_time("apple", [200, 300], {"foo":"bar"})

    with nose.tools.assert_raises(TypeError):
        close_time(object, arrow.Arrow, 34)