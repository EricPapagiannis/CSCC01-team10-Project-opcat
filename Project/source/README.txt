Deliverable 3 readme:



IMPORTANT:
Due to the nature of the CSV library is stored on NASA archive, we had to use third party (open source) python libraries (specifically: requests https://pypi.python.org/pypi/requests/2.11.1), which is not part of standard library, that is why we need the user to install it on their machine. To do that quickly, you can run the installDep.sh shell script in Project/source. (requires pip installed.)


So far we have implemented: retrieval of information from Open Exopanet Cat., as well as from NASA archive and exoplanet.eu; parsing the information from Open Exoplanet Catalogue into a form which is easy to analyse and compare. (Planet / Star / StarSystem objects, containing all the necessary information.)

driver.py contains the main function of our application. To run: driver --help for man page, or driver --update to initiate an update.