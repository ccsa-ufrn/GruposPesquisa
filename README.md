# Plataforma de Pós-Graduação

## Version 1: Juno 

Utility system for the research
programs from University Applied Social Sciences Center ([CCSA](https://ccsa.ufrn.br/)/[UFRN](http://ufrn.br/)).

This first goal is to start assembling data and providing basic information management.

## Setting up development environment

This will show up how to start the project using Linux **Lubuntu 17.04** with virtualenv.

> Read [wiki](https://github.com/ccsa-ufrn/GruposPesquisa/wiki/) for information about dockerized setup.

Having already installed:
  - Python 3.5 interpreter, ```python3``` (was already installed by default);
  - PyPI 9 client, ```pip3``` from 'python3-pip' package (usual ```sudo apt install``` command);
  - VirtualEnv module, ```python3 -m virtualenv``` command (usual ```sudo pip3 install``` script); and
  - MongoDB 3.2 and its shell ```mongo``` from an updated source (following [this Digital Ocean tutorial](https://www.digitalocean.com/community/tutorials/como-instalar-o-mongodb-no-ubuntu-16-04-pt)).

Now start by cloning this repository in a local folder and change directory to it:

```sh
git clone https://github.com/ccsa-ufrn/GruposPesquisa GruposPesquisa
cd GruposPesquisa 
```

### Virtualenv

Use these command lines to create and activate the virtual environment:

```sh
python3 -m virtualenv ./pg_env/
source ./pg_env/bin/activate
```

You will notice a ```(pg_env)``` prefixing your prompt string if it worked.
Now install all required libs:

```sh
pip install -r ./requirements.txt
```

### Database server

Let's start a mongo service. Here I run:

```sh
sudo systemctl start mongod
sudo systemctl status mongod
```

We should see, after the last command line, an output "Active: active (running)".

Assuming that there's no GruposPesquisa database installed, it's necessary to run a initial script for inputting
some initial data. It consists of redirecting some scripts to ```mongo```:

```sh
mongo < ./settings/files/standard_installation.js
```
### Testes

Not only do we need the GruposPesquisa database, but is also good practice to have a database whose only function is to 
run tests, we create that database in the next line.

```sh
mongo < ./settings/files/standard_installation_tests.js
```

Please, check if mongo output looking for errors before proceding, everything should have been
well acknowledged. Make sure to have an updated Mongo service running too.

### Web server

If packages installation went successfully and
our configuration files are ok, you can
now start running the local server:

```sh
python ./app.py
```

Assuming that you did everything right, your terminal will output the URL for you to
access using a web browser.
It should be http://localhost:3001/ but always read the output ("0.0.0.0:80" means you have super user
permission and your server is opened for public access, so you need to know your IP address instead of "localhost" or "0.0.0.0").

### Tests

If you wanna run some tests, this is what you have to do.

First you need to tell the application what database to use, you can do that by setting an environment variable, after that you can
run the unit test script test_unit.py

```sh
export DATABASE_NAME='grupospesquisa-test'
python test_unit.py
```

Any doubts, just open an issue here on GitHub!

## License

    Copyright (C) 2018 Luccas Mateus de Medeiros Gomes 
    Contact: luccasmmg@gmail.com 

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
