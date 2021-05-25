from Controller.Controller import Controller
from View.UI import UI
from Model.Drone import Drone
from Model.Map import Map
import ast


# define a main function

def main():
    # we create the environment/map
    theMap = Map()
    theMap.loadEnvironment("test1.map")

    # we get the other in data: drone position, energy of the drone, sensors positions
    with open("data.in", 'r') as file:
        line = file.readline().strip()
        drone_pos = ast.literal_eval(line.replace("drone_position=", ""))

        line = file.readline().strip()
        drone_energy = int(line.replace("m=", ""))

        line = file.readline().strip()
        sensors_pos = ast.literal_eval(line.replace("sensors_positions=", ""))

    # we put the sensors on the map
    for s in sensors_pos:
        theMap.markSensor(s[0], s[1])

    # we get the ACO parameters
    with open("aco-params.in", 'r') as file:
        line = file.readline().strip()
        noEpoch = int(line.replace("number_of_epoch:", ""))

        line = file.readline().strip()
        noAnts = int(line.replace("number_of_ants:", ""))

        line = file.readline().strip()
        alpha = float(line.replace("alpha:", ""))

        line = file.readline().strip()
        beta = float(line.replace("beta:", ""))

        line = file.readline().strip()
        rho = float(line.replace("rho:", ""))

        line = file.readline().strip()
        q0 = float(line.replace("q0:", ""))

    # we create the drone
    d = Drone()

    # we create the controller
    controller = Controller(theMap, drone_pos, drone_energy, sensors_pos)
    controller.setACOParameters(noEpoch, noAnts, alpha, beta, rho, q0)

    UserInterface = UI(controller,theMap,d)
    UserInterface.run()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
