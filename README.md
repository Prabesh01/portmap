### Prerequisites

- python 3.6 or above.

### Installation

Install portmap from PIP
```sh
pip install git+https://github.com/Prabesh01/portmap.git
```

## Usage

```sh
$ portmap 5000
Any requests to 91.208.197.189:3456 will me mapped to port 5000 on this computer.
```

If you get command not found error, download [portmapc.py](https://raw.githubusercontent.com/Prabesh01/portmap/refs/heads/main/portmap/portmapc.py), and run it:
```sh
$ python portmapc.py <port>
```
