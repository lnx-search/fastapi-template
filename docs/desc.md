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
        - "/my/dir:/etc/lnx/index" 
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

```
USAGE:                                                                                           
    lnx [OPTIONS]                                                                                
                                                                                                 
OPTIONS:                                                                                         
        --disable-asni-logs                                                                      
            An optional bool to disable ASNI colours and pretty formatting for logs. You probably
            want to disable this if using file-based logging                                     
                                                                                                 
            [env: DISABLE_ASNI_LOGS=]                                                            
                                                                                                 
    -h, --host <HOST>                                                                            
            The host to bind to (normally: '127.0.0.1' or '0.0.0.0'.)                            

            [env: HOST=]
            [default: 127.0.0.1]

        --help
            Print help information

        --json-logs
            An optional bool to enable json formatting logging.

            This formats the resulting log data into line-by-line JSON objects. This can be useful
            for log files or automatic log ingestion systems however, this can come at the cost for
            performance at very high loads.

            [env: JSON_LOGS=]

        --load-snapshot <LOAD_SNAPSHOT>
            Load a past snapshot and use it's data.

            This expects `./index` not to have any existing data or exist.

            This is technically a separate sub command.

        --log-directory <LOG_DIRECTORY>
            A optional directory to send persistent logs.

            Logs are split into hourly chunks.

            [env: LOG_DIRECTORY=]

        --log-level <LOG_LEVEL>
            The log level filter, any logs that are above this level won't be displayed.

            For more detailed control you can use the `RUST_LOG` env var.

            [env: LOG_LEVEL=]
            [default: info]

    -p, --port <PORT>
            The port to bind the server to

            [env: PORT=]
            [default: 8000]

        --pretty-logs
            An optional bool to enable pretty formatting logging.

            This for most people, this is probably too much pretty formatting however, it can make
            reading the logs easier especially when trying to debug and / or test.

            [env: PRETTY_LOGS=]

        --silent-search
            If enabled each search request wont be logged

            [env: SILENT_SEARCH=]

        --snapshot
            Generates a snapshot of the current server setup.

            The extracted snapshot will be saved in the directory provided by `--snapshot-
            directory`.

        --snapshot-directory <SNAPSHOT_DIRECTORY>
            The output directory where snapshots should be extracted to

            [env: SNAPSHOT_DIRECTORY=]
            [default: ./snapshots]

        --snapshot-interval <SNAPSHOT_INTERVAL>
            The interval time in hours to take an automatic snapshot.

            The limits are between 1 and 255 hours.

            This is quite a heavy process at larger index sizes so anything less than 24 hours is
            generally recommended against.

            The extracted snapshot will be saved in the directory provided by `--snapshot-
            directory`.

            [env: SNAPSHOT_INTERVAL=]

        --super-user-key <SUPER_USER_KEY>
            The super user key.

            If specified this will enable auth mode and require a token bearer on every endpoint.

            The super user key is used to make tokens with given permissions.

            [env: SUPER_USER_KEY]

    -t, --runtime-threads <RUNTIME_THREADS>
            The number of threads to use for the tokio runtime.

            If this is not set, the number of logical cores on the machine is used.

            [env: RUNTIME_THREADS=]

    -V, --version
            Print version information

        --verbose-logs
            An optional bool to enable verbose logging, this includes additional metadata like span
            targets, thread-names, ids, etc... as well as the existing info.

            Generally you probably dont need this unless you're debugging.

            [env: VERBOSE_LOGS=]
```