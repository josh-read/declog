# Tutorial

Tutorial based on code in `examples/facility_example`.

This tutorial is written to demonstrate some useful functionality
built into the DecLog library, as well as how to write your own Database
backend and extend the BaseLogger.

Say for example, that we want to overhaul the way we record analysis
results at a research lab.

In the old days, all analysis would've
been performed in a lab book. This works fine, results are somewhat
searchable by date and the only limit is what can be worked out with
pen, paper and a calculator.

However, in the modern day, datasets are often so huge that it becomes
impractical to work this way. Python is one of the most popular languages
for scientific computing and data science. Jupyter notebooks provides a
development environment very much like working in a lab book. This is great,
because the limit is no longer what can be done with pen and paper, and being
saved on a computer, with a little discipline when naming files, makes them
instantly searchable.

In my view Jupyter notebooks are a fantastic tool for one offs -
little investigations which are not repeated many times. However,
when there are analysis routines which are computed over and over,
copying the same notebook and changing just a couple of variables
becomes burdensome. As for using a real notebook, there is a
searchable trail of the files/pages where calculations have been completed,
yet the results themselves are not searchable.

For example, if a function is written to measure a parameter an experiment
and each experiment is analysed in a separate file, we need to open up each
file to find the result. Now if we wanted to compare across many experiments
we would have to either go through this manual process, or write a new script
reevaluating the function for each experiment. If the analysis function
has a long run time or requires user interaction, then this quickly becomes
inconvenient.

Another issue with working using Jupyter notebooks, is there is no accounting
for changes in the functions it imports and uses. For example if the imported
function's library makes a change which refines a measurement using
improved statistics, then it is important that the results calculated prior to
this change are not compared to the results calculated after the change.

Our research lab has an extensive analysis library, providing well tested
and documented functions and classes for performing common analysis
routines on our experimental data. Each experiment involves firing a 'shot'
on one of the machines, and a number of measurements are made depending on
the interaction between the machine and the load.

## Setting custom unique keys

## Using a custom database