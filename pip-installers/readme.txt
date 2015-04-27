
#For use UCI internal PyPi
pip install GitPython -i http://pypi.prod.uci.cu:8081/root/pypi/+simple/

#build the installer
python setup.py sdist

#install
pip install <name>

#uninstall
pip uninstall <name>