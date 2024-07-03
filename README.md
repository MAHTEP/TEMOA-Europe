# TEMOA-Europe

## Features

**TEMOA-Europe** is an energy system model instance based on the **open-source energy system modeling framework** [**TEMOA**](https://temoacloud.com/) for integrated supply and demand optimization. TEMOA-Europe is a case study based on the OECD Europe Reference Energy System and is the first replicable and transparent tool to allow analyses concerning net-zero emissions trajectories.

The developing team includes Prof. Laura Savoldi[^1], Prof. Valeria Di Cosmo[^2], Daniele Lerede[^2], Matteo Nicoli[^3], Gianvito Colucci[^3] and Dario Cottafava[^4]. For any inquiries, please, contact us at:
* laura.savoldi@polito.it
* valeria.dicosmo@unito.it
* daniele.lerede@unito.it
* matteo.nicoli@polito.it
* gianvito.colucci@polito.it
* dario.cottafava@unito.it

[^1]: Full Professor @ Politecnico di Torino, Head of the [**MAHTEP** research group](http://www.mahtep.polito.it/).
[^2]: Postdoctoral researcher @ Università degli Studi di Torino, member of the [**MAHTEP** research group](http://www.mahtep.polito.it/). Lead developer of TEMOA-Europe.
[^3]: PhD student @ Politecnico di Torino, members of the [**MAHTEP** research group](http://www.mahtep.polito.it/).
[^4]: Postdoctoral researcher @ Università degli Studi di Torino.

Davide Segantini[^5] and Daniele Lerede developed the Endogenous Technology Learning (ETL) extension of the model (branch 'etl').
* davide.segantini@studenti.polito.it
* daniele.lerede@unito.it
[^5]: MSc student @ Politecnico di Torino.

The `temoa_energysystem/` directory contains the database of the techno-economic description for the European energy system over a time scale starting from 2005 and up to 2050 and results postprocessing files:

 - `TEMOA_Europe.sql` is the text file containing the modifiable version of the database
 - `TEMOA_Europe.sqlite` is the relational dataset containing all data from `TEMOA_Europe.sql` and the necessary modifications apported through `database_preprocessing.sql` (application of interpolation rules, computation of emission activities, demand projection). `database_preprocessing.sql` is automatically called when running `database_creator.sql`.

The `TEMOA_Europe_Results/` directory contains a set of detailed scenario results including: 1) Composition of the transport sector (including technological mix and fuel mix); 2) Primary energy supply; 3) Composition of the electricity generation system; 4) Hydrogen production 5) Final energy consumption 6) Composition of the heat generation sector; 7) Composition of the biofuels production sector; 8) Industrial energy consumption and technology mix; 9) Composition of the energy import/export sector. All the results are aggregate in the `Results_*.xlsx` file.
   
If you already have TEMOA ready to run on your PC, please ensure you are using the version of the model files located in the `temoa_model` folder provided here (the main difference with respect to the standard version of the model is the implementation of capacity retirement for existing technologies).

# References
[1] D. Lerede, V. Di Cosmo, 'Temoa-Europe: An Open-Source and Open-Data Energy System Optimization Model for the Analysis of the European Energy Mix', submitted to Energy, 2024.

# Contributions

The developing team wishes to receive help form the users in the definition and test of new test cases, in the benchmark against other established software, in the update of other functionalities.
To contribute please refer to [contribution](CONTRIBUTION.md).

# Code of Conduct

The developing team agreed to embrace the [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md) **Code of Conduct**.
 
 # License
 TEMOA-Europe is licensed under [![AGPL](https://www.gnu.org/graphics/agplv3-with-text-100x42.png)](LICENSE) or any other version of it.
