# TEMOA-Europe

## Features

**TEMOA-Europe** is an energy system model instance based on the **open-source energy system modeling framework** [**TEMOA**](https://temoacloud.com/) for integrated supply and demand optimization. TEMOA-Europe is a case study based on the OECD Europe Reference Energy System and is the first replicable and transparent tool to allow analyses concerning net-zero emissions trajectories.

For any inquiries concerning TEMOA-Europe, please contact [Laura Savoldi, Valeria di Cosmo and Matteo Nicoli](mailto:laura.savoldi@polito.it;valeria.dicosmo@unito.it;matteo.nicoli@polito.it).

The `temoa_energysystem/` directory contains the database of the techno-economic description for the European energy system over a time scale starting from 2005 and up to 2050 and results postprocessing files:

 - `TEMOA_Europe.sql` is the text file containing the modifiable version of the database
 - `TEMOA_Europe.sqlite` is the relational dataset containing all data from `TEMOA_Europe.sql` and the necessary modifications apported through `database_preprocessing.sql` (application of interpolation rules, computation of emission activities, demand projection). `database_preprocessing.sql` is automatically called when running `database_creator.sql`.

The `TEMOA_Europe_Results/` directory contains a set of detailed scenario results including: 1) Composition of the transport sector (including technological mix and fuel mix); 2) Primary energy supply; 3) Composition of the electricity generation system; 4) Hydrogen production 5) Final energy consumption 6) Composition of the heat generation sector; 7) Composition of the biofuels production sector; 8) Industrial energy consumption and technology mix; 9) Composition of the energy import/export sector. All the results are aggregate in the `Results_*.xlsx` file.
   
If you already have TEMOA ready to run on your PC, please ensure you are using the version of the model files located in the `temoa_model` folder provided here (the main difference with respect to the standard version of the model is the implementation of capacity retirement for existing technologies).

# Contributions

The developing team wishes to receive help form the users in the definition and test of new test cases, in the benchmark against other established software, in the update of other functionalities.
To contribute please refer to [contribution](CONTRIBUTION.md).

# Code of Conduct

The developing team agreed to embrace the [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md) **Code of Conduct**.
 
 # License
 TEMOA-Europe is licensed under [![AGPL](https://www.gnu.org/graphics/agplv3-with-text-100x42.png)](LICENSE) or any other version of it.
