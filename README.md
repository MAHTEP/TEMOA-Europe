# TEMOA-Europe

## Features

**TEMOA-Europe** is an energy system optimization model instance based on the **open-source energy system modeling framework** [**TEMOA**](https://temoacloud.com/). TEMOA-Europe is a case study based on the OECD Europe Reference Energy System.

The developing team includes Prof. Laura Savoldi[^1], Daniele Lerede[^2], Matteo Nicoli[^3], Gianvito Colucci[^3]  @ Energy Department “Galileo Ferraris” @ [**Politecnico di Torino**](https://www.polito.it/). For any inquiries, please, contact us at:
* laura.savoldi@polito.it
* daniele.lerede@polito.it
* matteo.nicoli@polito.it
* gianvito.colucci@polito.it

[^1]: Full Professor @ Politecnico di Torino, Head of the [**MAHTEP** research group](http://www.mahtep.polito.it/).
[^2]: Post-doctoral researcher @ Università degli Studi di Torino, member of the [**MAHTEP** research group] (http://www.mahtep.polito.it/).
[^3]: PhD students @ Politecnico di Torino, members of the [**MAHTEP** research group](http://www.mahtep.polito.it/).

The `temoa_energysystem/` directory contains the database of the techno-economic description for the European energy system over a time scale starting from 2005 and up to 2050:

 - `TEMOA_Europe.sql` is the text file containing the modifiable version of the database
 - `TEMOA_Europe.sqlite` is the relational dataset containing all data from `TEMOA_Europe.sql` and the necessary modifications apported through `database_preprocessing.sql` (application of interpolation rules, computation of emission activities, demand projection). `database_preprocessing.sql` is automatically called when running `database_creator.sql`.
   
If you already have TEMOA ready to run on your PC, please ensure you are using the version of the model files located in the `temoa_model` folder provided here (the main difference with respect to the standard version of the model is the implementation of capacity retirement for existing technologies).

# Contributions

The developing team wishes to receive help form the users in the definition and test of new test cases, in the benchmark against other established software, in the update of other functionalities.
To contribute please refer to [contribution](CONTRIBUTION.md).

# Code of Conduct

The developing team agreed to embrace the [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md) **Code of Conduct**.
 
 # License
 TEMOA-Europe is licensed under [![AGPL](https://www.gnu.org/graphics/agplv3-with-text-100x42.png)](LICENSE) or any other version of it.
