Mathematical equations
=======================


=============
Calculations
=============

.. code-block:: python


   import os
   from DwdMain import main_dwd
   local_domain_ = r"YOUR_PATH/"
   os.chdir(local_domain_)
   looking_for_ = ["FF_10"]
   start_date_ = 199401190000
   end_date_   = 199402191020
   x_coordinate_ = 6.0941 # 7 for compare == False
   y_coordinate_ = 50.7827 # 51 for compare == False
   z_coordinate_ = 0 # not needed for now (maybe in future)
   k_factor_ = 7 # how many station are you looking for around your location? 7 means, it will find 7 next stations for your location
   compare_station_ = "wind_00003" # needed for comparing (don't forget to set the prefix (wind_)
   type_of_data_ = "wind"
   type_of_time_ = "historical"
   dwd = main_dwd(local_domain=local_domain_,
                  type_of_data=type_of_data_,
                  type_of_time=type_of_time_,
                  start_date=start_date_,
                  end_date=end_date_,
                  compare_station=compare_station_,
                  x_coordinate=x_coordinate_,
                  y_coordinate=y_coordinate_,
                  z_coordinate=z_coordinate_,
                  k_factor=k_factor_,
                  looking_for=looking_for_)

.. code-block:: python


   dwd.main_plotter_data(qn_weight=False, distance_weight=False, compare=True, no_plot=False)


.. note::
    ..  math::
        A:= Matrix \ with \ your \ data \\
        A =
        \left[ \begin{array}{rrr}
        x_{11} & x_{12} & ... & x_{1j}\\
        x_{21} & x_{22} & ... & x_{2j}\\
        ...    & ... & ...    & ...   \\
        x_{i1} & x_{i2} & ... & x_{ij} \\
        \end{array}\right]\\

        y(i) = \frac{\displaystyle\sum\limits_{j=0}^{kfactor} x_{ij}}{kfactor}



.. code-block:: python


    dwd.main_plotter_data(qn_weight=False, distance_weight=True, compare=True, no_plot=False)

If :math:`\sigma_{1}` equals :math:`\sigma_{2}` then etc, etc.

.. code-block:: python


     dwd.main_plotter_data(qn_weight=False, distance_weight=False, compare=True, no_plot=False)

If :math:`\sigma_{1}` equals :math:`\sigma_{2}` then etc, etc.