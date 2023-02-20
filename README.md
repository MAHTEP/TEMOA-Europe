# TEMOA-Europe

## Features

**TEMOA-Europe** is an energy system optimization model instance based on the **open-source energy system modeling framework** [**TEMOA**](https://temoacloud.com/). TEMOA-Europe is a case study based on the European Reference Energy System.

The developing team includes Prof. Laura Savoldi[^1], Daniele Lerede[^2], Matteo Nicoli[^2], Gianvito Colucci[^2]  @ Energy Department “Galileo Ferraris” @ [**Politecnico di Torino**](https://www.polito.it/). For any inquiries, please, contact us at:
* laura.savoldi@polito.it
* daniele.lerede@polito.it
* matteo.nicoli@polito.it
* gianvito.colucci@polito.it

[^1]: Head of the [**MAHTEP** research group](http://www.mahtep.polito.it/).
[^2]: PhD students @ the [**MAHTEP** research group](http://www.mahtep.polito.it/).

The `TEMOA-Europe/` directory contains the database of the techno-economic description for the European energy system over a time scale starting from 2005 up to 2100:
 - `TEMOA_Europe.sql` is the modifialble version of the dataset
 - `TEMOA_Europe_Fusion_2035` includes the binary version of the database file and the Excel file with the results for the scenario "Fusion_2035", where fusion energy is available starting from 2035;
 -  `TEMOA_Europe_Fusion_2060` includes the binary version of the database file and the Excel file with the results for the scenario "Fusion_2060", where fusion energy is available starting from 2060;
 -  `TEMOA_Europe_no_fusion` includes the binary version of the database file and the Excel file with the results for the scenario "No_fusion", where fusion energy is not available in the European energy system.

The three scenarios are described in detail in Daniele Lerede's PhD thesis (available soon)


# Contributions

The developing team wishes to receive help form the users in the definition and test of new test cases, in the benchmark against other established software, in the update of other functionalities.
To contribute please refer to [contribution](CONTRIBUTION.md).

# Code of Conduct

The developing team agreed to embrace the [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md) **Code of Conduct**.
 
 # License
 TEMOA-Europe is licensed under [![AGPL](https://www.gnu.org/graphics/agplv3-with-text-100x42.png)](LICENSE) or any other version of it.
