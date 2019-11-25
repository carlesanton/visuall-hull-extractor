# visuall-hull-extractor
utilities and functions to extract visuall hull from several image silhouettes.

Code structure is the following:


Markup : * Extract camera internal parametters and external parametters to know relative camera positions using "cam_params_position.py"
* Extract webcam image silhouette using "get_silhouette.py"
* Fuse external parametters and image silhouette information to get a 3D model (pending to be done)
* Represent 3D model into a virtual enviroment (in "enviroment.py") where videogame-like navigation is possible (using support class "Camera.py")
