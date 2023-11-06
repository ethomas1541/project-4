"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow
from math import modf

#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#

# Brevet table as determined by the algorithm above.
# Originally stored as a tuple of tuples. This is not necessary because min speeds are always either
# 15km/h or 11.428. Not enough data to warrant storage in a tuple, or even a loop.

brev_maxspeeds = (34, 32, 30, 28)

# Nominal brevet lengths, as shown in the docstrings below
valid_brev_lens = (200, 300, 400, 600, 1000)

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
   """
   Args:
      control_dist_km:  number, control distance in kilometers
      brevet_dist_km: number, nominal distance of the brevet
         in kilometers, which must be one of 200, 300, 400, 600,
         or 1000 (the only official ACP brevet distances)
      brevet_start_time:  An arrow object
   Returns:
      An arrow object indicating the control open time.
      This will be in the same time zone as the brevet start time.
   """ 

   if 0 <= control_dist_km <= 1000 and brevet_dist_km in valid_brev_lens and control_dist_km <= brevet_dist_km:
      # Time shift expressed as decimal hours (1.5 = 1 hour 30 min)
      timeshift_decimal = 0

      # Subtract from this to iterate through the fields of the chart as shown on the website
      cdist_composite = control_dist_km
      for i in range(4):

         # First 3 fields increment by 200km each. Last one increments by 400km.
         if i < 3 and cdist_composite > 200:
            # Find the given max speed for this distance, divide by speed field of chart
            timeshift_decimal += 200/brev_maxspeeds[i]
         else:
            # There's some remainder if it's less than 200. It's no longer as simple as 200/brev_maxspeeds[i]
            timeshift_decimal += cdist_composite/brev_maxspeeds[i]
         cdist_composite -= 200
         if cdist_composite <= 0:
            break

      # Break it into an integer and decimal component
      tshift_parts = modf(timeshift_decimal)

      # For debugging
      print(f"{round(tshift_parts[1])}H{str(round(tshift_parts[0] * 60)).zfill(2)}")

      return brevet_start_time.shift(hours = round(tshift_parts[1]), minutes = round(tshift_parts[0] * 60))

   elif not 0 <= control_dist_km <= 1000:
      raise OverflowError
   
   elif brevet_dist_km not in valid_brev_lens:
      raise IndexError
   
   elif control_dist_km > brevet_dist_km:
      raise ArithmeticError

def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
   """
   Args:
      control_dist_km:  number, control distance in kilometers
         brevet_dist_km: number, nominal distance of the brevet
         in kilometers, which must be one of 200, 300, 400, 600, or 1000
         (the only official ACP brevet distances)
      brevet_start_time:  An arrow object
   Returns:
      An arrow object indicating the control close time.
      This will be in the same time zone as the brevet start time.
   """

   if 0 <= control_dist_km <= 1000 and brevet_dist_km in valid_brev_lens and control_dist_km <= brevet_dist_km:
      # Time shift expressed as decimal hours (1.5 = 1 hour 30 min)
      timeshift_decimal = 0

      # Same idea as above
      cdist_composite = control_dist_km
      if cdist_composite > 600:
         # 600/15 = 40
         timeshift_decimal += 40

         # Move to 11.428 field
         cdist_composite -= 600
      else:

         # Divide remainder by 15 then continue
         timeshift_decimal += cdist_composite/15
         cdist_composite = 0

      # If for any reason this evaluates to true, there's still some remainder. If so, move to 11.428 min speed field
      if cdist_composite:
         timeshift_decimal += cdist_composite/11.428

      # Break apart
      tshift_parts = modf(timeshift_decimal)

      # Debugging
      print(f"{round(tshift_parts[1])}H{str(round(tshift_parts[0] * 60)).zfill(2)}")

      return brevet_start_time.shift(hours = round(tshift_parts[1]), minutes = round(tshift_parts[0] * 60))

   elif not 0 <= control_dist_km <= 1000:
      raise OverflowError
   
   elif not brevet_dist_km in valid_brev_lens:
      raise IndexError
   
   elif control_dist_km > brevet_dist_km:
      raise ArithmeticError
   
# if __name__ == "__main__":
   # print(list(range(1, 6)))