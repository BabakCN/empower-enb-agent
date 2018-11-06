# EmPOWER Agent project

The EmPOWER eNB Agent, as the name says, is a component of the EmPOWER NOS (Network Operating System) which is strictly related with the LTE branch of the project. The task of this software is to provide an eNB-side (LTE base station) independent software which can communicate with the EmPOWER controller by using a set of protocols crafted for this particular job.

The Agent itself comes in the shape of a (shared) library which must be included in the Base Station, or in the software which communicates with it. The Agent must be interfaced with the eNB through the implementation of a set of functionalities that will be passed to it (the Agent) during its bootstrap (we call this part the "wrapper").

There are no restrictions on the wrapper implementation, and you are free to choose the strategy which better fit the implementation of your Base Station. Some example on how the Agent can be integrated can be found in the **srsLTE** repository (example of integration in a real eNB software) and in the **EMBase** repository (example of integration in a virtualized eNB software, a simulator).

### Compatibility
This software has been developed and tested for Linux.

## Installing from source

### Pre-requisites

The first steps, in order to proceed with the correct compilation of the software, is to download the pre-requisites for the Agent. This software comes with minimal impact on your system, and already contains all the important elements necessary for it to correctly operate. Currently there are only few requirements, and probably is something you already have on your system:

* Linux standard build suite (GCC, LD, AR, etc...).
* Pthread library, necessary to handle multithreading.
* EmPOWER eNB protocol library (see the repository **empower-enb-proto**).

These steps can be performed on any Linux distribution with the command:

`sudo apt-get install build-essential libpthread-stubs0-dev`

Note that you will need super-user right to install the additional software.

### Compile

The eNB Agent compilation uses Makefiles to perform all the necessary stages to obtain the shared library. The Makefile itself is kept minimal in order to simplify any modification that need to be applied on it. The library can be compiled with different flavour, depending in which modes you want it to operate.

In order to compile the Agent to run normally within the Base station subsystem run:

`make`

If you desire to inspect/debug the Agent internals, you can compile the library in "debug mode":

`make debug`

Finally, if you desire even more verbosity while debugging (see the RAW messages sent), you can run:

`make verbose`

### Installation/removal from the system

By default the compilation stages does not install the library in your system, but just compile and prepare it to be included in your project. If you desire to install it within your standard libraries, you need to run the following command (run as super user if you don't have the `sudo` utility):

`sudo make install`

This will copy the shared library within the `/usr/lib` folder. By doing this, you will be able to include the Agent in your projects just by compiling it with the additional flag `-lemagent`. 

The second action taken by the install command is copying the headers of the Agent inside `/usr/include/emage` folder. This will allows your projects to reach the Agent definitions from within your code by including the Agent header as it follows: `#include <emage/emage.h>`.

In the case where EmPOWER Software is no more necessary for your Base station, you can uninstall the suite from your system by running (as super user if you don't have the `sudo` utility):

`sudo make uninstall`

This will revert the changes done by the installation steps, removing the library and the headers previously installed in your system.

## Agent bindings

The library has been improved in order to include bindings of various programming languages. The bindings aim to provide an interface to the Agent library (written in C) to the environment provided by other languages.

### Python

Python bindings provides a single class named EmpowerAgent that is able to perform operations exported by the Agent library API.

Python bindings can be installed in your system by invoking the `make python` command from the root directory. After the command is correctly executed, a file called install.log will be written in the `bindings\python` folder, tracing the modification in your system. The bindings can be removed by invoking the `make remove` command from the `bindings\python` folder of the bindings (the feature is *not accessible* from the root makefile).

The class is organized as follows:

```Python
class EmpowerAgent
        # Get/set the eNB Id
        @property enb_id

        # Get/set the controller address
        @property ctrl_addr

        # Get/set the controller port
        @property ctrl_port

        # Register to an event of the Agent
        def register_to(self, event, *args)

        # Check if a particular trigger exists 
        def has_trigger(self, trig_id)
        
        # Delete a trigger by using its Id
        def del_trigger(self, trig_id)

        # Check if the Agent is connected to a controller
        def is_connected(self)

        # Start the Agent instance
        def start(self)

        # Stop the Agent instance
        def terminate(self)
```

Starting the agent will inhibits the possibility to change its properties like Id, Controller address and port. These elements will be writable again once the agent is terminated. Terminating an agent wont invalidate the class instance, and you can start it again in a second time.

The following script provides an example of how you can use the Python bindings:

```Python
#!/usr/bin/env python3
#

import time

from emage import INIT
from emage import DISCONNECTED
from emage import ENB_SETUP_REQUEST

from emage.empoweragent import EmpowerAgent

def main():
    enblist = []

    enb = EmpowerAgent(id=1)
    enblist.append(enb)

    enb.register_to(INIT, testinit)
    enb.register_to(RELEASE, testrelease)
    enb.register_to(DISCONNECTED, testdisconnect)
    enb.register_to(ENB_SETUP_REQUEST, testcap)
    enb.start()

    time.sleep(10)

    enb.terminate()

def testcap(mod):
    print("eNB capabilities requested from module " + str(mod))

def testinit():
    print("Agent initialized")

def testrelease():
    print("Agent released")

def testdisconnect():
    print("Agent disconnected")

if __name__ == "__main__":
    main()
```

The script just allocates an Agent instance with Id 1 (unspecified controller address and port will fallback to default 127.0.0.1, port 2210). The script subscribe to some Agent events, then start it. After 10 seconds of wait time the Agent is terminated and the script ends.

### License
The code is released under the Apache License, Version 2.0.
