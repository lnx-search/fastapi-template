Generally, it is highly recommended that you enable token authorization
for lnx although you should still put lnx behind a api / reverse proxy, 
mistakes do happen.

Luckily for you lnx provides you with a simple a customisable authorization permission system.

When you first setup permissions you will need to pass a `--super-user-key <key>` as a cli option
when running lnx; this is not only how you access the endpoints to create new tokens at first
but also how lnx knows whether or not to enable auth.

When passing authentication tokens to endpoints it's expected to be in the following
format in the headers:

```
Authorization: <token>
```

## Permissions

- **MODIFY_ENGINE** - `1 << 0` = 1
    * Users with this permission can create and delete indexes.
    This is arguably the most dangerous permission aside from super user.
    
- **SEARCH_INDEX** - `1 << 1` = 2
    * Users with this permission can search their allowed indexes.
    
- **MODIFY_DOCUMENTS** - `1 << 2` = 4
    * Users with this permission can add and remove documents from their
    allowed indexes.
    
- **MODIFY_STOP_WORDS** - `1 << 3` = 8
    * Users with this permission can add and remove stop words from their
    allowed indexes.
    
- **MODIFY_AUTH** - `1 << 4` = 16
    * Users with this permission can create, revoke and modify access tokens.
    
- **SUPER_USER** - `1 | 2 | 4 | 8 | 16` = 31
    * This is just all of the above permissions combined, and can control everything.
    
    
### Calculating Permissions
Permissions are calculated bit fields meaning lnx expects an integer of the combined 
permissions you want. You can calculate the permission integer you need by taking
the bitwise `OR` / `|` of two permissions acting as a permission1 + permission2 flag.
for example if we want our token to be able to modify documents and search the index
we can do:

```
permissions = 1 << 2 | 1 << 1
```

