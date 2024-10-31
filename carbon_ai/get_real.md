# Get Real

So, maybe you figured out that this is satire?  I hope so.  Let's go through
some real calculations to try to get a better understanding of software and 
its climate impacts!

## Doing Everything Right

Actually, it is pretty impossible to measure the climate impact of individual 
software components.  It certainly could be done, but to do it right, you'll need
to go beyond pure software.  Modern computer systems are multi-core systems, with
computation split between CPU and GPU, and sometimes other components, such as TPUs.
Things aren't so simple.  So, here's what you'd need to do.

1. Determine the climate impact per unit of electrical energy you use.  You'll want to
   use a tool like [EPA's eGRID Power Profiler](https://www.epa.gov/egrid).  This tool
   is designed to give you annual emissions in pounds of CO2, so, you'll need to do
   some conversions.  But you can get it down to something like a value of 
   `kg(CO2)/kWh(electricity)`.  For example, looking at my area now, we get 0.39 kg/kWh.
   That's pretty close to the US national average, at least circa 2022.

2. Use a power measuring device, at the power outlet, to measure the power usage.  The
   "Kill a Watt" brand is pretty well known, and these, and other similar devices, are
   not very expensive.  Run the function to be tested many times (so it takes maybe a 
   minute or so to run them all), and record the power draw during that time.  We'll call
   the number of times it was run `n`.  Also,
   record how long it took to run.  Then, after a wait period to ensure the temperatures
   return to baseline, record the power draw during that same time interval, without
   running the program.  While doing this test, try to keep all other computer activity
   the same, and minimal.  Finally subtract the energy used during the with-code period
   from the energy used during the baseline period.  Hopefully it is a positive number.

3. Multiply the carbon impact of the energy (the quantity from step 1) with the difference in
   with/without code energy use (determined in step 2), and divide by `n`, the number of times
   the function ran.  This should yield an estimate for the energy use of the function.

## Some Caveats.

* The mixture of electricity sources varies by day, by season, by time of day, and so on.
  Some times, power may come almost exclusively from solar and wind, other times, it may be
  nearly entirely fossil fuel.  In general, coal will have the highest carbon footprint,
  natural gas about half as high, and obviously wind, solar and nuclear are near zero.

* Different computers will run the same code with a different amount of energy.  Even a
  single machine may run the same code with different energy usage, depending on whether
  it uses higher efficiency or higher performance cores, CPU vs GPU usage, ram access, 
  and so on.  It will also be very difficult (though possible) to fully remove the effects of
  other software (including operating system tasks) running along with the software to be
  profiled.

* Laptops have batteries, and they may use their batteries in hard-to-predict ways.  To
  extend their battery life, they may let the battery run down and not draw current from the
  outlet, and they may do it at unpredictable times.  They may also draw more current than is
  used for processing, and charge the battery.  It would be very difficult to do this test
  with a laptop.  It may work to run the test for a very long time, on the order of hours, to
  average out any battery effects, but that... well, takes a long time, and a lot of energy,
  for something which is probably just a curiosity to you.

## Rules of thumb

* In general, the climate impact of a portion of code will be be proportional to its energy
  use, which is proportional to its runtime.  If your code runs faster, it will use less energy,
  and have less impact on the environment.

* If you really want to minimize the impact of your software, and you have some substantial
  compute needs, and you have flexibility on when the code runs (for example, ML model training,
  or periodic database analysis), consider running it around mid-day, when the sun is high,
  and solar power is abundant.  Avoid running in the early evening, as this is when demand is
  highest, and solar power is waning as the sun sets.  You may be able to get time-of-use pricing
  from your electrical utility, and this may end up saving you some money.  If you're on an
  enormous scale, you may even be able to join a demand response program and save even more money.