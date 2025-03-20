# Broadworks-OCIP-SOAP

[![pypi version](https://img.shields.io/pypi/v/broadworks_ocip.svg)](https://pypi.python.org/pypi/broadworks_ocip-soap)

Broadworks-OCIP-SOAP is a Python wrapper package built on top of the original [Broadworks OCI-P Interface](https://github.com/nigelm/broadworks_ocip/) package. It changes the connection method to access the Broadworks OCIP provisioning interface over the SOAP API, while keeping the same usage, commands, and overall behavior as the original package.

---

## Overview

This package leverages the hard work of the original Broadworks OCI-P Interface package and adapts it to use the SOAP API interface for communicating with a Broadworks softswitch. 

If you're already familiar with the original package, you will notice that the usage is identical, and you can refer to its documentation for further details.

However, as this is another package and uses a different connection there are small changes. For details see Installation & Usage 

---

## Features

- **SOAP API Connection:**  
  Switches the underlying connection to use SOAP API for accessing the OCIP interface.

- **Seamless Integration:**  
  Retains the same API, commands, and user experience as the original Broadworks OCI-P Interface package.

- **Fully Compatible:**  
  Uses the same Python objects matching Broadworks schema objects, supports authentication, session management, and command execution.

- **Based on Broadworks Schema R25:**  
  Adheres to the Broadworks schema R25 (with some changes from earlier R24-based implementations).

---

## Current Version

Version: 0.1.0

*Note: This version reflects the wrapper's initial release. All underlying functionality is provided by the original Broadworks OCI-P Interface package.*

---

## Installation

Install Broadworks-OCIP-SOAP with pip:

```bash
python3 -m pip install broadworks-ocip-soap
```

## Usage

The package is used in exactly the same way as the original Broadworks OCI-P Interface package. For example:

```python
from broadworks_ocip_soap import BroadworksSOAP

# Configure the API, connect, and authenticate to the Broadworks server
api = BroadworksSOAP(
    url=args.url username=args.username, password=args.password, user_agent=args.user_agent
)

# Get the platform software version
response = api.command("SystemSoftwareVersionGetRequest")
print(response.version)
```

For more detailed usage and API commands, please refer to the [orginal documentation](https://nigelm.github.io/broadworks_ocip/).

## Credits

This package builds upon the excellent work of the original Broadworks OCI-P Interface package. Special thanks to:

[@nigelm (Nigel Metheringham)](https://github.com/nigelm/) – Developer of the original Python version.

Karol Skibiński – For extensive testing, bug reporting, and valuable contributions.

[@ewurch (Eduardo Würch)](https://github.com/ewurch) – For contributing the R25 schema update and other improvements.

