# python_network: Python Network Monitoring API

This is a tool written for network monitoring, which is built using [pyspeedtest](https://github.com/fopina/pyspeedtest) and [flask](http://flask.pocoo.org/). The aim of this tool is to display the network information such as ping info, download and upload speed in JSON format. The author wants to use the data in building realtime network reporting tools, using either [d3.js](https://d3js.org/) or [PyBokeh](https://bokeh.pydata.org/en/latest/), however unable to realize to some personal reasons.

### How to install

Once you had launched your terminal, type the following command on the command prompt (assuming you have git and make installed):

```bash
SHELL> git clone https://github.com/tangingw/python_network.git
SHELL> cd ~/python_network
SHELL> make install_ubuntu
```

It will install the necessary libraries for this tool.

### How to use

On your terminal, type the following command:

```bash
SHELL> cd python_network
SHELL> python data_engine.py
Beginning data_engine process...
data_engine PID: 31558
data_engine PID: 31559
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
* Restarting with stat
Beginning data_engine process...
data_engine PID: 31567
data_engine PID: 31568
* Debugger is active!
* Debugger pin code: 538-722-211
```

After you see these message, type https://<YOUR IP>/network_data?key=mynetwork123456 on your browser. 
If you wish to change the key, please edit data_engine.py inside _python_network_ folder by looking for the following function:

```python
@APP.route("/network_data")
def get_network_data():

    key = request.args.get("key")

    if key == <CHANGE TO YOUR DESIRED PASSWORD/PASSPHRASE>:

        return open("result.json", "r").read()

    return json.dumps({"status": "Error", "error_msg": "Invalid Keys"})

```

### To Do

There are few more things that the author wishes to do:

1. In-depth understand on how [multiprocessing.Process](https://docs.python.org/2/library/multiprocessing.html#multiprocessing.Process) works
2. Deploy this data to either [d3.js](https://d3js.org/) or [PyBokeh](https://bokeh.pydata.org/en/latest/)
3. Make it into package like setup.py 
4. Store the key into a config.json file
5. Can't think of it at the moment.

### Note

The author is going to present this tool in [Pycon Indonesia](http://pycon.id) 2017