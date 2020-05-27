# visuall-hull-extractor
utilities and functions to extract visuall hull from several image silhouettes.

Code structure is the following:
* Extract camera internal parametters and external parametters to know relative camera positions using `cam_params_position.py`
* Extract webcam image silhouette using `get_silhouette.py`
* Fuse external parametters and image silhouette information to get a 3D model (__pending to be done__). Possible implementation references:
    * https://paperswithcode.com/paper/video-based-reconstruction-of-3d-people
    * http://homepages.inf.ed.ac.uk/rbf/CVonline/LOCAL_COPIES/AV0809/schneider.pdf
    * https://paperswithcode.com/paper/deep-single-view-3d-object-reconstruction
    * https://github.com/chrischoy/3D-R2N2
    * https://paperswithcode.com/paper/learning-efficient-point-cloud-generation-for
    * https://paperswithcode.com/paper/photometric-mesh-optimization-for-video
    * https://www.sciencedirect.com/science/article/abs/pii/S0141933112000750 (I think this is the deffinitive one)


* Represent 3D model into a [virtual enviroment](https://github.com/carlesanton/3d-environment) where videogame-like navigation is possible.
