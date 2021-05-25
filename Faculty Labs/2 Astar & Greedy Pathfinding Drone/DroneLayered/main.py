from Controller.Controller import Controller
from View.UI import UI
from Model.Drone import Drone
from Model.Map import Map


# define a main function

def main():
    # we create the environment/map
    theMap = Map()
    theMap.loadEnvironment("test1.map")

    # we create the drone
    d = Drone()

    controller = Controller(theMap)
    UserInterface = UI(controller,theMap,d)
    UserInterface.run()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
