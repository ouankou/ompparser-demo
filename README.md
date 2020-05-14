# ompparser-demo

## Deployment using Docker

```bash
docker pull ouankou/ompparser:demo
docker run -p 8080:8080 -p 5050:5000 --name ompparser_demo ouankou/ompparser:demo &
```

Then go to `localhost:5050` to check the ompparser demo.

## Start Flask server

```bash
# make sure ompparser executable can be in the PATH variable
cd flask
python3 server.py
```

## npm

#### Install a new package

The new dependency should be added to `package.json` so that others won't miss this particular new package.
The following command will update the `package.json` during installation.

```bash
npm install <package_name> --save
```

#### Update

The following command will update the packages as well as `package-lock.json`.

```bash
npm update
```

#### Build

The final product is served after building. 
`npm ci` will find out whether `package.json` and `package-lock.json` are sufficient since it only reads from them without installing anything else not on the list.
Meanwhile, `npm install` will install the missing packages automatically even `package.json` is incomplete.

```bash
npm ci
npm run build
```

#### Commit

After the steps above, the `package.json` and `package-lock.json` should be updated and ready.
Those two files can be commited and pushed to GitHub to build a newer Docker image.
