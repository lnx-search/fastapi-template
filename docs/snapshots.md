Snapshots were first introduced in `v0.8.0` and provide a basic layer of wrapping up the index directory into a
single compressed file.

## Caveats
This allows you to restore your index from a previous snapshot however, there are some caveats:

- Snapshots between versions may not be compatible if the underlying storage system has changed, although rare there
  is an experimental plan later on to change the storage system.
- The bigger the index the slower the snapshot process, the snapshotting system is single threaded both extracting
  and wrapping in the first place. This allows for the rest of the system to feel minimal impact when the process is
  running but at the cost of the time it takes to produce the archive.
  On larger datasets this is probably a bad idea to have set up and instead consider just maintaining a separate back up
  of the index metadata e.g. schema, stopwords (if applicable), etc... and then the data originally indexed itself.
  On modern hardware you can index your 50GB of data in the fraction of the time it takes to decompress and export
  the equivalent snapshot. 
  An important point: **lnx should not be your primary data store, nor does it expect to be used like one.**

## Creating a snapshot
To create a snapshot you can run lnx with the `--snapshot` flag to produce a once off save.
e.g.
```shell
lnx --snapshot
```

If you want to take a snapshot ever `n` hours you can do so with the `--snapshot-interval <hours>` flag.

For example to take a snapshot every 24 hours.
```shell
lnx --snapshot-interval 24
```

*NOTE: The limits for this interval are between 1 and 255 hours*

This will produce a file in the format of:
```
snapshot-<timestamp>-lnx-v<lnx-version>
```

## Changing output directory
By default, lnx will produce snapshots in the `snapshots` directory relative to it's CWD.

You can change this by passing the `--snapshot-directory <path>` flag.

e.g.
```shell
lnx --snapshot-directory some_folder --snapshot
```


## Loading snapshots
To load snapshots you can pass the `--load-snapshot <file>` flag when running lnx.
This sub command will load the data from the snapshot and prep it to be used by lnx.

e.g.
```shell
lnx --load-snapshot ./snapshot-124213411-lnx-v0.8.0
```