install_ubuntu:
	apt-get update
	apt-get install -y python-pip
	pip install --upgrade pip
	pip install flask pyspeedtest

clean:
	rm *.pyc