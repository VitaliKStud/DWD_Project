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

    **If compare == False:** With a matrix :math:`A =\left[ \begin{array}{rrr} x_{11} & x_{12} & ... & x_{1j}\\ x_{21} & x_{22} & ... & x_{2j}\\ ...    & ... & ...    & ...
    \\ x_{i1} & x_{i2} & ... & x_{ij} \\ \end{array}\right]`, which includes your data, it will calculate the average for every row:
    :math:`y(i) = \frac{\displaystyle\sum\limits_{j=1}^{kfactor} x_{ij}}{kfactor}`. While kfactor describes the number of stations around your location.

.. note::
    **if compare == True:** With a matrix :math:`A =\left[ \begin{array}{rrr} x_{11} & x_{12} & ... & x_{1j}\\ x_{21} & x_{22} & ... & x_{2j}\\ ...    & ... & ...    & ...
    \\ x_{i1} & x_{i2} & ... & x_{ij} \\ \end{array}\right]`, which includes your data, it will calculate the average for every row:
    :math:`y(i) = \frac{\displaystyle\sum\limits_{j=1}^{kfactor-1} x_{ij}}{kfactor-1}`. While kfactor-1 describes the number of stations around your location.
    The result :math:`\vec{y} = \left(\begin{array}{c}y(1)\\ y(2)\\ y(3) \\ ...\\ y(n)\end{array}\right)\\`
    represent the average of every row of your matrix A. With the first column of your matrix A, you got the vector :math:`\vec{c} = \left(\begin{array}{c}x_{11}\\ x_{21}\\ x_{31} \\ ...\\ x_{n1}\end{array}\right)\\`.
    Vector c describes the station you are comparing your calculations with (distance = 0).
    So the absolute differences are calculated as following: :math:`\vec{d} = \left(\begin{array}{c} \arrowvert y(1) - x_{11} \arrowvert\\
    \arrowvert y(2) - x_{21} \arrowvert\\
    \arrowvert y(3) - x_{31} \arrowvert\\
    ...\\
    \arrowvert y(n) - x_{n1} \arrowvert\\
    \end{array}\right) = \left(\begin{array}{c}
    d_{1}\\
    d_{2}\\
    d_{3} \\
    ...\\
    d_{n}\end{array}\right)\\ \\`.
    So the average difference is calculated as: :math:`avgdiff = \frac{\displaystyle\sum\limits_{i=1}^{n} d_{i}}{n}\\`

method: weighted average (distance)
***********************************
.. code-block:: python


    dwd.main_plotter_data(qn_weight=False, distance_weight=True, compare=False, no_plot=False)
    dwd.main_plotter_data(qn_weight=False, distance_weight=True, compare=True, no_plot=False)

.. note::

    **If compare == False:** With the vector :math:`\vec{d} = \left(\begin{array}{c}d_{1}\\  ...\\ d_{kfactor}\end{array}\right)\\` as the euclidean distance between a station and your location. It will calculate the weight for the distance as
    following: :math:`w(i) = \frac{1- \frac{\huge{d_{i}}}{\displaystyle\sum\limits_{j=1}^{kfactor} d_{j}}}{kfactor-1}` for every row in vector :math:`\vec{d}`. Note, that the kfactor for this method must be :math:`\geq 2` and describes, how many
    stations are around your location. With a matrix :math:`A =\left[ \begin{array}{rrr} x_{11} & x_{12} & ... & x_{1j}\\ x_{21} & x_{22} & ... & x_{2j}\\ ...    & ... & ...    & ...
    \\ x_{i1} & x_{i2} & ... & x_{ij} \\ \end{array}\right]`, which includes your data, it will calculate elementwise the weighted average as following:
    :math:`W =\left[ \begin{array}{rrr} x_{11}*w(1) \ + \ x_{12}*w(2) \ + \  ... \ + \ x_{1j}*w(j)\\ x_{21}*w(1)  \ + \  x_{22}*w(2)  \ + \  ...  \ + \  x_{2j}*w(j)\\ ... \\
    x_{i1}*w(1)  \ + \  x_{i2}*w(2)  \ + \  ...  \ + \  x_{ij}*w(j) \\ \end{array}\right]`.

