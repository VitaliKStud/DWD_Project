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

method: standard average
************************

.. code-block:: python


   dwd.main_plotter_data(qn_weight=False, distance_weight=False, compare=False, no_plot=False)
   dwd.main_plotter_data(qn_weight=False, distance_weight=False, compare=True, no_plot=False)



.. note::
    **if compare == False**

    ..  math::

       \begin{eqnarray}
            A =
            \left[ \begin{array}{rrr}
            x_{11} & x_{12} & ... & x_{1j}\\
            x_{21} & x_{22} & ... & x_{2j}\\
            ...    & ... & ...    & ...   \\
            x_{i1} & x_{i2} & ... & x_{ij} \\
            \end{array}\right]\\
            y(i) = \frac{\displaystyle\sum\limits_{j=1}^{kfactor} x_{ij}}{kfactor}\\
            \triangle time = endDate - startDate\\
            A:= Matrix \ with \ your \ data \\
            kfactor := number \ of \ stations \ around \ your \ location\\
            y(i) := function \ for \ every \ point \ in \ your \  \triangle time \\
        \end{eqnarray}

.. note::
    **if compare == True**

    ..  math::

        A =
        \left[ \begin{array}{rrr}
        x_{11} & x_{12} & ... & x_{1j}\\
        x_{21} & x_{22} & ... & x_{2j}\\
        ...    & ... & ...    & ...   \\
        x_{i1} & x_{i2} & ... & x_{ij} \\
        \end{array}\right]\\

        y(i) = \frac{\displaystyle\sum\limits_{j=2}^{kfactor-1} x_{ij}}{kfactor-1}\\[200mm]

        y = \left(\begin{array}{c}y(1)\\ y(2)\\ y(3) \\ ...\\ y(n)\end{array}\right)\\

        c = \left(\begin{array}{c}x_{11}\\ x_{21}\\ x_{31} \\ ...\\ x_{n1}\end{array}\right)\\

       \Rightarrow diff = \left(\begin{array}{c}
       \arrowvert y(1) - x_{11} \arrowvert\\
       \arrowvert y(2) - x_{21} \arrowvert\\
       \arrowvert y(3) - x_{31} \arrowvert\\
       ...\\
       \arrowvert y(n) - x_{n1} \arrowvert\\
       \end{array}\right) = \left(\begin{array}{c}
       d_{1}\\
       d_{2}\\
       d_{3} \\
       ...\\
       d_{n}\end{array}\right)\\ \\


        \Rightarrow avgdiff = \frac{\displaystyle\sum\limits_{i=1}^{n} d_{i}}{n}\\

        \triangle time = \ & endDate - startDate\\
        A:= \ & Matrix \ with \ your \ data \\
        kfactor := \ & number \ of \ stations \ around \ your \ location\\
        y(i) := \ &averageFunction \ for \ every \ point \ in \ your \  \triangle time \\
        y := \ &averageVector \\
        c := \ &data \ of \ the \ station \ you \ are \ comparing \ with\\

.. code-block:: python


    dwd.main_plotter_data(qn_weight=False, distance_weight=True, compare=True, no_plot=False)

If :math:`A =\left[ \begin{array}{rrr} x_{11} & x_{12} & ... & x_{1j}\\ x_{21} & x_{22} & ... & x_{2j}\\ ...    & ... & ...    & ...   \\ x_{i1} & x_{i2} & ... & x_{ij} \\ \end{array}\right]` equals :math:`\sigma_{2}` then etc, etc.

.. code-block:: python


     dwd.main_plotter_data(qn_weight=False, distance_weight=False, compare=True, no_plot=False)

If :math:`\sigma_{1}` equals :math:`\sigma_{2}` then etc, etc.