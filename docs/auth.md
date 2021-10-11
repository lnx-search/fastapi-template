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