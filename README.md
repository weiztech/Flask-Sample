# Flask Sample

###### Documentation-Driven Development API Using Flask

#

#

## Run Server

Create Mysql database with name `flask_sample` and Go to app dir

```
cd app
```

Install Dependency Modules

```
pip install -r requirements.txt
```

Call `flask init-db` command for create table and sample data (Note: should be run one time not multiple times)

```
cd app
flask init-db
```

Run Flask Server

```sh
flask run
```

## Documentation

Documentation url can be access after run server

##### Swagger

#

```
http://localhost:5000/doc/swagger-ui
```

##### Redoc

#

```
http://localhost:5000/doc/redoc
```

##### Rapidoc

#

```
http://localhost:5000/doc/rapidoc
```

## Test API

on root Folder, run below command

```
pytest
```
