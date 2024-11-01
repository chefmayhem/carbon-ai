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

## An Interesting Rabbit Hole

* There actually are tools out there designed to measure power use of the computer.  Depending on
  your OS and processor, there's quite some variety, but it seems the main thing is Running
  Average Power Limit (RAPL), a feature of most x86 CPUs.
* There are definitely limitations to this!  For one, it doesn't distinguish between separate cores.
  If different processes are happening on different cores, you can't tell which is which.
* The functionality is necessarily made fuzzy.  It turns out that very precise data on power use
  with a very high sampling rate can reveal significant information about what a user is doing.
  This can be used to allow processes to indirectly determine information about other processes.
  For example, a spyware program could determine which website a user is visiting by analyzing
  the energy use pattern while the website loads ([here's a description of how!](https://zhenkai-zhang.github.io/papers/rapl.pdf)).
* Because of this, the functionality is [intentionally limited](https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/advisory-guidance/running-average-power-limit-energy-reporting.html).
  This is all reasonable, but it shows that this isn't a trivial thing to do.  Also important
  to note is that this functionality is, as far as I understand, exclusive to x86 processors,
  and its exact implementation may differ between vendors and such.

## Rules of Thumb

* In general, the climate impact of a portion of code will be be proportional to its energy
  use, which is proportional to its runtime.  If your code runs faster, it will use less energy,
  and have less impact on the environment.
* You can probably get an idea of the computer's maximum power draw by looking at the power rating
  of the power adapter.
* If you really want to minimize the impact of your software, and you have some substantial
  compute needs, and you have flexibility on when the code runs (for example, ML model training,
  or periodic database analysis), consider running it around mid-day, when the sun is high,
  and solar power is abundant.  Avoid running in the early evening, as this is when demand is
  highest, and solar power is waning as the sun sets.  You may be able to get time-of-use pricing
  from your electrical utility, and this may end up saving you some money.  If you're on an
  enormous scale, you may even be able to join a demand response program and save even more money.
* Data center compute is likely to be more efficient than compute on a device such as a laptop,
  which is likely to be more efficient than compute on a desktop.

## A Simple Rough Estimation

* Here's a very back-of-the-envelope calculation.  It is not terribly accurate, but should be
  right to... maybe within a factor of ten.
* I'll assume the computer is using 60W power.  That's probably high for my laptop, but could
  easily be low for a desktop.
* I'll assume we have 0.39 kg CO2/kWh.  That comes to 0.23 kg/h, or 65 mg/s.
* I'll assume that one half of the power use on the computer comes from my code, and the other
  half from OS, other programs, etc.  That takes us to 33 mg/s.
* So, if my program takes one second to run, that corresponds to 33 mg CO2.
* You can find other calculations online, and we're within an order of magnitude.
* For the small python program I wrote to find the prime numbers between 400 and 500, which runs
  on my machine in around 30 microseconds, this corresponds to 1 microgram of CO2.

## LLM Integration and Impact

* The CO2 emissions of various LLM systems is a complicated topic.  First, consider that CO2 can
  come from model training or model inference, as well as from manufacture of data center
  equipment.  How much these emissions should be counted in a single query depends on how
  long the data center lasts, and how long between model trainings.  Arguably, emissions from
  research training might also merit being counted.
* The model used also dramatically affects the emissions.  Different models from different providers
  have wildly different impacts.  The LLM provider might source its electricity from cleaner or
  dirtier sources, though it is worth noting that, unless they're time-shifting for that efficiency,
  the use of electicity from cleaner sources is, at least to a degree, displacing other uses for that
  clean electricity, and pushing the rest of the grid onto dirtier power.
* Because this is a joke and a chance to play around with LLM integration, I'm not going to dig into
  the details.  I'm going to use an estimate of 2 g/query.  I'm basing that number on 
  [this paper](https://www.nature.com/articles/s41598-024-54271-x) published in Nature.  Very interesting
  to note is that the majority of that comes from the training expense.  I do not know how 
  reasonable the assumptions in this paper were, but I suspect that's probably within an order of
  magnitude.
* Using this module to "estimate" the CO2 emissions from a function, assuming that 2g/query estimate
  is correct, produces around 2000 times more emissions than just running the code.
* If this is accurate (and I believe it is pretty accurate, to within an order of magnitude or so), then
  this library succeeds at being the deep fried diet cola of python libraries.  You want to use
  diet cola so you get fewer calories, but you also deep fried it, negating any benefits by an
  incredible margin.