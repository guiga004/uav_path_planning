# Path Planning for Energy-Constrained UAV/UGV Teams in Persistent Surveillance Missions

Unmanned Aerial Vehicles (UAVs) are gaining significant attention for large-scale missions. These missions include drone delivery, precision agricultural, environmental/infrastructure monitoring, 3D modeling, patrolling, reconnaissance, etc. However, one common drawback to UAVs is the length of their flight time. One method to overcome this constraint is to deploy an Unmanned Ground Vehicle (UGV) on the mission with the UAVs. The UGV will serve as a mobile charging station, and allow the UAVs to recharge throughout the mission. 


# Instructions

Make sure that the python you are using is python 3. This can be checked using the following command:

    python -V

If python 2 comes up as the version, then try this:

    python3 - V

If this also does not return a correct python version, then python 3 must be installed.

The next step is to clone the repository:

    git clone https://github.umn.edu/guiga004/Senior-Honors-Project.githttps://github.umn.edu/guiga004/Senior-Honors-Project.git

A few necessary packages must be installed: 
    
    numpy, pandas, matplotlib, tsp

Check if pip or pip3 is installed using the following commands:

    pip -V
    pip3 -V

You want the pip corresponding to python 3. In my case, pip3 -V showed the following:
    pip 18.1 from /usr/lib/python3/dist-packages/pip (python 3.7)

To install the packages run the following commands:

    pip3 install numpy
    pip3 install pandas
    pip3 install matplotlib
    pip3 install tsp


The final step is to enter the project directory and run the testing_grounds script:

    cd <where you cloned the repo>/Senior-Honors-Project/
    python3 testing_grounds.py
