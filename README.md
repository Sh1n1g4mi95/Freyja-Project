# ![Talos-Logo](arc_frejya/resources/img/Frejya_logo.png) Freyja-Project Automation Framework

> A framework developed and supported by ***Adrián Rodríguez Carneiro***

**Freyja-Project** is a [Python](https://devdocs.io/python~3.9/) test automation framework based on the BDD development
methodology. Uses a Gherkin language layer for automated test case development. It allows the automation of functional
tests web in a simple, fast and easy maintenance way.

----

## Table of Contents  
1. [About Freyja-Project](#about-Freyja-Project)  
2. [Requirements](#requirements)  
3. [How to download Freyja-Project](#how-to-download-Freyja-Project)  
   - [Download mode](#download-mode) 
4. [How to install](#how-to-install)  
5. [Folder structure](#folder-structure)  
6. [Freyja-Project settings](#talosbdd-settings)
   - [Freyja-Project config](#talosbdd-config)

----

## <a id="about-Freyja-Project">About Freyja-Project</a>
Freyja-Project is based on open technologies to offer the necessary functionalities to automate your tests. Among these
technologies are:

- [Behave](https://behave.readthedocs.io/en/latest/)
- [Selenium](https://www.seleniumhq.org/docs/)

----

## <a id="requirements">Requirements</a>

- [Python 3.9.2 16 bits](https://www.python.org/downloads/release/python-3916/)
- [PyCharm](https://www.jetbrains.com/es-es/pycharm/) as a highly recommended IDE

----

## <a id="how-to-download-Freyja-Project">How to download Freyja-Project</a>

**Freyja-Project** is managed by Adrián Rodríguez Carneiro and its base version is available in his personal GitHub repository.


### <a id="download-mode">Download mode</a>

1. Go to Freyja-Project Github repository and do a clone or download of the repository.
    - https://github.com/Sh1n1g4mi95/Freyja-Project

----

## <a id="how-to-install">How to install</a>

The installation of **Freyja-Project** is very simple, just open the project in your IDE and configure the virtual environment required. For this the following will be done:

> The following step guide will be done keeping in mind that you have selected PyCharm as your IDE. For the rest of the IDE, please find in its documentation how to configure the Python virtual environment.

1. #### Open PyCharm
2. #### In File \> Open... look for the path where I unzip the framework .zip
3. #### Make sure that in the previous step you have chosen as the parent folder the folder containing the framework files and folders.
...
----

## <a id="folder-structure">Folder structure</a>

Within the **Freyja-Project** Framework you will find the following folders

- **arc_frejya -->** There are all the files related to the functionalities of the Framework. It is recommended **not to change** the content of this folder for a good functioning of the Framework and an easy version migration. All the changes you make in this folder **will be erased** in subsequent updates.
  - **[drivers](arc_frejya/drivers/drivers.md) -->** There are all the files related to the drivers of the Framework. By default only the Firefox driver is in this folder (geckodriver)
  - **lib -->** There are the basic libraries to the Framework execution.
  - **[logs](arc_frejya/logs/logs.md) -->** There are all logs related to the Framework execution. 
  - **resources -->** There are the resources to the Framework (images, docs,...).
  - **test -->** There are the test of the Framework functions.
  - **utils -->** There are the basic Framework util functions to use in automations.
- **example_project -->** There are all the files relate to the project/module automations:
  - **automation -->** There are all the files related to the automation of the project/module.
  - **drivers -->** There are all the files related to the drivers of the project/module.

----

## <a id="talosbdd-settings">Freyja-Project settings</a>

### <a id="talosbdd-config">Freyja-Project config</a>

The default **Freyja-Project** configuration is in the **config.ini** file in the "arc_frejya" folder.

It is possible to set specific configuration for each project/module by creating **config.ini** file inside the project/module folder.
