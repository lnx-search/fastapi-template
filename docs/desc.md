# 👋 Welcome to the docs

Feel free to have a look around and explore the API of lnx.

If you're new you can get started by scrolling down a bit onto the `installing` section.


# 🏗️ Installing

Setting up lnx is pretty simple overall, you will want either a copy of the docker image
or build from source to start using it.

## Building from source
You will need a newish version of rust for this, this project was built on rustc `rustc 1.52.1`
to be specific so any version beyond this should be alright.

- Download the file via `git clone https://github.com/lnx-search/lnx.git` and enter the downloaded 
folder.
- Run `cargo build --release`
- Extract the exported binary from the `target/release` folder.

*alternatively you can use `cargo run --release -- <flags>` if you want to avoid the 
job of extracting the built binary*

## Running from docker
Docker images are pre-built following the `master` branch, this becomes the `latest`
docker image tag.

#### Running via docker CLI
```bash
docker run chillfish8/lnx:latest -p "8000:8000" -e "AUTHORIZATION_KEY=hello" -e "LOG_LEVEL=info" 
```

*Note: Running without a persistent volume will mean no data will be kept
between a restart, if you intend on deploying this it is **HIGHLY** advised
you mount a volume.*

#### Running via docker-compose
```yaml
version: '3'

services:
    lnx:
      image: chillfish8/lnx:latest
      ports:
        - "8000:8000"
      volumes:
        - "/my/dir:/etc/lnx" 
      environment:
        - AUTHORIZATION_KEY=hello
        - LOG_LEVEL=info
```

# 🚀 Running
Running a default version of lnx can be done simply using the following commands:

#### Running
```
lnx <flags>
```
This will start the sever in a default configuration.

*NOTE: It is generally recommend to customise the running on lnx for production and optimum systems,
see [**optimising lnx**](/#section/Optimising) for information on why it matters for performance sake.* 

#### Help
```
lnx --help
``` 
This will bring up a detailed help command for 
all CLI options (including environment options.)

## Optional Flags
lnx provides a wide set of command line arguments to customise the running
of the server.

### Authentication Key
If specified this will require an authentication key on each request. 
 
Generally, it's recommended to have this in a production environment.

As CLI:
```
-a, --authentication-key <authentication-key>
```

As environment key:
```
AUTHENTICATION_KEY=<key>
```


### Server Host
The host to bind to (normally: '127.0.0.1' or '0.0.0.0'.) 

The default is `127.0.0.1`

As CLI:
```
-h, --host <host>
```

As environment key:
```
HOST=<host>
```


### Server Port
The port to bind the server to.

The default is `8000`

As CLI:
```
-p, --port <port>
```

As environment key:
```
PORT=<port>
```


### Log File
A optional file to send persistent logs.

This should be given as a file path.

As CLI:
```
--log-file <log-file>
```

As environment key:
```
LOG_FILE=<log-file>
```


### Log Level
The log level filter, any logs that are above this level wont be displayed.

Defaults to `info`

As CLI:
```
--log-level <log-level>
```

As environment key:
```
LOG_LEVEL=<log-level>
```


### Pretty Logs
An optional bool to use ASNI colours for log levels. 
You probably want to disable this if using file based logging.

Defaults to `true`

As CLI:
```
--pretty-logs <pretty-logs>
```

As environment key:
```
PRETTY_LOGS=<pretty-logs>
```


### Silent Search
An optional bool to disable info! level logs on every search request,
often this can boost performance quite significantly.
Defaults to `false`

As CLI:
```
--silent-search <silent-search>
```

As environment key:
```
SILENT_SEARCH=<silent-search>
```


### Runtime Threads
The number of threads to use for the [tokio](https://tokio.rs) runtime.


If this is not set, the number of logical cores on the machine is used.

As CLI:
```
-t, --runtime-threads <runtime-threads>
```

As environment key:
```
RUNTIME_THREADS=<runtime-threads>
```
