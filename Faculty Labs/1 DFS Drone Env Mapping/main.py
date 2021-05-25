from Controller.DFSController import DFSController
from View.UI import UI
from Model.DetectedMap import DMap
from Model.Drone import Drone
from Model.Environment import Environment


# define a main function

def main():
    # we create the environment
    e = Environment()
    e.loadEnvironment("test2.map")
    # we create the map
    m = DMap()
    # we create the drone
    d = Drone()

    controller = DFSController(d,m)
    UserInterface = UI(controller,e)
    UserInterface.run()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