.. note::

    **if compare == True:** With the vector :math:`\vec{e} = \left(\begin{array}{c}e_{1}\\  ...\\ e_{kfactor-1}\end{array}\right)\\` as the euclidean distance between a station and your location. It will calculate the weight for the distance as
    following: :math:`w(i) = \frac{1- \frac{\huge{e_{i}}}{\displaystyle\sum\limits_{j=2}^{kfactor-1} e_{j}}}{kfactor-2}` for every row in vector :math:`\vec{e}`. Note, that the kfactor for this method must be :math:`\geq 3` and describes, how many
    stations are around your location. With a matrix :math:`A =\left[ \begin{array}{rrr} x_{11} & x_{12} & ... & x_{1j}\\ x_{21} & x_{22} & ... & x_{2j}\\ ...    & ... & ...    & ...
    \\ x_{i1} & x_{i2} & ... & x_{ij} \\ \end{array}\right]`, which includes your data, it will calculate elementwise the weighted average as following:
    :math:`W =\left[ \begin{array}{rrr} x_{12}*w(2) \ + \  ... \ + \ x_{1j}*w(j)\\ x_{22}*w(2)  \ + \  ...  \ + \  x_{2j}*w(j)\\ ... \\
    x_{i2}*w(2)  \ + \  ...  \ + \  x_{ij}*w(j) \\ \end{array}\right] = \vec{w} = \left(\begin{array}{c}w_{1}\\  w_{2} \\...\\ w_{n}\end{array}\right)\\`. With the first column of your matrix A you got the vector
    :math:`\vec{c} = \left(\begin{array}{c}x_{11}\\ x_{21}\\ x_{31} \\ ...\\ x_{n1}\end{array}\right)\\`. Vector :math:`\vec{c}` describes the station you are comparing your calculations with (distance = 0).
    So the absolute differences are calculated as following: :math:`\vec{d} = \left(\begin{array}{c} \arrowvert w_{1} - x_{11} \arrowvert\\
    \arrowvert w_{2} - x_{21} \arrowvert\\
    \arrowvert w_{3} - x_{31} \arrowvert\\
    ...\\
    \arrowvert w_{n} - x_{n1} \arrowvert\\
    \end{array}\right) = \left(\begin{array}{c}
    d_{1}\\
    d_{2}\\
    d_{3} \\
    ...\\
    d_{n}\end{array}\right)\\ \\`.
    So the average difference is calculated as: :math:`avgdiff = \frac{\displaystyle\sum\limits_{i=1}^{n} d_{i}}{n}\\`


method: weighted data-quality (qn)
***********************************
.. code-block:: python


     dwd.main_plotter_data(qn_weight=True, distance_weight=False, compare=False, no_plot=False)
     dwd.main_plotter_data(qn_weight=True, distance_weight=False, compare=True, no_plot=False)

.. note::
    **If compare == False:** With :math:`0<QN<4` as a mark for data quality (higher is better) for every data point. So the vector :math:`\vec{q} =  \left(\begin{array}{c}q_{1}\\  ...\\ q_{kfactor}\end{array}\right)\\` describes the quality of data
    for every station. It will calculate the weighted quality of data as following: :math:`q(i) = \frac{\Large q_{i}}{\displaystyle\sum\limits_{j=1}^{kfactor} q_{j}}` for every row in :math:`\vec{q}`.  With a matrix
    :math:`A =\left[ \begin{array}{rrr} x_{11} & x_{12} & ... & x_{1j}\\ x_{21} & x_{22} & ... & x_{2j}\\ ...    & ... & ...    & ...
    \\ x_{i1} & x_{i2} & ... & x_{ij} \\ \end{array}\right]`, which includes your data, it will calculate elementwise the weighted average as following:
    :math:`Q =\left[ \begin{array}{rrr} x_{11}*q(1) \ + \ x_{12}*q(2) \ + \  ... \ + \ x_{1j}*w(j)\\ x_{21}*q(1)  \ + \  x_{22}*q(2)  \ + \  ...  \ + \  x_{2j}*q(j)\\ ... \\
    x_{i1}*q(1)  \ + \  x_{i2}*q(2)  \ + \  ...  \ + \  x_{ij}*q(j) \\ \end{array}\right]`.


.. note::

    **If compare == True:** With :math:`0<QN<4` as a mark for data quality (higher is better) for every data point. So the vector :math:`\vec{q} =  \left(\begin{array}{c}q_{1}\\  ...\\ q_{kfactor-1}\end{array}\right)\\` describes the quality of data
    for every station. It will calculate the weighted quality of data as following: :math:`q(i) = \frac{\Large q_{i}}{\displaystyle\sum\limits_{j=1}^{kfactor-1} q_{j}}` for every row in :math:`\vec{q}`.  With a matrix
    :math:`A =\left[ \begin{array}{rrr} x_{11} & x_{12} & ... & x_{1j}\\ x_{21} & x_{22} & ... & x_{2j}\\ ...    & ... & ...    & ...
    \\ x_{i1} & x_{i2} & ... & x_{ij} \\ \end{array}\right]`, which includes your data, it will calculate elementwise the weighted average as following:
    :math:`Q =\left[ \begin{array}{rrr} x_{12}*q(2) \ + \  ... \ + \ x_{1j}*q(j)\\ x_{22}*q(2)  \ + \  ...  \ + \  x_{2j}*q(j)\\ ... \\
    x_{i2}*q(2)  \ + \  ...  \ + \  x_{ij}*q(j) \\ \end{array}\right] = \vec{q} = \left(\begin{array}{c}q_{1}\\  q_{2} \\...\\ q_{n}\end{array}\right)\\`. With the first column of your matrix A you got the vector
    :math:`\vec{c} = \left(\begin{array}{c}x_{11}\\ x_{21}\\ x_{31} \\ ...\\ x_{n1}\end{array}\right)\\`. Vector :math:`\vec{c}` describes the station you are comparing your calculations with (distance = 0).
    So the absolute differences are calculated as following: :math:`\vec{d} = \left(\begin{array}{c} \arrowvert q_{1} - x_{11} \arrowvert\\
    \arrowvert q_{2} - x_{21} \arrowvert\\
    \arrowvert q_{3} - x_{31} \arrowvert\\
    ...\\
    \arrowvert q_{n} - x_{n1} \arrowvert\\
    \end{array}\right) = \left(\begin{array}{c}
    d_{1}\\
    d_{2}\\
    d_{3} \\
    ...\\
    d_{n}\end{array}\right)\\ \\`.
    So the average difference is calculated as: :math:`avgdiff = \frac{\displaystyle\sum\limits_{i=1}^{n} d_{i}}{n}\\`
