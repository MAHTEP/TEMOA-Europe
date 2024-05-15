import os
import sqlite3

Postprocessing = True

# Execute the database_preprocessing.py script

if Postprocessing:
    with open("1_Transport.py") as Transport_postprocessing:
        exec(Transport_postprocessing.read())
    print("{:>62}".format('1_Transport_postprocessing processed.'))
    with open("2_TPES.py") as TPES_postprocessing:
        exec(TPES_postprocessing.read())
    print("{:>62}".format('2_TPES_postprocessing processed.'))
    with open("3_Electricity.py") as Electricity_postprocessing:
        exec(Electricity_postprocessing.read())
    print("{:>62}".format('3_Electricity_postprocessing processed.'))
    with open("4_Hydrogen.py") as Hydrogen_postprocessing:
        exec(Hydrogen_postprocessing.read())
    print("{:>62}".format('4_Hydrogen_postprocessing processed.'))
    with open("5_FC.py") as FC_postprocessing:
        exec(FC_postprocessing.read())
    print("{:>62}".format('5_FC_postprocessing processed.'))
    with open("6_Heat.py") as Heat_postprocessing:
        exec(Heat_postprocessing.read())
    print("{:>62}".format('6_Heat_postprocessing processed.'))
    with open("7_Biorefineries.py") as Biorefineries_postprocessing:
        exec(Biorefineries_postprocessing.read())
    print("{:>62}".format('7_Biorefineries_postprocessing processed.'))
    with open("8_Biorefineries feedstock.py") as Biorefineries_feedstock_postprocessing:
        exec(Biorefineries_feedstock_postprocessing.read())
    print("{:>62}".format('8_Biorefineries_feedstock_postprocessing processed.'))
    with open("9_Industrial consumption.py") as Industry_postprocessing:
        exec(Industry_postprocessing.read())
    print("{:>62}".format('9_Industrial consumption postprocessing processed.'))