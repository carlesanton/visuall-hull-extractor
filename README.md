# visuall-hull-extractor
utilities and functions to extract visuall hull from several image silhouettes.

Code structure is the following:
* Extract camera internal parametters and external parametters to know relative camera positions using "_cam_params_position.py_"
* Extract webcam image silhouette using "_get_silhouette.py_"
* Fuse external parametters and image silhouette information to get a 3D model (__pending to be done__)
* Represent 3D model into a virtual enviroment (in "_enviroment.py_") where videogame-like navigation is possible (using support class "_Camera.py_")
