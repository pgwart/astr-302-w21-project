# astr-302-w21-project

The interactiveplots module queries the SDSS data set on the fly to generate a scatter plot and Hess diagram. The query finds all stars with g - r between -0.5 and 2.5 and g 
between 14 and 24. The area searched is within a radius (in arcminutes, up to 120") of a given RA and dec (in degrees), which are manually entered through widgets.

To use, import into a Jupyter notebook and call the plots() function, then specify parameters with widgets. There are also widgets for controlling the appearance of the 
Hess diagram. 

There is a slight delay after updating parameters as it must run a new query. If the query finds no stars, such as a target outside of the survey, blank plots will be generated.
