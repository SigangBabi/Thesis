from roboflow import Roboflow

rf = Roboflow(api_key="OjBKNg6KvztGDDu76cUk")
project = rf.workspace("thesiss-wtvnb").project("thesis-bwuft")
version = project.version(24)
dataset = version.download("yolov8")
