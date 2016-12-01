# team10-Project

An utility for updating the open exoplanet catelogue with external sources

Copyright (c) 2016 [Chain Coders], All Right Reserved

DIRECTORY STRUCTURE

root

|

|_Deliverables

|            |_Deliverable_1.pdf

|            |_Deliverable_2.pdf

|            |_Deliverable_3.pdf

|_Project

        |_source_
		
                 |_data_parsing
				 
                 |            |_CSV_data_parser.py
				 
                 |            |_Planet.py
				 
                 |            |_PlanetaryObject.py
				 
                 |            |_Star.py
				 
                 |            |_System.py
				 
                 |            |_XML_data_parser.py
				 
                 |
				 
                 |_data_retrieval
				 
                 |              |_apiGet.py
				 
                 |              |_remoteGet.py
				 
                 |_test
				 
				 |    |_CSVTest.py
				 
				 |    |_ProposedChangeTest.py
				 
				 |    |_TestComparator.py
				 
				 |    |_XML_data_parser_test.py
				 
                 |___init__.py
				 
                 |_driver.py
				 
                 |_installDep.sh

INSTALLATION

  -  Ensure that Python 3.x is installed

  -  Ensure that pip (https://pypi.python.org/pypi/pip) is installed

  -  Ensure that Hub (https://hub.github.com/) is installed
	 - If you're using OS-X, hub can be installed through brew by running "brew install hub"
	 - If you're using Linux, Either install Go and run the hub installation tips on their website, 
	 or Install LinuxBrew(http://linuxbrew.sh/) and run "brew install hub"

  -  IMPORTANT: Execute "installDep.sh" found in /Project/source/
     This will install the GPL-compatible "requests" library

USAGE

  -  Program is ran on the command line through passing commands to "driver.py",
     found in /Project/source/

LICENSE

  This software is licensed under the MIT License
